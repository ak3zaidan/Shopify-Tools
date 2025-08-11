import datetime
import discord
import asyncio
import aiohttp
import json

try:
    with open('config.json', 'r') as file:
        config = json.load(file)
except:
    with open('ForwardPro/config.json', 'r') as file:
        config = json.load(file)

FAST_REFRESH_MODE = config['FAST_REFRESH_MODE']
TOKEN = config['TOKEN']
ChannelToMonitor = config['ChannelToMonitor']
AcoSuccessChannel = config['AcoSuccessChannel']
hex_color = int(config['EmbedColor'], 16)
Embed_Title = config['EmbedTitle']
Webhooks = config['Webhooks']

processedMessages = []
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def check_new_messages(allChannels):
    while True:
        for channel in allChannels:
            try:
                async for message in channel.history(limit=75 if FAST_REFRESH_MODE else 25):

                    current_time = datetime.datetime.now(datetime.timezone.utc)
                    time_difference = current_time - message.created_at

                    if time_difference.total_seconds() <= 45:
                        if message.id not in processedMessages:
                            getUid(message)
                            processedMessages.append(message.id)

            except discord.errors.DiscordServerError:
                print("Discord server error occurred. Retrying in a few seconds...")
                await asyncio.sleep(15)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            await asyncio.sleep(0.5 if FAST_REFRESH_MODE else 1.5)













# Mark: Ignore --------------------- ---------------------- ----------------------

def extractUID(profileName):

    temp = profileName.replace("|", "").strip()

    parts = temp.split(maxsplit=1)
    
    if len(parts) == 0:
        return (None, "")
    elif len(parts) == 1:
        if parts[0].isdigit() and len(parts[0]) > 3:
            return (parts[0], parts[0])
        else:
            return (None, parts[0])
    elif len(parts) == 2:
        if parts[0].isdigit() and len(parts[0]) > 3:
            return (parts[0], parts[1])
        else:
            return (None, profileName)

def convert_message_to_string(message):
    message_parts = []

    # Add the main content of the message
    if message.content:
        message_parts.append(f"Content: {message.content}")

    # Process embeds
    if message.embeds:
        for i, embed in enumerate(message.embeds, start=1):
            embed_dict = embed.to_dict()  # Convert the embed to a dictionary
            message_parts.append(f"Embed {i}: {json.dumps(embed_dict, indent=2)}")  # Pretty print the embed as JSON

    # Add any additional components, e.g., footer or attachments
    if hasattr(message, 'attachments') and message.attachments:
        attachments = [attachment.url for attachment in message.attachments]
        message_parts.append(f"Attachments: {attachments}")

    # Combine all parts into one big string
    return "\n\n".join(message_parts)

def getUid(message):

    def get_message_type():
        big_string = convert_message_to_string(message)

        if "Valor" in big_string:
            return 1
        elif "Cybersole" in big_string:
            return 2
        elif "AlpineAIO" in big_string:
            return 3
        elif "Make Success" in big_string:
            return 4
        elif "Swft" in big_string:
            return 5
        elif "Prism Technologies" in big_string:
            return 6
        elif "stellara_io" in big_string:
            return 7
        elif "HayhaAIO" in big_string:
            return 8
        elif "Nexar" in big_string:
            return 9
        elif "Bookie Bandit Bot" in big_string:
            return 10
        elif "NSB" in big_string:
            return 11
        elif "Enven" in big_string:
            return 12
        elif "TaranisSNKRS" in big_string:
            return 13
        elif "Shikari" in big_string:
            return 14
        else:
            return 0

    def check_card_declined():
        if "card decline" in message.content.lower():
            return True
        if message.embeds:
            for embed in message.embeds:
                if embed.title and "card decline" in embed.title.lower():
                    return True
                if embed.description and "card decline" in embed.description.lower():
                    return True
                for field in embed.fields:
                    if field.name and "card decline" in field.name.lower():
                        return True
                if embed.footer and embed.footer.text and "card decline" in embed.footer.text.lower():
                    return True
        return False

    # Return early if "card declined" is found
    if check_card_declined():
        return

    value = get_message_type()

    if value == 1:
        handleValor(message)
    elif value == 2:
        handleCyber(message)
    elif value == 3:
        handleAlpine(message)
    elif value == 4:
        handleMake(message)
    elif value == 5:
        handleSwift(message)
    elif value == 6:
        handleRefract(message)
    elif value == 7:
        handleStellar(message)
    elif value == 8:
        handleHahya(message)
    elif value == 9:
        handleNexar(message)
    elif value == 10:
        handleBookie(message)
    elif value == 11:
        handleNSB(message)
    elif value == 12:
        handleEnven(message)
    elif value == 13:
        handleTaranius(message)
    elif value == 14:
        handleShikari(message)

