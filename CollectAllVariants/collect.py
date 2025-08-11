import requests
import random
import json
import re
import os

SPECIFIC_SCRAPE = []
proxies = []

allSites = {
    "303 Boards": "www.303boards.com",
    "35th North": "35thnorth.com",
    "Adrift Shop CA": "www.adriftshop.com",
    "A Ma Maniere": "www.a-ma-maniere.com",
    "Antonioli EU": "antonioli.eu",
    "Analogue": "store.analogue.co",
    "APB Store": "www.apbstore.com",
    "Addict Miami": "www.addictmiami.com",
    "Afew Store": "en.afew-store.com",
    "Albino & Preto": "www.albinoandpreto.com",
    "Alife": "www.alifenewyork.com",
    "All The Right": "alltheright.com",
    "Alumni of NY": "www.alumniofny.com",
    "Amie Leon Dore": "www.aimeleondore.com",
    "ANTA": "anta.com",
    "Arts And Rec Skate Shop": "artsandrecstore.com",
    "Atlas Skateboarding": "shop.atlasskateboarding.com",
    "Asics HK": "www.asics.com.hk",
    "Asphalt NYC": "asphalt-nyc.com",
    "August Shop": "august-shop.com",
    "Awake NY": "awakenyclothing.com",
    "Bad Bunny Adidas": "badbunnyadidas.com",
    "BBBranded CA": "www.bbbranded.com",
    "BKLYN CAP": "bklyncap.com",
    "Baklava Flea Market": "baklavafleamarket.com",
    "Bandier": "www.bandier.com",
    "Bape": "us.bape.com",
    "Bape JP": "jp.bape.com",
    "Be A Spunge": "beaspunge.com",
    "Better Gift Shop": "www.bettergiftshop.com",
    "Billie Eilish Store US": "store.billieeilish.com",
    "Billie Eilish Store CA": "shopca.billieeilish.com",
    "Billionaire Boys Club": "www.bbcicecream.com",
    "Blacklist Board Shop": "blacklistboardshop.com",
    "Black Sheep Skate Shop": "blacksheepskateshop.com",
    "Blends": "www.blendsus.com",
    "Blue Tile Lounge CA": "bluetilelounge.ca",
    "Bode": "bode.com",
    "Bodega": "bdgastore.com",
    "Born X Raised": "bornxraised.com",
    "Bows Arrows Berkeley": "bowsandarrowsberkeley.com",
    "Burn Rubber": "burnrubbersneakers.com",
    "Bratz": "www.bratz.com",
    "Brooklyn Projects": "brooklynprojects.com",
    "CCS": "shop.ccs.com",
    "Crenshaw Skate Club": "crenshawskateclub.com",
    "CRSVR": "crsvr.com",
    "Cactus Plant Flea Market": "cactusplantfleamarket.com",
    "Canary Yellow": "canary---yellow.com",
    "Capsule": "capsule.nyc",
    "Carhartt WIP USA": "us.carhartt-wip.com",
    "Civilized Nation Shop": "civilizednationshop.com",
    "Civil Regime": "shop.civilclothing.com",
    "CNTRBND CA": "www.cntrbndshop.com",
    "Commonwealth FTGG": "commonwealth-ftgg.com",
    "Concepts": "cncpts.com",
    "Corporate Gotem": "corporategotem.com",
    "Coureur Goods": "coureurgoods.com",
    "Courtside CA": "www.courtsidesneakers.com",
    "Creme321": "creme321.com",
    "DarcSport": "shop.darcsport.com",
    "DSMJP E-SHOP": "shop-jp.doverstreetmarket.com",
    "DSML E-SHOP": "shop.doverstreetmarket.com",
    "DSMNY E-SHOP": "shop-us.doverstreetmarket.com",
    "DSMSG E-SHOP": "singapore.doverstreetmarket.com",
    "DTLR": "www.dtlr.com",
    "Denim Exchange": "denimexchangeusa.com",
    "Denim Tears": "denimtears.com",
    "Dime MTL": "dimemtl.com",
    "Dont Give A Putt": "dontgiveaputt.com",
    "Drew House": "thehouseofdrew.com",
    "Drift House": "www.drifthouse.com",
    "Eastside Golf": "eastsidegolf.com",
    "ECapCity": "www.ecapcity.com",
    "Eric E Manuel": "www.ericemanuel.com",
    "Exclusive Fitted": "exclusivefitted.com",
    "Exodus Ride Shop": "exodusrideshop.com",
    "Extra Butter": "extrabutterny.com",
    "Familia Skate": "familiaskate.com",
    "Fear of God": "fearofgod.com",
    "Feature": "feature.com",
    "Final Mouse": "finalmouse.com",
    "Foosh CA": "www.foosh.ca",
    "Foster": "shopfoster.com",
    "Furnace Skate": "www.furnaceskate.com",
    "FUTURA LABORATORIES": "futuralaboratories.com",
    "GBNY": "gbny.com",
    "Gallery Dept": "gallerydept.com",
    "Garage Skate Shop": "garageskateshop.com",
    "Geometric Skate Shop": "www.geometricskateshop.com",
    "GIRLS DONT CRY": "girlsdontcry.shop",
    "Good News Skate Shop CA": "goodnewsskateshop.com",
    "Grinmore Store": "www.grinmorestore.com",
    "Gym Shark": "www.gymshark.com",
    "HLorenzo": "www.hlorenzo.com",
    "Hanon Shop": "www.hanon-shop.com",
    "Hat Club": "www.hatclub.com",
    "Hat Dreams": "www.hatdreams.com",
    "Hatch Golf": "www.hatchgolf.com",
    "Haven Shop": "havenshop.com",
    "Hell Star": "hellstar.com",
    "Hell Star Golden Ticket": "hellstar.com",
    "Hirshleifers": "hirshleifers.com",
    "HOMEBRED": "homebred.com",
    "HUF Worldwide": "hufworldwide.com",
    "Humanmade JP": "humanmade.jp",
    "Humidity": "humiditynola.com",
    "Hush Life Boutique": "hushlifeboutique.com",
    "Icon Board Shop": "www.iconboardshop.com",
    "JD Sports CA": "jdsports.ca",
    "Joe Fresh Goods": "joefreshgoods.com",
    "JJJJound": "www.jjjjound.com",
    "JYW POKECA": "jyw-pokeca.com",
    "Juice": "juicestore.com",
    "JxBalvin": "jbalvin.com",
    "J Balvin Universal Music": "shop.universalmusica.com",
    "KCDC Skate Shop": "kcdcskateshop.com",
    "Kicking It ATX": "kickingit.com",
    "Kicks Crew": "www.kickscrew.com",
    "Kicks Lounge": "kickslounge.com",
    "Kicks Theory": "kickstheory.com",
    "Kinetic Skate Boarding": "kineticskateboarding.com",
    "Kith": "kith.com",
    "Kith Canada": "ca.kith.com",
    "KRS Comics": "krscomics.com",
    "Lady Gaga": "www.ladygaga.com",
    "LDRS 1354": "ldrs1354.com",
    "Labor Skateshop": "laborskateshop.com",
    "Lamb Crafted": "lambcrafted.com",
    "Lapstone and Hammer": "www.lapstoneandhammer.com",
    "Lids HD": "www.lidshd.com",
    "Likelihood": "likelihood.us",
    "Long Beach Skate Co": "lbskate.com",
    "LoveShackFancy": "www.loveshackfancy.com",
    "MCT TOKYO": "mct.tokyo",
    "Mainland Skate & Surf": "mainlandskateandsurf.com",
    "Magnolia Skate Shop": "www.magnoliaskateshop.com",
    "Makeway CA": "shopmakeway.co",
    "MNML": "mnml.la",
    "Mamba & Mambacita": "shop.mambaandmambacita.org",
    "Manorphx": "www.manorphx.com",
    "Mattel Creations": "creations.mattel.com",
    "Maxfield LA": "www.maxfieldla.com",
    "Menu Skate Shop CA": "menuskateshop.com",
    "Meta Store": "www.metastore.com",
    "Millennium Shoes": "millenniumshoes.com",
    "Momentum Cali": "momentumshop.ca",
    "MoMa Design Store": "store.moma.org",
    "My Fitteds": "www.myfitteds.com",
    "Naked Copenhagen": "nakedcph.com",
    "Ninetimes Skateshop CA": "ninetimesskateshop.com",
    "Nike x RTFKT": "rtfkt.com",
    "NJ Skateshop": "njskateshop.com",
    "NHS Skate Direct": "nhsskatedirect.com",
    "Nohble": "nohble.com",
    "NOCTA": "www.nocta.com",
    "Nomad CA": "nomadshop.net",
    "NRML": "nrml.ca",
    "No Comply Skateshop": "nocomplyatx.com",
    "Notre": "www.notre-shop.com",
    "Obey Giant": "obeygiant.com",
    "Olivia Rodrigo": "store.oliviarodrigo.com",
    "Olympia Skate Shop": "olympiaskateshop.com",
    "Oneblockdown ROW": "oneblockdown.com",
    "Oneness Boutique": "www.onenessboutique.com",
    "Orchard Shop": "orchardshop.com",
    "Octobers Very Own": "us.octobersveryown.com",
    "Packer": "packershoes.com",
    "Palace US": "www.palaceskateboards.com",
    "PLA Skateboarding": "www.plaskateboarding.com",
    "Pawnshop Skate Co": "pawnshopskate.com",
    "Patta": "pattaclothing.us",
    "PDP Gaming": "pdp.com",
    "Pharmacy Board Shop": "pharmacyboardshop.com",
    "Phenom": "ca.phenomglobal.com",
    "Premium Goods": "premiumgoods.com",
    "Private Sneakers": "www.privatesneakers.com",
    "Pro Image America": "proimageamerica.com",
    "Prociety Shop": "procietyshop.com",
    "Proper LBC": "properlbc.com",
    "Puffer Reds": "pufferreds.com",
    "Renarts": "renarts.com",
    "Reynolds & Sons": "reynoldsandsons.com",
    "RSVP Gallery": "rsvpgallery.com",
    "Rock City Kicks": "rockcitykicks.com",
    "Rule of Next": "www.ruleofnext.com",
    "Sp5der Worldwide": "kingspider.co",
    "SVRN": "www.svrn.com",
    "Saint Alfred": "www.saintalfred.com",
    "Sandy Liang": "www.sandyliang.info",
    "Sesinko": "sesinko.com",
    "Skate Park of Tampa": "skateparkoftampa.com",
    "Shoe Palace": "www.shoepalace.com",
    "Shop Kings": "www.shopatkings.com",
    "Shop Nice Kicks": "shopnicekicks.com",
    "Shop Overload": "shopoverload.com",
    "ShopWSS": "www.shopwss.com",
    "Size?": "www.size.co.uk",
    "Slam Jam": "us.slamjam.com",
    "Sneakerbox Cali": "sneakerboxshop.ca",
    "Sneaker Junkies": "sneakerjunkiesusa.com",
    "Sneaker Politics": "sneakerpolitics.com",
    "Sneaker Town": "www.sneakertownmia.com",
    "Social Status": "www.socialstatuspgh.com",
    "Sole Classics": "www.soleclassics.com",
    "Solefly": "www.solefly.com",
    "Sole Play": "www.soleplayatl.com",
    "Solestop": "www.solestop.com",
    "Somewhere": "somewhereofficial.com",
    "Specializing In Life": "www.specializinginlife.com",
    "Sports World": "sportsworld165.com",
    "Sporty & Rich": "sportyandrich.com",
    "Spusta Studio Shop": "shop.marqspusta.com",
    "Stadium Status": "www.stadiumstatusla.com",
    "Stanley 1913": "www.stanley1913.com",
    "Stanley 1913 CA": "ca.stanley1913.com",
    "Stashed": "stashedsf.com",
    "Strange Love": "www.strangeloveshop.com",
    "Stussy": "www.stussy.com",
    "Succezz": "succezzthestore.com",
    "Sun Diego Board Shop": "sundiego.com",
    "Super Cool Studios": "getsupercool.com",
    "Supreme EU": "eu.supreme.com",
    "Supreme JP": "jp.supreme.com",
    "Supreme UK": "uk.supreme.com",
    "Supreme US": "us.supreme.com",
    "Swag Golf": "swag.golf",
    "Swell-O-Phonic": "shopswellophonic.com",
    "Takeout NY": "takeoutny.com",
    "Taylor Swift Official Store": "store.taylorswift.com",
    "Taylor Swift Store CA": "storeca.taylorswift.com",
    "Taylor Swift Store UK": "storeuk.taylorswift.com",
    "Telfar": "telfar.net",
    "Tiki Room Skateboards CA": "tikiroomskateboards.com",
    "Time Machine Skate Shop": "timemachineskateshop.com",
    "The Better Generation": "thebettergeneration.com",
    "TheClosetinc CA": "www.theclosetinc.com",
    "The Darkside Initiative": "www.thedarksideinitiative.com",
    "The Premier Store": "thepremierstore.com",
    "There Skateboards": "thereskateboards.com",
    "Todd Snyder": "www.toddsnyder.com",
    "Tom Sachs": "store.tomsachs.com",
    "Tony Brimz": "tonybrimz.com",
    "Tops and Bottoms USA": "www.topsandbottomsusa.com",
    "Travel Skate Shop": "www.travelskateshop.com",
    "Travis Scott": "www.travisscott.com",
    "Tres Bien": "tres-bien.com",
    "Trophy Room": "www.trophyroomstore.com",
    "Two18": "two18.com",
    "UNheardof": "unheardofbrand.com",
    "UPNYC Store": "upnycstore.com",
    "Uprise Skate Shop": "upriseskateshop.com",
    "USA Cap King": "usacapking.com",
    "Undefeated": "undefeated.com",
    "Underground Skate Shop": "www.undergroundskateshop.com",
    "Union": "store.unionlosangeles.com",
    "Val Surf": "valsurf.com",
    "Wales Bonner": "walesbonner.com",
    "WALLHACK": "wallhack.com",
    "We Are Civil": "www.wearecivil.com",
    "Wish ATL": "wishatl.com",
    "wooDstack": "www.woodstack.com",
    "Wutang Clan": "www.thewutangclan.com",
    "Xhibition": "www.xhibition.co",
    "Xtreme Board Shop": "xbusa.com"
}

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
        variants = product.get("variants", [])
        if not isinstance(variants, list):
            continue
        
        variant_list = []
        for variant in variants:
            variant_id = variant.get("id", "")
            
            variant_list.append(variant_id)
        
        found_items.append({
            "variants": variant_list
        })
    
    return found_items, ""

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

