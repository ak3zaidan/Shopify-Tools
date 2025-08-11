from urllib.parse import urlparse
import threading
import requests
import random
import json
import time
import os
import re

with open('config.json', 'r') as file:
    config = json.load(file)

DELAY = config['Delay']
Webhook = config['DiscordWebHook']
Input = config['BaseUrlandInput']
proxies = []

def parse_supreme_keyword_body(body: str):
    match = re.search(r'<script type="application/json" id="products-json">(.*?)</script>', body, re.DOTALL)
    if not match:
        return None, "Error: JSON script tag not found"
    
    json_part = match.group(1)
    
    try:
        data = json.loads(json_part)
    except json.JSONDecodeError as e:
        return None, f"Error parsing JSON: {str(e)}"
    
    products_data = data.get("products", [])
    if not isinstance(products_data, list):
        return None, "Error: Products array not found in JSON"
    
    found_items = []
    
    for product in products_data:
        title = product.get("title", "")
        color = product.get("color", "")

        variants = product.get("variants", [])
        if not isinstance(variants, list):
            continue
        
        variant_list = []
        for variant in variants:
            variant_id = variant.get("id", "")
            size = variant.get("title", "")
            
            variant_list.append({
                "variantID": variant_id,
                "size": size
            })
        
        found_items.append({
            "title": title,
            "color": color,
            "variants": variant_list
        })
    
    return found_items, ""

def get_end_substring(body: str, begin: str, end: str) -> str:
    start_index = body.rfind(begin)
    if start_index == -1:
        return "-1"
    
    start_index += len(begin)
    
    end_index = body.find(end, start_index)
    
    if end_index == -1:
        return "-1"
    
    return body[start_index:end_index]

def get_substring(body: str, begin: str, end: str) -> str:
    start_index = body.find(begin)
    if start_index == -1:
        return "-1"
    
    start_index += len(begin)
    end_index = body.find(end, start_index)
    
    if end_index == -1:
        return "-1"
    
    return body[start_index:end_index]

def split_words(text):
    return [word for word in text.split() if word.strip()]

