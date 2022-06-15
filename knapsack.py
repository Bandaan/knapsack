import requests

result = True

categorien = []


def get_product_info(categorie):

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

    return product_ids


def get_data():

    categories = ["aardappel-groente-fruit", "salades-pizza-maaltijden", "vlees-kip-vis-vega", "kaas-vleeswaren-tapas", "zuivel-plantaardig-en-eieren", "bakkerij-en-banket", "ontbijtgranen-en-beleg",
                  "snoep-koek-chips-en-chocolade", "tussendoortjes", "frisdrank-sappen-koffie-thee", "wijn-en-bubbels", "bier-en-aperitieven", "pasta-rijst-en-wereldkeuken", "soepen-sauzen-kruiden-olie",
                  "sport-en-dieetvoeding", "diepvries", "drogisterij", "baby-en-kind", "huishouden", "huisdier", "koken-tafelen-vrije-tijd"]

    product_pids = []
    for cat in categories:
        pids = get_product_info(cat)

        for j in pids:
            product_pids.append(j)

    print(len(product_pids))



if __name__ == "__main__":
    get_data()