def create_files(created_dict):
    # Go format
    go_dict = 'var urlToVariant = map[string][]string{\n'
    go_dict += ",\n".join([f'    "{url}": {json.dumps(variant)}' for url, variant in created_dict.items()])
    go_dict += "\n}"

    # Swift format
    swift_dict = 'let urlToVariant: [String: [String]] = [\n'
    swift_dict += ",\n".join([f'    "{url}": {variant}' for url, variant in created_dict.items()])
    swift_dict += "\n]"

    # Python format
    python_dict = 'url_to_variant = {\n'
    python_dict += ",\n".join([f'    "{url}": {variant}' for url, variant in created_dict.items()])
    python_dict += "\n}"

    # Write to files
    with open("GoFormat1.txt", "w") as go_file:
        go_file.write(go_dict)

    with open("SwiftFormat1.txt", "w") as swift_file:
        swift_file.write(swift_dict)

    with open("PythonFormat1.txt", "w") as python_file:
        python_file.write(python_dict)

    print("\nGo, Swift, and Python format files generated successfully!")

def add_to_cart(proxy, variant_id, base_url):
    if not base_url.startswith("https://"):
        base_url = "https://" + base_url
    
    url = f"{base_url.rstrip('/')}/cart/add.js"
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Origin": base_url,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
    }
    formData = {
        "items": [
            {
                "id": variant_id,
                "quantity": 1,
                "properties": {"variant_inventorystatus": "Available"} if "creations.mattel" in base_url else {}
            }
        ]
    }

    host, port, username, password = parse_proxy(proxy)
    
    json_data = json.dumps(formData)
    headers["Content-Length"] = str(len(json_data))
    proxies = {"http": f"http://{username}:{password}@{host}:{port}"} if proxy else None

    try:
        response = requests.post(url, headers=headers, data=json_data, proxies=proxies)

        if response.status_code != 200:
            return "", f"Failed to add to cart with status code: {response.status_code}"

        return response.text, ""
    except requests.exceptions.RequestException as e:
        return "", f"Error making request: {e}"

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

