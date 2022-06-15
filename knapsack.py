import requests
import asyncio
import aiohttp


def get_product_pids(categorie):

    req = requests.get(f"https://www.ah.nl/zoeken/api/products/search?taxonomySlug={categorie}&size=1000")

    product_ids = []
    products = req.json()['cards']

    for i in range(len(products)):
        product_ids.append(products[i]['id'])

    if int(req.json()["page"]["totalElements"]) > 1000:
        elements = int(req.json()["page"]["totalElements"])

        links = [f"https://www.ah.nl/zoeken/api/products/search?page=1&taxonomySlug={categorie}&size=1000"]

        elements -= 1000
        index = 2
        while elements != 0:
            if elements >= 1000:
                links.append(f"https://www.ah.nl/zoeken/api/products/search?page={index}&taxonomySlug={categorie}&size=1000")
                elements -= 1000
                index += 1
            else:
                links.append(f"https://www.ah.nl/zoeken/api/products/search?page={index}&taxonomySlug={categorie}&size={elements}")
                elements = 0

        for endpoint in links:
            req = requests.get(endpoint)

            try:
                products = req.json()['cards']
            except Exception:
                pass

            for j in range(len(products)):
                if products[j]['id'] not in product_ids:
                    product_ids.append(products[j]['id'])

    return product_ids, categorie


async def get_product_info(pid):

    async with aiohttp.ClientSession() as session:
        req = await session.get(f'https://www.ah.nl/zoeken/api/products/product?webshopId={pid}')

        response = await req.json()

        product_info = {}

        for p in range(len(response['card']['meta']['nutritions'][0]['nutrients'])):
            product_info[response['card']['meta']['nutritions'][0]['nutrients'][p]['name']] = response['card']['meta']['nutritions'][0]['nutrients'][p]['value']

        product_info['product_name'] = response['card']['products'][0]['title']
        product_info['product_link'] = response['card']['products'][0]['link']
        product_info['product_price'] = response['card']['products'][0]['price']['now']
        product_info['product_weight'] = response['card']['products'][0]['price']['unitSize']


async def multiple_tasks(tasks):
    await asyncio.gather(*tasks, return_exceptions=True)


def get_data():

    categories = ["aardappel-groente-fruit", "salades-pizza-maaltijden", "vlees-kip-vis-vega", "kaas-vleeswaren-tapas", "zuivel-plantaardig-en-eieren", "bakkerij-en-banket", "ontbijtgranen-en-beleg",
                  "snoep-koek-chips-en-chocolade", "tussendoortjes", "frisdrank-sappen-koffie-thee", "wijn-en-bubbels", "bier-en-aperitieven", "pasta-rijst-en-wereldkeuken", "soepen-sauzen-kruiden-olie",
                  "sport-en-dieetvoeding", "diepvries", "drogisterij", "baby-en-kind", "huishouden", "huisdier", "koken-tafelen-vrije-tijd"]

    product_pids = []
    for cat in categories:
        pids = get_product_pids(cat)

        for j in pids:
            product_pids.append(j)

    tasks = []

    for i in product_pids:
        tasks.append(get_product_info(i))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(multiple_tasks(tasks))


if __name__ == "__main__":
    get_data()

