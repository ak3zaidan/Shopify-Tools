from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
import requests_go
import discord
import random
import json
import html
import csv
import os

SKIP_CHECK = True
TEST_MODE = False
TEST_LINK = "https://us.checkout.gymshark.com/checkouts/c/e1efc890e20bda63e1ce65f82a3bb627/thank_you"

try:
    with open('config.json', 'r') as file:
        config = json.load(file)
except:
    with open('CsvPro/config.json', 'r') as file:
        config = json.load(file)

TOKEN = config['TOKEN']
FILTER = config['Filter']
ChannelToMonitor = config['ChannelToScrape']

processedMessages = []
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
proxies = []

# Order check functions

def get_substring(body: str, begin: str, end: str) -> str:
    start_index = body.find(begin)
    if start_index == -1:
        return "-1"
    
    start_index += len(begin)
    end_index = body.find(end, start_index)
    
    if end_index == -1:
        return "-1"
    
    return body[start_index:end_index]

def load_proxies():
    """
    Load proxies from the appropriate file based on configuration.
    """
    global proxies

    try:
        if not os.path.exists("proxies.txt"):
            raise Exception("Error: 'proxies.txt' not found.")

        with open("proxies.txt", "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
    except:
        if not os.path.exists("CsvPro/proxies.txt"):
            print("Error: 'proxies.txt' not found.")
            return
        with open("CsvPro/proxies.txt", "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
        
    print(f"\n\nLoaded {len(proxies)} proxies.")

def parse_proxy(proxy_string):
    """
    Parse a proxy string into its components.
    
    Args:
        proxy_string: String in format "host:port:username:password"
        
    Returns:
        tuple: (host, port, username, password) or empty strings if invalid
    """
    try:
        host, port, username, password = proxy_string.split(':')
        return host, port, username, password
    except:
        return "", "", "", ""

def update_order_status(order_link, retry=True):
    global proxies

    if SKIP_CHECK:
        return "NA"

    if not order_link:
        return "NA"
    
    if "paypal" in order_link.lower():
        return "NA"

    headers = {
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i"
    }

    header_order = [
        "sec-ch-ua",
        "sec-ch-ua-mobile",
        "sec-ch-ua-platform",
        "upgrade-insecure-requests",
        "user-agent",
        "accept",
        "sec-fetch-site",
        "sec-fetch-mode",
        "sec-fetch-user",
        "sec-fetch-dest",
        "accept-encoding",
        "accept-language",
        "priority"
    ]

    tls = requests_go.tls_config.TLSConfig()
    tls.random_ja3 = True
    tls.headers_order = header_order
    
    randomProxy = random.choice(proxies)
    host, port, username, password = parse_proxy(randomProxy)
    proxy_url = f"http://{username}:{password}@{host}:{port}"

    proxy = {
        "http": proxy_url,
        "https": proxy_url
    }    

    try:
        response = requests_go.get(order_link, headers=headers, proxies=proxy, tls_config=tls)
        body = html.unescape(response.text)
        body_lower = body.lower()

        orderId = get_substring(body_lower, '"orderid":"', '"')

        if orderId == "-1":
            return "NA"
        
        payload = {
            "operationName": "OrderDetails",
            "variables": {
                "redacted": True,
                "isReturnFeesEnabled": False,
                "isPreAuth": False,
                "isRedactedOrBusinessCustomer": True,
                "extensionIds": ["gid://shopify/UiExtension/1bd251a9-d2dd-4773-b5a3-aae80b649fbb", "gid://shopify/UiExtension/1a56fc36-532a-4e1b-9d04-c090a6eed4e8", "gid://shopify/UiExtension/1a56fc36-532a-4e1b-9d04-c090a6eed4e8", "gid://shopify/UiExtension/1a56fc36-532a-4e1b-9d04-c090a6eed4e8", "gid://shopify/UiExtension/1a56fc36-532a-4e1b-9d04-c090a6eed4e8", "gid://shopify/UiExtension/2d675569-4975-4198-9178-7db148d5e621", "gid://shopify/UiExtension/1b52b47b-1498-4507-bdb2-dfbab3cc77e3", "gid://shopify/UiExtension/a4eee822-4d05-4932-b511-5e9801fc9795", "gid://shopify/UiExtension/1a56fc36-532a-4e1b-9d04-c090a6eed4e8", "gid://shopify/UiExtension/659e6aab-976f-4e39-b70a-85549d8f7270", "gid://shopify/UiExtension/85476acc-cfdf-4844-b9d1-164b82dcc7d1", "gid://shopify/UiExtension/1b52b47b-1498-4507-bdb2-dfbab3cc77e3"],
                "skipExchangeLineItems": False,
                "orderId": f'gid://shopify/Order/{orderId}',
                "isBusinessCustomer": False
            },
            "query": "query OrderDetails($orderId: ID!, $isBusinessCustomer: Boolean!, $redacted: Boolean = false, $isReturnFeesEnabled: Boolean = false, $isPreAuth: Boolean = false, $isRedactedOrBusinessCustomer: Boolean = false, $extensionIds: [ID!] = [], $skipExchangeLineItems: Boolean = true) {\n  order(id: $orderId) {\n    id\n    ...OrderFragment\n    customer @skip(if: $redacted) {\n      id\n      emailAddress {\n        emailAddress\n        marketingState\n        __typename\n      }\n      firstName @skip(if: $isPreAuth)\n      lastName @skip(if: $isPreAuth)\n      phoneNumber {\n        phoneNumber @skip(if: $isPreAuth)\n        marketingState\n        __typename\n      }\n      imageUrl @skip(if: $isPreAuth)\n      displayName @skip(if: $isPreAuth)\n      displayContact @include(if: $isPreAuth)\n      __typename\n    }\n    poNumber @include(if: $isBusinessCustomer)\n    pickupInformation {\n      address @skip(if: $redacted) {\n        address1\n        address2\n        city\n        countryCode\n        zip\n        zoneCode\n        __typename\n      }\n      status\n      updatedAt\n      __typename\n    }\n    shopAppLinksAndResources @skip(if: $isRedactedOrBusinessCustomer) {\n      canTrackOrderUpdates\n      qrCodeUrl\n      mobileUrl\n      shopAppQrCodeKillswitch\n      shopAppEligible\n      mobileUrlAttributionPayload\n      shopPayOrder\n      shopInstallmentsViewSchedules\n      installmentsHighlightEligible\n      shopInstallmentsMobileUrl\n      __typename\n    }\n    pickupPointInformation @skip(if: $isRedactedOrBusinessCustomer) {\n      name\n      carrierName\n      carrierLogoUrl\n      address {\n        address1\n        address2\n        city\n        countryCode\n        zip\n        zoneCode\n        __typename\n      }\n      __typename\n    }\n    returnInformation {\n      ...NonReturnableSummary\n      returnFees @include(if: $isReturnFeesEnabled) {\n        amountSet {\n          presentmentMoney {\n            ...Price\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ...Returns\n    ...VatInvoices @skip(if: $redacted)\n    __typename\n  }\n  uiExtensionMetafields(orderId: $orderId, extensionIds: $extensionIds) @skip(if: $redacted) {\n    id\n    ownerId\n    key\n    namespace\n    type\n    value\n    valueType\n    __typename\n  }\n}\n\nfragment OrderFragment on Order {\n  id\n  name\n  confirmationNumber\n  processedAt\n  cancelledAt\n  draftOrderName\n  currencyCode @skip(if: $redacted)\n  hasEmail\n  email @skip(if: $redacted)\n  automaticDeferredPaymentCollection\n  transactions @skip(if: $redacted) {\n    ...OrderTransaction\n    __typename\n  }\n  dutiesIncluded\n  discountInformation {\n    allOrderLevelAppliedDiscounts: allOrderLevelAppliedDiscountsOnSoldItems {\n      title @skip(if: $redacted)\n      targetType\n      discountApplicationType @skip(if: $redacted)\n      discountValue {\n        ...Price\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  billingAddress @skip(if: $redacted) {\n    id\n    ...Address\n    __typename\n  }\n  shippingAddress @skip(if: $redacted) {\n    id\n    ...Address\n    __typename\n  }\n  shippingTitle @skip(if: $redacted)\n  fulfillments(\n    first: 20\n    sortKey: CREATED_AT\n    reverse: true\n    query: \"NOT status:CANCELLED\"\n  ) {\n    edges {\n      node {\n        id\n        ...Fulfillment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  editSummary {\n    ...OrderEditSummary\n    __typename\n  }\n  currentTotalPrice: totalPrice {\n    ...Price\n    __typename\n  }\n  subtotal: subtotalBeforeDiscounts {\n    ...Price\n    __typename\n  }\n  totalShipping: totalDiscountedShipping {\n    ...Price\n    __typename\n  }\n  taxesIncluded\n  totalTax {\n    ...Price\n    __typename\n  }\n  totalTip {\n    ...Price\n    __typename\n  }\n  cashRoundingAdjustment {\n    ...Price\n    __typename\n  }\n  shippingLineGroups {\n    groupType\n    lineAmountAfterDiscounts {\n      ...Price\n      __typename\n    }\n    __typename\n  }\n  financialStatus\n  customerFulfillmentStatus\n  purchasingEntity @skip(if: $redacted) {\n    ... on PurchasingCompany {\n      ...PurchasingCompany\n      __typename\n    }\n    __typename\n  }\n  totalRefunded {\n    ...Price\n    __typename\n  }\n  refunds {\n    id\n    createdAt\n    __typename\n  }\n  paymentInformation {\n    paymentCollectionUrl @skip(if: $redacted)\n    ...OrderPaymentInformation\n    __typename\n  }\n  reorderPath\n  market {\n    ...OrderMarket\n    __typename\n  }\n  requiresShipping\n  totalDutiesSummary {\n    totalDuties {\n      amount\n      currencyCode\n      __typename\n    }\n    totalDutiesStatus\n    totalAdditionalFees {\n      amount\n      currencyCode\n      __typename\n    }\n    __typename\n  }\n  note @skip(if: $redacted)\n  checkoutToken @skip(if: $redacted)\n  paymentTermsTemplate @skip(if: $redacted) {\n    id\n    dueInDays\n    description\n    name\n    translatedName\n    __typename\n  }\n  customAttributes @skip(if: $redacted) {\n    key\n    value\n    __typename\n  }\n  orderReceiptMetafields @skip(if: $redacted) {\n    key\n    namespace\n    value\n    type\n    __typename\n  }\n  buyerContext @skip(if: $redacted) {\n    country\n    companyLocationId\n    __typename\n  }\n  __typename\n}\n\nfragment OrderTransaction on OrderTransaction {\n  id\n  processedAt\n  paymentIcon {\n    id\n    url\n    altText\n    __typename\n  }\n  paymentDetails {\n    __typename\n    ... on CardPaymentDetails {\n      last4\n      cardBrand\n      __typename\n    }\n    ... on CustomGiftCardPaymentDetails {\n      last4\n      __typename\n    }\n    ... on LocalPaymentMethodsPaymentDetails {\n      brand\n      __typename\n    }\n  }\n  transactionAmount {\n    presentmentMoney {\n      ...Price\n      __typename\n    }\n    __typename\n  }\n  giftCardDetails {\n    last4\n    balance {\n      ...Price\n      __typename\n    }\n    __typename\n  }\n  status\n  kind\n  transactionParentId\n  type\n  typeDetails {\n    name\n    message\n    __typename\n  }\n  emvDetails @include(if: $isPreAuth) {\n    accountType\n    applicationPreferredName\n    applicationIdentifier\n    paymentSource\n    authorizationCode\n    verificationMethod\n    transactionStatus\n    transactionOutcome\n    transactionHappenedAt\n    __typename\n  }\n  __typename\n}\n\nfragment Price on MoneyV2 {\n  amount\n  currencyCode\n  __typename\n}\n\nfragment Address on CustomerAddress {\n  id\n  address1\n  address2\n  firstName\n  lastName\n  provinceCode: zoneCode\n  city\n  zip\n  countryCodeV2: territoryCode\n  company\n  phone: phoneNumber\n  __typename\n}\n\nfragment Fulfillment on Fulfillment {\n  id\n  status\n  createdAt\n  estimatedDeliveryAt\n  trackingInformation @skip(if: $redacted) {\n    number\n    company\n    url\n    __typename\n  }\n  requiresShipping\n  fromPos\n  isPickedUp\n  fulfillmentLineItems(first: 20) {\n    nodes {\n      id\n      quantity\n      lineItem {\n        id\n        name\n        title\n        presentmentTitle\n        sku\n        group {\n          id\n          parentLineItemId\n          title\n          __typename\n        }\n        image {\n          id\n          url\n          altText\n          __typename\n        }\n        giftCard\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  onItsWay: events(\n    first: 1\n    query: \"status:in_transit\"\n    sortKey: HAPPENED_AT\n    reverse: true\n  ) {\n    edges {\n      node {\n        id\n        ...FulfillmentEvent\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  outForDelivery: events(\n    first: 1\n    query: \"status:out_for_delivery\"\n    sortKey: HAPPENED_AT\n    reverse: true\n  ) {\n    edges {\n      node {\n        id\n        ...FulfillmentEvent\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  delivered: events(\n    first: 1\n    query: \"status:delivered\"\n    sortKey: HAPPENED_AT\n    reverse: true\n  ) {\n    edges {\n      node {\n        id\n        ...FulfillmentEvent\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  service\n  __typename\n}\n\nfragment FulfillmentEvent on FulfillmentEvent {\n  id\n  status\n  happenedAt\n  __typename\n}\n\nfragment OrderEditSummary on OrderEditSummary {\n  latestHappenedAt\n  changes {\n    id\n    delta\n    handle\n    lineItem {\n      id\n      image {\n        id\n        altText\n        url\n        __typename\n      }\n      title\n      variantTitle\n      quantity\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PurchasingCompany on PurchasingCompany {\n  company {\n    id\n    name\n    externalId\n    __typename\n  }\n  contact {\n    id\n    __typename\n  }\n  location {\n    id\n    externalId\n    name\n    market {\n      id\n      webPresence {\n        id\n        rootUrls {\n          url\n          locale\n          __typename\n        }\n        subfolderSuffix\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OrderPaymentInformation on OrderPaymentInformation {\n  paymentStatus\n  totalPaidAmount {\n    ...Price\n    __typename\n  }\n  totalOutstandingAmount {\n    ...Price\n    __typename\n  }\n  paymentTerms {\n    id\n    paymentTermsType\n    overdue\n    nextDueAt\n    lastSchedule: paymentSchedules(first: 1, reverse: true) {\n      nodes {\n        id\n        dueAt\n        completed\n        totalBalance {\n          ...Price\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OrderMarket on Market {\n  id\n  handle\n  webPresence {\n    id\n    domain {\n      id\n      type\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment NonReturnableSummary on OrderReturnInformation {\n  nonReturnableSummary {\n    summaryMessage\n    nonReturnableReasons\n    __typename\n  }\n  __typename\n}\n\nfragment Returns on Order {\n  returns(first: 10, sortKey: CREATED_AT, reverse: true) {\n    nodes {\n      ...Return\n      reverseDeliveries(first: 10) @skip(if: $redacted) {\n        nodes {\n          id\n          deliverable {\n            ... on ReverseDeliveryShippingDeliverable {\n              label {\n                createdAt\n                publicFileUrl\n                __typename\n              }\n              tracking {\n                carrierName\n                trackingNumber\n                trackingUrl\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Return on Return {\n  id\n  closedAt\n  name\n  status\n  returnLineItemsCount {\n    count\n    __typename\n  }\n  timelineEvents {\n    id\n    title\n    subtitle\n    message\n    happenedAt\n    __typename\n  }\n  returnLineItems(first: 8) {\n    nodes {\n      ...ReturnLineItem\n      ...UnverifiedReturnLineItem\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    __typename\n  }\n  exchangeLineItems(first: 8) @skip(if: $skipExchangeLineItems) {\n    nodes {\n      id\n      quantity\n      title\n      variantTitle\n      image {\n        id\n        url\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReturnLineItem on ReturnLineItem {\n  id\n  quantity\n  lineItem {\n    id\n    image {\n      id\n      url\n      altText\n      __typename\n    }\n    title\n    name\n    groupTitle\n    group {\n      id\n      title\n      parentLineItemId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment UnverifiedReturnLineItem on UnverifiedReturnLineItem {\n  id\n  quantity\n  lineItem {\n    id\n    image {\n      id\n      url\n      altText\n      __typename\n    }\n    title\n    name\n    groupTitle\n    group {\n      id\n      title\n      parentLineItemId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VatInvoices on Order {\n  vatInvoices: taxInvoices {\n    invoiceNumber\n    createdAt\n    url\n    buyerTimeZone\n    __typename\n  }\n  __typename\n}"
        }

        headers = {
            "content-length": str(len(json.dumps(payload))),
            "sec-ch-ua-platform": "\"macOS\"",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "accept": "*/*",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "content-type": "application/json",
            "x-shopify-order-access-token": orderId,
            "sec-ch-ua-mobile": "?0",
            "origin": "https://shopify.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": response.url,
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i"
        }

        header_order = [
            "content-length",
            "sec-ch-ua-platform",
            "user-agent",
            "accept",
            "sec-ch-ua",
            "content-type",
            "x-shopify-order-access-token",
            "sec-ch-ua-mobile",
            "origin",
            "sec-fetch-site",
            "sec-fetch-mode",
            "sec-fetch-dest",
            "referer",
            "accept-encoding",
            "accept-language",
            "cookie",
            "priority"
        ]

        final_url = response.url.split("/orders")[0] + "/customer/api/unstable/graphql?operation=OrderDetails"

        tls.headers_order = header_order

        response = requests_go.post(final_url, headers=headers, json=payload, proxies=proxy, tls_config=tls)

        # print(json.dumps(response.json(), indent=4))

        return get_substring(response.text, '"customerFulfillmentStatus":"', '"')
        
    except Exception as e:
        if retry:
            return update_order_status(order_link, False)

        print(e)
        return "NA"

# Main

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

def handleValor(message):
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
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleCyber(message):
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
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleAlpine(message):
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
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleMake(message):
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

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleSwift(message):
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
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleRefract(message):
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
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleStellar(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        product = field.value
                    elif field_name == "site":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None
    
def handleTaranius(message):
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
                image = embed_dict['thumbnail'].get('url', '[No thumbnail URL]')
            
            # print(embed_dict)  # Debug output to inspect the embed structure

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None
    
def handleHahya(message):
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
                image = embed_dict['thumbnail'].get('url', '[No thumbnail URL]')

            # Extract order link from URL field
            if 'url' in embed_dict:
                orderLink = embed_dict['url']

            # print(embed_dict)  # Debug output to inspect the embed structure

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleNexar(message):
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
                image = embed_dict['thumbnail'].get('url', '[No thumbnail URL]')

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
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleNSB(message):
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
                image = embed_dict['thumbnail'].get('url', '[No thumbnail URL]')

            # Extract order link from URL field (if applicable)
            if 'url' in embed_dict:
                orderLink = embed_dict['url']

    # Check values and extract UID
    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleEnven(message):
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
                image = embed_dict['thumbnail'].get('url', '[No thumbnail URL]')

            # Extract order link from URL field
            if 'url' in embed_dict:
                orderLink = embed_dict['url']

            # print(embed_dict)  # Debug output to inspect the embed structure

    # Check values and extract UID
    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleBookie(message):
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
                image = embed_dict['thumbnail'].get('url', '[No thumbnail URL]')

            # print(embed_dict)  # Debug output to inspect the embed structure

    # Check values and extract UID
    values = [unitsWagered, image, unitsWon, account]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return ("", unitsWagered, unitsWon, account, "", "")
    else:
        return None
   
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
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def get_message_type(message):
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

def test():
    load_proxies()

    print(update_order_status(TEST_LINK))

async def fetch_messages_and_generate_csv():
    num_days = int(input("Enter the number of days to check messages: "))

    load_proxies()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=num_days)

    all_data = []

    for channel_id in ChannelToMonitor:
        channel = client.get_channel(channel_id)

        if channel:
            print(f"Found channel name: {channel.name}")
        else:
            print(f'Channel not found, fix json file: {channel_id}')

        last_message = None

        while True:
            messages = []
            async for message in channel.history(limit=100, before=last_message):
                if message.created_at < start_time:
                    break
                messages.append(message)

            if not messages:
                break

            for message in messages:
                try:
                    result = None
                    key = get_message_type(message)

                    if key == 1:
                        result = handleValor(message)
                    elif key == 2:
                        result = handleCyber(message)
                    elif key == 3:
                        result = handleAlpine(message)
                    elif key == 4:
                        result = handleMake(message)
                    elif key == 5:
                        result = handleSwift(message)
                    elif key == 6:
                        result = handleRefract(message)
                    elif key == 7:
                        result = handleStellar(message)
                    elif key == 8:
                        result = handleHahya(message)
                    elif key == 9:
                        result = handleNexar(message)
                    elif key == 10:
                        result = handleBookie(message)
                    elif key == 11:
                        result = handleNSB(message)
                    elif key == 12:
                        result = handleEnven(message)
                    elif key == 13:
                        result = handleTaranius(message)
                    elif key == 14:
                        result = handleShikari(message)

                    if result:
                        product, site, size, profile, order, orderLink = result

                        keywords = FILTER.lower().split()

                        combined_fields = " ".join(map(str, [product, site, size, profile, order, orderLink])).lower()

                        if not FILTER or any(keyword in combined_fields for keyword in keywords):
                            uid = None
                            uid, profile = extractUID(profile)
                            timestamp = message.created_at.isoformat()
                            channel_name = channel.name
                            all_data.append((timestamp, product, order, orderLink, site, size, profile, uid, channel_name))

                except Exception as e:
                    print(f"Error processing message {message.id}: {e}")

            last_message = messages[-1]

    print("Checking order statuses with 50 threads...")

    await client.close()

    # === Run update_order_status with ThreadPoolExecutor ===
    order_links = [row[3] for row in all_data]  # index 3 = orderLink
    statuses = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_index = {
            executor.submit(update_order_status, link): idx for idx, link in enumerate(order_links)
        }

        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                status = future.result()
            except Exception as e:
                print(f"Error getting status for index {idx}: {e}")
                status = "NA"
            statuses.append((idx, status))

    # === Merge statuses back into all_data in order ===
    status_map = dict(statuses)
    all_data_with_status = []
    for i, row in enumerate(all_data):
        status = status_map.get(i, "NA")
        all_data_with_status.append(row + (status,))  # Append status as final column

    # === Write to CSV ===
    with open("discord_messages.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Product", "Order Number", "Order Link", "Site", "Size", "Profile", "UID", "Channel Name", "Order Status"])
        writer.writerows(all_data_with_status)

    print("CSV saved with order statuses.")

if TEST_MODE:
    test()
else:
    @client.event
    async def on_ready():
        await fetch_messages_and_generate_csv()
        await client.close()

    client.run(TOKEN)