def handleNexar(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()  # Convert the embed to a dictionary

            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].strip("*").lower()  # Remove asterisks and lowercase
                    field_value = field['value']

                    if field_name == "site":  # Extract site
                        site = field_value
                    elif field_name == "size":  # Extract size
                        size = field_value
                    elif field_name == "product":  # Extract product
                        product = field_value
                    elif field_name == "order":  # Extract order
                        order = field_value
                    elif field_name == "profile":  # Extract profile
                        profile = field_value

            # Extract thumbnail URL
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')

            # Extract order link from 'Order' field if available
            if order:
                start_idx = order.find("(")
                end_idx = order.find(")", start_idx)
                if start_idx != -1 and end_idx != -1:
                    orderLink = order[start_idx + 1:end_idx]

                start_idx2 = order.find("[")
                end_idx2 = order.find("]", start_idx2)
                if start_idx2 != -1 and end_idx2 != -1:
                    order = order[start_idx2 + 1:end_idx2]

            # print(embed_dict)  # Debug output to inspect the embed structure

    # Check values and extract UID
    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleNSB(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()  # Convert the embed to a dictionary

            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].lower()
                    field_value = field['value']

                    if field_name == "product":  # Extract product
                        product = field_value
                    elif field_name == "site":  # Extract site
                        site = field_value
                    elif field_name == "size":  # Extract size
                        size = field_value
                    elif field_name == "profile":  # Extract profile
                        profile = field_value
                    elif field_name == "order #":  # Extract order
                        order = field_value

            # Extract thumbnail URL
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')

            # Extract order link from URL field (if applicable)
            if 'url' in embed_dict:
                orderLink = embed_dict['url']

    # Check values and extract UID
    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleEnven(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    site = "Amazon"

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()  # Convert the embed to a dictionary

            # Extract product title
            if 'title' in embed_dict:
                product = embed_dict['title']

            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].lower()
                    field_value = field['value']

                    if field_name == "asin":  # ASIN corresponds to size
                        size = field_value
                    elif field_name == "amazon account":  # Account corresponds to profile
                        profile = field_value
                    elif field_name == "order id":  # Order corresponds to order
                        order = field_value

            # Extract thumbnail URL
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')

            # Extract order link from URL field
            if 'url' in embed_dict:
                orderLink = embed_dict['url']

            # print(embed_dict)  # Debug output to inspect the embed structure

    # Check values and extract UID
    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleBookie(message):
    uid = None
    image = unitsWagered = unitsWon = account = ""

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()  # Convert embed to dictionary

            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].lower()
                    field_value = field['value']

                    if field_name == "units wagered":
                        unitsWagered = field_value
                    elif field_name == "units won":
                        unitsWon = field_value
                    elif field_name == "account":
                        account = field_value

            # Extract thumbnail URL
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')

            # print(embed_dict)  # Debug output to inspect the embed structure

    # Check values and extract UID
    values = [unitsWagered, image, unitsWon, account]
    set_count = sum(bool(value) for value in values)

    if set_count >= 2:
        result = extractUID(account)
        uid = result[0]
        account = result[1]
        asyncio.create_task(sendBookieMessage(uid, image, account, unitsWagered, unitsWon))