def is_url(input_string):
    try:
        result = urlparse(input_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def parse_proxy(proxy_string):
    try:
        host, port, username, password = proxy_string.split(':')
        return host, port, username, password
    except:
        return "", "", "", ""
    
def load_proxies():
    global proxies
    if not os.path.exists("proxies.txt"):
        print("Error: 'proxies.txt' not found.")
        return
    with open("proxies.txt", "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    print(f"\n\nLoaded {len(proxies)} proxies.")

def postWebhook(site, userinput, variants):
    if Webhook:
        fields = []

        if site:
            fields.append({"name": "Site", "value": site})
        if userinput:
            fields.append({"name": "Input", "value": userinput})
        if variants:
            variants_value = '\n'.join(variants)
            fields.append({"name": "Variants", "value": variants_value})

        embed = {
            "title": "Variants Found",
            "color": 65280,
            "fields": fields
        }

        payload = {
            "embeds": [embed]
        }

        json_payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        requests.post(Webhook, data=json_payload, headers=headers)

        print("\n\n\nWebhook sent!")
        print(f'Variants for site {site} on input: {userinput}:')
        print(variants)
    else:
        print("\n\n\nNo webhook configured, will only print variants")
        print(f'Variants for site {site} on input: {userinput}:')
        print(variants)

def makeRequest(proxy, endpoint, headers):
    if proxy:
        host, port, username, password = parse_proxy(proxy)
        proxies = {"http":f"http://{username}:{password}@{host}:{port}"}
    else:
        proxies = None

    try:
        response = requests.get(endpoint, headers=headers, proxies=proxies)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def checkLadyGaga(site, userinput):
    proxy = random.choice(proxies) if proxies else None

    if is_url(userinput):
        headers = {
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": userinput,
            "Priority": "u=3, i"
        }
        
        body = makeRequest(proxy, userinput, headers)

        if body:
            variant = get_substring(body, "ProductVariant/", "\"")

            if variant and variant != "-1":
                postWebhook(site, userinput, [str(variant)])
                return
        else:
            print("Err getting product link for lady gaga.")
    else:
        words = split_words(userinput)

        base_url = "https://www.ladygaga.com/us-en/search?q="
        filtered_words = [word for word in words if not word.startswith("-")]
        query_string = "+".join(filtered_words)
        Referer = base_url + query_string

        headers = {
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": Referer,
            "Priority": "u=3, i"
        }

        endpoint = Referer + "&_data=routes%2F%28%24locale%29.search"
        body = makeRequest(proxy, endpoint, headers)

        if body:
            try:
                response_body = json.loads(body)

                products = response_body.get("settings", {}).get("mostPopularSearchedItems", [])
                product_list = [
                    {"title": product["title"], "handle": product["handle"]}
                    for product in products
                    if "title" in product and "handle" in product
                ]

                shop_products = response_body.get("result", {}).get("shop", {}).get("result", [])
                product_list.extend([
                    {"title": product["title"], "handle": product["handle"]}
                    for product in shop_products
                    if "title" in product and "handle" in product
                ])
                
                foundHandle = ""

                for product in product_list:
                    title = product.get("title", "").lower()

                    required_keywords = [kw.lower() for kw in words if not kw.startswith("-")]
                    excluded_keywords = [kw.lower()[1:] for kw in words if kw.startswith("-")]

                    if all(req in title for req in required_keywords):
                        if all(excl not in title for excl in excluded_keywords):
                            foundHandle = product.get("handle", "")

                if foundHandle:
                    foundUrl = "https://www.ladygaga.com/us-en/shop/products/" + foundHandle + "?Title=Default+Title"
                    print("\nFound item link: " + foundUrl)
                    checkLadyGaga(site, foundUrl)
                    return
                else:
                    print("searching for keywords: " + "+".join(words))
            except Exception as e:
                print(f"Error parsing data, retrying")
        else:
            print("Err getting product link for lady gaga.")

    time.sleep(DELAY / 1000)
    checkLadyGaga(site, userinput)

def checkPalace(site, userinput):
    proxy = random.choice(proxies) if proxies else None

    if is_url(userinput):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Dest": "document",
            "Priority": "u=0, i"
        }
        
        body = makeRequest(proxy, userinput, headers)

        if body:
            try:
                json_string = get_substring(body, "\"variants\":{\"nodes\":", "},\"vendor\"")
                data = json.loads(json_string)
                variants = []

                for item in data:
                    variant_id = item['id'].split('/')[-1]
                    title = item['title']
                    formatted_string = f"{title}: {variant_id}"
                    variants.append(formatted_string)

                if variants:
                    postWebhook(site, userinput, variants)
                    return
            except Exception as e:
                print(f"Error parsing data, retrying")
        else:
            print("Err getting product link for palace.")
    else:
        words = split_words(userinput)

        headers = {
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://shop-usa.palaceskateboards.com/collections/new",
            "Priority": "u=3, i"
        }

        endpoint =  "https://shop-usa.palaceskateboards.com/collections/new?_data=routes%2F%28%24locale%29.collections.%24handle"

        body = makeRequest(proxy, endpoint, headers)

        if body:
            try:
                response_body = json.loads(body)

                products = response_body.get("collection", {}).get("products", {}).get("nodes", [])

                product_list = [
                    {"title": product["title"], "handle": product["handle"]}
                    for product in products
                    if "title" in product and "handle" in product
                ]
                
                foundHandle = ""

                for product in product_list:
                    title = product.get("title", "").lower()

                    required_keywords = [kw.lower() for kw in words if not kw.startswith("-")]
                    excluded_keywords = [kw.lower()[1:] for kw in words if kw.startswith("-")]

                    if all(req in title for req in required_keywords):
                        if all(excl not in title for excl in excluded_keywords):
                            foundHandle = product.get("handle", "")

                if foundHandle:
                    foundUrl = "https://shop-usa.palaceskateboards.com/products/" + foundHandle
                    print("\nFound item link: " + foundUrl)
                    checkPalace(site, foundUrl)
                    return
                else:
                    print("searching for keywords: " + "+".join(words))
            except Exception as e:
                print(f"Error parsing data, retrying")
        else:
            print("Err getting product link for palace.")
    
    time.sleep(DELAY / 1000)
    checkPalace(site, userinput)

def checkDenimTears(site, userinput):
    proxy = random.choice(proxies) if proxies else None

    if is_url(userinput):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Dest": "document",
            "Priority": "u=0, i"
        }
        
        body = makeRequest(proxy, userinput, headers)

        if body:
            try:
                json_string = get_end_substring(body, "\"variants\":{\"nodes\":", "}]},")

                if json_string != "-1":
                    json_string += "}]"

                    data = json.loads(json_string)
                    variants = []

                    for item in data:
                        variant_id = item['id'].split('/')[-1]
                        title = item['title']
                        formatted_string = f"{title}: {variant_id}"
                        variants.append(formatted_string)

                    if variants:
                        postWebhook(site, userinput, variants)
                        return
                else:
                    print(f"Error parsing data, retrying")
            except Exception as e:
                print(f"Error parsing data, retrying")
        else:
            print("Err getting product link for denim tears.")
    else:
        words = split_words(userinput)

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Dest": "document",
            "Priority": "u=0, i"
        }

        endpoint =  "https://denimtears.com/shop?categories=category%3ANew"

        body = makeRequest(proxy, endpoint, headers)

        subStr = get_substring(body, "\"products\":{\"edges\":", "}}},\"analytics\"")

        if body:
            try:
                data = json.loads(subStr)

                product_list = []
                for item in data:
                    title = item['node']['title']
                    handle = item['node']['handle']
                    product_list.append({'title': title, 'handle': handle})
        
                foundHandle = ""

                for product in product_list:
                    title = product.get("title", "").lower()

                    required_keywords = [kw.lower() for kw in words if not kw.startswith("-")]
                    excluded_keywords = [kw.lower()[1:] for kw in words if kw.startswith("-")]

                    if all(req in title for req in required_keywords):
                        if all(excl not in title for excl in excluded_keywords):
                            foundHandle = product.get("handle", "")

                if foundHandle:
                    foundUrl = "https://denimtears.com/products/" + foundHandle
                    print("\nFound item link: " + foundUrl)
                    checkDenimTears(site, foundUrl)
                    return
                else:
                    print("searching for keywords: " + "+".join(words))
            except Exception as e:
                print(f"Error parsing data, retrying")
        else:
            print("Err getting product link for denim tears.")
    
    time.sleep(DELAY / 1000)
    checkDenimTears(site, userinput)

