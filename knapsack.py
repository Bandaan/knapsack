import requests
import asyncio
import aiohttp
import database
import json
import time
import os


class Product:
    def __init__(self):
        self.categories = ["aardappel-groente-fruit", "salades-pizza-maaltijden", "vlees-kip-vis-vega", "kaas-vleeswaren-tapas", "zuivel-plantaardig-en-eieren", "bakkerij-en-banket", "ontbijtgranen-en-beleg",
                            "snoep-koek-chips-en-chocolade", "tussendoortjes", "frisdrank-sappen-koffie-thee", "wijn-en-bubbels", "bier-en-aperitieven", "pasta-rijst-en-wereldkeuken", "soepen-sauzen-kruiden-olie",
                            "sport-en-dieetvoeding", "diepvries", "drogisterij", "baby-en-kind", "huishouden", "huisdier", "koken-tafelen-vrije-tijd"]

        self.categories = ["salades-pizza-maaltijden"]
        self.products = []
        self.product_pids = []
        self.tasks = []
        self.error_pids = []
        self.test = []

    async def main(self):

        for cat in self.categories:
            pids = await self.get_product_pids(cat)

            for j in pids:
                self.product_pids.append(j)

        self.product_pids = list(dict.fromkeys(self.product_pids))

        index = 0
        for i in self.product_pids:
            self.tasks.append(asyncio.create_task(self.get_product_info(i, index)))
            index += 1

        await asyncio.gather(*self.tasks)

        await db.commit()

    async def get_product_pids(self, categorie):

        req = requests.get(f"https://www.ah.nl/zoeken/api/products/search?taxonomySlug={categorie}&size=1000")

        product_ids = []
        products = req.json()['cards']

        for i in range(len(products)):
            if products[i]['id'] not in product_ids:
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

    async def get_product_info(self, pid, index):
        try:
            async with aiohttp.ClientSession() as session:
                error = 0

                while True:
                    try:
                        result = await session.get(f'https://www.ah.nl/zoeken/api/products/product?webshopId={pid}')
                    except Exception:
                        if error > 2:
                            self.error_pids.append(pid)
                            return
                        error += 1
                        continue
                    else:
                        break

                response = await result.json(content_type=None)

                product_info = {}

                try:
                    voedingsstoffen = len(response['card']['meta']['nutritions'][0]['nutrients'])
                except KeyError:
                    voedingsstoffen = 0

                for p in range(voedingsstoffen):
                    product_info[response['card']['meta']['nutritions'][0]['nutrients'][p]['name']] = response['card']['meta']['nutritions'][0]['nutrients'][p]['value']

                try:
                    product_info['product_name'] = response['card']['products'][0]['title']
                    product_info['product_link'] = response['card']['products'][0]['link']
                    product_info['product_price'] = response['card']['products'][0]['price']['now']
                    product_info['product_weight'] = response['card']['products'][0]['price']['unitSize']

                except KeyError:
                    product_info['product_name'] = 0
                    product_info['product_link'] = 0
                    product_info['product_price'] = 0
                    product_info['product_weight'] = 0

            product_info['product_pid'] = pid

            if not product_info.get("Energie"):
                product_info["Energie"] = 0
            if not product_info.get("Vet"):
                product_info["Vet"] = 0
            if not product_info.get("Koolhydraten"):
                product_info["Koolhydraten"] = 0
            if not product_info.get("Eiwitten"):
                product_info["Eiwitten"] = 0
            if not product_info.get("Zout"):
                product_info["Zout"] = 0
            if not product_info.get("Voedingsvezel"):
                product_info["Voedingsvezel"] = 0

            if "kg" in str(product_info.get("product_weight")):
                s_nums = "".join([ch for ch in str(product_info.get("product_weight")) if ch.isdigit()])
                product_info["product_weight"] = f"{int(s_nums) * 1000} g"

            if "stuk" in str(product_info.get("product_weight")):
                if response['card'].get("meta"):
                    try:
                        gewicht = response['card']['meta']['contents']['netContents'][0]

                    except Exception:
                        gewicht = 0
                        pass

                    s_nums = "".join([ch for ch in str(gewicht) if ch.isdigit()])
                    product_info["product_weight"] = f"{int(s_nums)} g"


            await db.insert_table(product_info)
            #self.products.append(product_info)
            await db.commit()

            return

        except asyncio.TimeoutError:
            self.error_pids.append(pid)
            print( {"results": f"timeout error on {pid}"})


if __name__ == "__main__":
    db = database.Database()
    db.main()
    asyncio.get_event_loop().run_until_complete(Product().main())