def handleTaranius(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()  # Convert the embed to a dictionary
            
            # Extract product from 'description'
            if 'description' in embed_dict:
                product = embed_dict['description']
            
            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].lower()
                    field_value = field['value']

                    if field_name == "region":  # Corresponds to "site"
                        site = field_value
                    elif field_name == "size":
                        size = field_value
                    elif field_name == "profileid":  # Adjusted to match "profile"
                        profile = field_value
                    elif field_name == "orderid":  # Adjusted to match "order"
                        order = field_value
                    elif field_name == "orderlink":  # If a specific field for orderLink exists
                        orderLink = field_value
            
            # Extract thumbnail URL
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')
            
            # print(embed_dict)  # Debug output to inspect the embed structure

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleHahya(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()  # Convert embed to dictionary

            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].lower()
                    field_value = field['value']

                    if field_name == "item":  # Product is in "Item" field
                        product = field_value
                    elif field_name == "site":  # Site is in "Site" field
                        site = field_value
                    elif field_name == "profile name":  # Profile is in "Profile Name" field
                        profile = field_value
                    elif field_name == "order number":  # Order is in "Order Number" field
                        order = field_value

            # Extract thumbnail URL
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')

            # Extract order link from URL field
            if 'url' in embed_dict:
                orderLink = embed_dict['url']

            # print(embed_dict)  # Debug output to inspect the embed structure

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleValor(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    if field.name.lower() == "product":
                        product = field.value
                    elif field.name.lower() == "site":
                        site = field.value
                    elif field.name.lower() == "size":
                        size = field.value
                    elif field.name.lower() == "profile":
                        profile = field.value
                    elif field.name.lower() == "order":
                        order = field.value
                    elif field.name.lower() == "orderlink":
                        orderLink = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleCyber(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.description:
                product = embed.description.split('\n')[0]

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "store":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order":
                        order = field.value

                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").replace("|", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.thumbnail:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleAlpine(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "site:":
                        site = field.value
                    elif field_name == "size:":
                        size = field.value
                    elif field_name == "profile:":
                        profile = field.value
                    elif field_name == "order:":
                        order = field.value

                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()
                    elif field_name == "product:":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")

            if embed.thumbnail:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleMake(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:

            if embed.description:
                site = embed.description.strip()

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")

                    elif field_name == "size":
                        if not size:
                            size = field.value
                    elif field_name == "profile name":
                        profile = field.value
                    elif field_name == "order":
                        order = field.value
                        # Extract order ID and order link from the order string if applicable
                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.title:
                order = embed.title  # Set order as the title of the embed
            if embed.url:
                orderLink = embed.url  # Set orderLink as the embed URL

            if embed.thumbnail and not image:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleSwift(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.strip().lower()
                    if field_name == "**site**":
                        site = field.value
                    elif field_name == "**item**":
                        product = field.value
                    elif field_name == "**profile**":
                        profile = field.value
                    elif field_name == "**order #**":
                        order = field.value.replace("||", "").strip()
                    elif field_name == "**size**":
                        size = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleRefract(message):
    uid = None
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:

            embed_str = str(embed.to_dict())

            if 'Amazon' in embed_str:
                site = 'Amazon'
            elif 'Walmart' in embed_str:
                site = 'Walmart'
            elif 'Target' in embed_str:
                site = 'Target'
            elif 'Best Buy' in embed_str:
                site = 'Best Buy'
            elif 'Nvidia' in embed_str:
                site = 'Nvidia'

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")
                    elif field_name == "price":
                        pass
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order number":
                        order = field.value
                        # Extract order ID and order link from the order string if applicable
                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            order.replace('|', '').strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.thumbnail:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order))

def handleStellar(message):
    uid = None
    product = image = site = size = profile = order = orderLink = quantity = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if "product" in field_name:
                        product = field.value
                    elif field_name == "site":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order id":
                        order = field.value
                    elif field_name == "quantity":
                        quantity = field.value
                        
                        try:
                            if int(quantity) < 2:
                                quantity = ""
                        except:
                            quantity = ""

            if embed.thumbnail:
                image = embed.thumbnail.url or ''

            # print(embed.to_dict())  # Outputs the entire embed as a dictionary for debugging

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order, quantity))

def handleShikari(message):
    import re

    uid = None
    product = image = size = profile = order = orderLink = ""
    site = "Target"

    if message.embeds:
        for embed in message.embeds:
            embed_dict = embed.to_dict()

            # Extract fields
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    field_name = field['name'].lower()
                    value = field['value']

                    if field_name == "product":
                        product = value
                    elif field_name == "profile":
                        profile = value
                    elif field_name == "order id":
                        order = value
                    elif field_name == "quantity":
                        size = value
                    elif field_name == "site":
                        site = value

            # Extract thumbnail image
            if 'thumbnail' in embed_dict:
                image = embed_dict['thumbnail'].get('url', '')

            # Extract product name and link from description
            if 'description' in embed_dict:
                match = re.search(r'\[\*\*(.*?)\*\*\]\((https?://[^\)]+)\)', embed_dict['description'])
                if match:
                    product = match.group(1)         # Extract product name
                    orderLink = match.group(2)       # Extract link
                
            # print(embed_dict)  # Optional debugging

    # Optional: Count how many variables have been set
    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        result = extractUID(profile)
        uid = result[0]
        profile = result[1]
        asyncio.create_task(sendMessage(uid, product, image, site, size, profile, orderLink, order, size))