def checkLadyGaga(userinput):
    proxy = random.choice(proxies) if proxies else None

    if userinput:
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
            allVars = []
            allVars.append(get_end_substring(body, "ProductVariant/", "\""))
            return allVars
    else:
        base_url = "https://www.ladygaga.com/us-en/shop/collections/all"
        
        headers = {
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": base_url,
            "Priority": "u=3, i"
        }

        body = makeRequest(proxy, base_url, headers)

        if body:
            bodyStr = str(body)

            foundUrl = get_substring(bodyStr, "\"position\":10,\"url\":\"", "\"}")

            if foundUrl == "-1":
                return []

            return checkLadyGaga(foundUrl)

    return []

def checkPalace(userinput):
    returnAnyways = []
    proxy = random.choice(proxies) if proxies else None

    if userinput:
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
                    
                multipleVars = []
                for item in data:
                    variant_id = item['id'].split('/')[-1]

                    if variant_id:
                        _, atcError = add_to_cart(proxy, variant_id, "shop-usa.palaceskateboards.com")

                        if not atcError:
                            multipleVars.append(variant_id)
                        else:
                            returnAnyways.append(variant_id)

                        if len(multipleVars) == 3:
                            return multipleVars
                        
                if multipleVars:
                    return multipleVars
                else:
                    return returnAnyways
                    
            except:
                return []
    else:
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
                
                for product in reversed(product_list):
                    foundHandle = product.get("handle", "")

                    if foundHandle:
                        foundUrl = "https://shop-usa.palaceskateboards.com/products/" + foundHandle
                        return checkPalace(foundUrl)
            except:
                return []
    
    return returnAnyways