def checkSupreme(site, userinput):
    proxy = random.choice(proxies) if proxies else None

    if is_url(userinput):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Dest": "document",
            "Priority": "u=0, i"
        }
        
        body = makeRequest(proxy, userinput, headers)

        if body:
            try:
                json_string = "[{" + get_end_substring(body, "\"variants\":[{", "}]") + "}]"

                data = json.loads(json_string)
                variants = []

                for item in data:
                    variant_id = item['id']
                    title = item['title']
                    formatted_string = f"{title}: {variant_id}"
                    variants.append(formatted_string)

                if variants:
                    postWebhook(site, userinput, variants)
                    return
            except Exception as e:
                print(f"Error parsing data, retrying")
        else:
            print("Err getting product link for supreme.")
    else:
        words = split_words(userinput)

        headers = {
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=3, i"
        }

        endpoint =  "https://us.supreme.com/collections/all"

        body = makeRequest(proxy, endpoint, headers)

        products, error = parse_supreme_keyword_body(body)
        if error:
            print("Error parsing supreme products, retrying")
        else:
            found = False
            for product in products:
                title = product.get("title", "").lower()
                color = product.get("color", "").lower()

                required_keywords = [kw.lower() for kw in words if not kw.startswith("-")]
                excluded_keywords = [kw.lower()[1:] for kw in words if kw.startswith("-")]

                if all(req in title for req in required_keywords):
                    if all(excl not in title for excl in excluded_keywords):

                        variants = product.get("variants", [])
                        filtered_variants = []
                        for variant in variants:
                            variant_str = f"{variant.get('size', '')} {color}: {variant.get('variantID', '')}"
                            filtered_variants.append(variant_str)

                        postWebhook(site, userinput, filtered_variants)
                        found = True
            
            if found:
                return

            print("Item not found, searching again")

    time.sleep(DELAY / 1000)
    checkSupreme(site, userinput)

def checkBasicShopify(site, userinput):
    proxy = random.choice(proxies) if proxies else None

    if "https://" not in site:
        site = "https://" + site
    
    endpoint = site + "/products.json?limit=" + "1000"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "document",
        "Priority": "u=0, i"
    }

    body = makeRequest(proxy, endpoint, headers)

    if body:
        try:
            data = json.loads(body)

            products_list = []

            for product in data['products']:
                title = product['title']
                handle = product['handle']
                body_html = product['body_html']
                tags = product['tags']
                variants = [f"{variant['title']}: {variant['id']}" for variant in product['variants']]
                
                product_info = {
                    'title': title,
                    'handle': handle,
                    'body_html': body_html,
                    'tags': tags,
                    'variants': variants
                }
                products_list.append(product_info)

            words = split_words(userinput)

            found = False
            for product in products_list:
                title = product.get("title", "").lower()

                required_keywords = [kw.lower() for kw in words if not kw.startswith("-")]
                excluded_keywords = [kw.lower()[1:] for kw in words if kw.startswith("-")]

                if all(req in title for req in required_keywords):
                    if all(excl not in title for excl in excluded_keywords):
                        postWebhook(site, userinput, product.get("variants", ""))
                        found = True
                
                handle = product.get("handle", "")

                if handle == userinput:
                    postWebhook(site, userinput, product.get("variants", ""))
                    found = True
                
                desc = product.get("body_html", "")

                if userinput in desc:
                    postWebhook(site, userinput, product.get("variants", ""))
                    found = True
                
                tags = product.get("tags", "")

                if userinput in tags:
                    postWebhook(site, userinput, product.get("variants", ""))
                    found = True
                
            if found:
                return
            
            print("Item not found, retrying")
            
        except Exception as e:
                print(f"Error parsing data, retrying")
    else:
        print("Err getting products.json, this shopify site may not support products.json")

    time.sleep(DELAY / 1000)
    checkBasicShopify(site, userinput)

def main():
    if not Input:
        print("Error reading input from json, or no input was provided")
        return
    
    load_proxies()

    threads = []
    for event in Input:
        site, input = event.split(',')

        if "denimtears.com" in site:
            thread = threading.Thread(target=checkDenimTears, args=(site, input))
        elif "supreme" in site:
            thread = threading.Thread(target=checkSupreme, args=(site, input))
        elif "palaceskateboards" in site:
            thread = threading.Thread(target=checkPalace, args=(site, input))
        elif "ladygaga" in site:
            thread = threading.Thread(target=checkLadyGaga, args=(site, input))
        else:
            thread = threading.Thread(target=checkBasicShopify, args=(site, input))

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Done.")

if __name__ == "__main__":
    main()