async def sendMessage(uid, product, thumbnail_url, site, size, profile, orderLink, order, quantity = None):
    profile = profile.replace("|", "").strip()

    if uid is not None:
        try:
            user = await client.fetch_user(uid)

            if user is not None:
                if quantity:
                    description_parts = [
                        f"**Product**: {product}" if product else "",
                        f"**Site**: {site}" if site else "",
                        f"**Quantity**: {size}" if size else "",
                        f"**Profile**: {profile}" if profile else ""
                    ]
                else:
                    description_parts = [
                        f"**Product**: {product}" if product else "",
                        f"**Site**: {site}" if site else "",
                        f"**Size**: {size}" if size else "",
                        f"**Profile**: {profile}" if profile else ""
                    ]

                description_parts = [part for part in description_parts if part]

                if order or orderLink:
                    description_parts.append(
                        f"**Order**: [{order}]({orderLink})"
                    )

                description = "\n".join(description_parts)

                embed = discord.Embed(
                    title=Embed_Title,
                    description=description,
                    color=hex_color
                )

                if thumbnail_url:
                    embed.set_thumbnail(url=thumbnail_url)

                await user.send(embed=embed)
            else:
                print("User not found.")
        except:
            print(f'Bad uid input, user not found with uid: {uid}')

    await sendPublicMessage(product, thumbnail_url, site, size, profile, uid, quantity)

async def sendPublicMessage(product, thumbnail_url, site, size, profile, uid, quantity = None):
    public = client.get_channel(AcoSuccessChannel)

    if quantity:
        description_parts = [
            f"**Product**: {product}" if product else "",
            f"**Site**: {site}" if site else "",
            f"**Quantity**: {size}" if size else "",
            f"**Profile**: {profile}" if profile else ""
        ]
    else:
        description_parts = [
            f"**Product**: {product}" if product else "",
            f"**Site**: {site}" if site else "",
            f"**Size**: {size}" if size else "",
            f"**Profile**: || {profile} ||" if profile else ""
        ]

    description_parts = [part for part in description_parts if part]

    description = "\n".join(description_parts)

    embed = discord.Embed(
        title=Embed_Title,
        description=description,
        color=hex_color
    )

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    if uid is not None:
        tag = f"<@{uid}>"

        await public.send(f"{tag}\n", embed=embed)
    else:
        await public.send(embed=embed)

    embed_dict = embed.to_dict()
    payload = {
        "embeds": [embed_dict]
    }

    if uid is not None:
        payload["content"] = f"<@{uid}>"

    async with aiohttp.ClientSession() as session:
        for webhook_url in Webhooks:
            try:
                async with session.post(webhook_url, json=payload) as resp:
                    if resp.status != 204 and resp.status != 200:
                        print("\nWebhook send Rate limited")
            except Exception as e:
                print(f"Error sending to webhook {webhook_url}: {e}")

async def sendBookieMessage(uid, thumbnail_url, account, wagered, won):
    account = account.replace("|", "").strip()

    if uid is not None:
        user = await client.fetch_user(uid)

        if user is not None:
            description_parts = [
                f"**Units Wagered**: {wagered}",
                f"**Units Won**: {won}",
                f"**Account**: {account}"
            ]

            description = "\n".join(description_parts)

            embed = discord.Embed(
                title=Embed_Title,
                description=description,
                color=hex_color
            )

            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)

            await user.send(embed=embed)
        else:
            print("User not found.")

    await sendBookiePublicMessage(uid, thumbnail_url, account, wagered, won)

async def sendBookiePublicMessage(uid, thumbnail_url, account, wagered, won):
    public = client.get_channel(AcoSuccessChannel)

    description_parts = [
        f"**Units Wagered**: {wagered}",
        f"**Units Won**: {won}",
        f"**Account**: || {account} ||"
    ]

    description = "\n".join(description_parts)

    embed = discord.Embed(
        title=Embed_Title,
        description=description,
        color=hex_color
    )

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    if uid is not None:
        tag = f"<@{uid}>"

        await public.send(f"{tag}\n", embed=embed)
    else:
        await public.send(embed=embed)

@client.event
async def on_ready():
    allChannels = []

    for channel in ChannelToMonitor:
        newChannel = client.get_channel(channel)
        allChannels.append(newChannel)
    
    await check_new_messages(allChannels)

client.run(TOKEN)