def checkDenimTears(userinput):
    proxy = random.choice(proxies) if proxies else None

    if userinput:
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

                    multipleVars = []
                    for item in data:
                        variant_id = item['id'].split('/')[-1]

                        if variant_id:
                            _, atcError = add_to_cart(proxy, variant_id, "denimtears.com")

                            if not atcError:
                                multipleVars.append(variant_id)
                            if len(multipleVars) == 3:
                                return multipleVars
                    return multipleVars
                
            except:
                return []
    else:
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
        
                for product in reversed(product_list):
                    foundHandle = product.get("handle", "")

                    if foundHandle:
                        foundUrl = "https://denimtears.com/products/" + foundHandle
                        return checkDenimTears(foundUrl)
            except:
                return []
    
    return []

def checkSupreme():
    proxy = random.choice(proxies) if proxies else None

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

    multipleVars = []
    products, error = parse_supreme_keyword_body(body)
    if not error:
        for product in reversed(products):
            if product['variants']:
                singleVar = product['variants'][0]

                _, atcError = add_to_cart(proxy, singleVar, "us.supreme.com")

                if not atcError:
                    multipleVars.append(singleVar)
                if len(multipleVars) == 3:
                    return multipleVars

    return multipleVars

def checkBasicShopify(retry, site):
    proxy = random.choice(proxies) if proxies else None

    if "https://" not in site:
        site = "https://" + site
    
    endpoint = site + "/products.json?limit=" + "70"

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
                variants = [f"{variant['id']}" for variant in product['variants']]
                
                product_info = {
                    'variants': variants
                }
                products_list.append(product_info)

            multipleVars = []
            for product in reversed(products_list):
                if product['variants']:
                    singleVar = product['variants'][0]

                    _, atcError = add_to_cart(proxy, singleVar, site)

                    if not atcError:
                        multipleVars.append(singleVar)
                    if len(multipleVars) == 3:
                        return multipleVars
        except:
            if retry:
                return checkBasicShopify(False, site)
            else:
                return []
    elif retry:
        return checkBasicShopify(False, site)

    return []

def GetVariant(site):
    if "denimtears.com" in site:
        return checkDenimTears(None)
    elif "supreme" in site:
        return checkSupreme()
    elif "palaceskateboards" in site:
        return checkPalace(None)
    elif "ladygaga" in site:
        return checkLadyGaga(None)
    else:
        return checkBasicShopify(True, site)

def main():
    load_proxies()

    createdDict = {}

    if SPECIFIC_SCRAPE:
        for url in SPECIFIC_SCRAPE:
            variant = GetVariant(url)
            createdDict[url] = variant

        print("\n\nData is \n\n")
        print(createdDict)
        print("\n\nDone.")

    else:
        index = 1

        for _, url in allSites.items():
            print("Getting site " + str(index))
            variant = GetVariant(url)
            createdDict[url] = variant
            index += 1

        for url, variant in createdDict.items():
            if variant == "-1":
                retryVariant = GetVariant(url)
                createdDict[url] = retryVariant
        
        create_files(createdDict)
        print("\n\nDone.")
        
if __name__ == "__main__":
    main()
