# -*- coding: utf-8 -*-
"""
@Author: Daan van Dijk
@Date: 27/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

import asyncio
from database import Database as dbRequest
from ah_requests import get_product_pids
from ah_requests import get_product_info


class Product:
    def __init__(self):
        # Alle categorieën die de Albert Heijn heeft
        self.categories = ["salades-pizza-maaltijden", "vlees-kip-vis-vega", "kaas-vleeswaren-tapas", "zuivel-plantaardig-en-eieren", "bakkerij-en-banket", "ontbijtgranen-en-beleg",
                            "snoep-koek-chips-en-chocolade", "tussendoortjes", "frisdrank-sappen-koffie-thee", "wijn-en-bubbels", "bier-en-aperitieven", "pasta-rijst-en-wereldkeuken", "soepen-sauzen-kruiden-olie",
                            "sport-en-dieetvoeding", "diepvries", "drogisterij", "baby-en-kind", "huishouden", "huisdier", "koken-tafelen-vrije-tijd"]


        # connectie met database maken
        self.database = dbRequest()

        # legen lijsten initialiseren
        self.products = []
        self.product_pids = []
        self.tasks = []
        self.error_tasks = []

    # Main functie die alles bestuurt
    async def main(self):
        # Voor elke categorie en tabel maken
        self.database.setup(self.categories)

        # Alle product pids van de AH aanvragen
        await self.get_all_product_pids()

        # Voor elke product pid de volledige product informatie krijgen
        await self.start_tasks()

        # Voor elke error product pid de volledige product informatie krijgen
        await self.start_error_tasks()

        # Producten in database zetten
        await self.insert_in_database()

    # Functie om alle product pids te krijgen
    async def get_all_product_pids(self):

        # Voor elke categorie alle product pids krijgen
        for cat in self.categories:
            pids = await get_product_pids(cat)

            # Product pids aan de product_pids lijst toevoegen
            for j in pids:
                self.product_pids.append(j)

        # Alle dubbele pids eruit filteren
        new_list = []
        for i in self.product_pids:
            if i not in new_list:
                new_list.append(i)

        self.product_pids = new_list

    # Functie om alle tasks te maken en te starten
    async def start_tasks(self):

        # Voor elke product pid een task maken
        # Gekozen voor async aangezien het proces zo vele malen sneller verloopt
        index = 0

        # Per product pid een task maken
        for i in self.product_pids:
            with open('Proxies.txt') as proxy_file:
                file_content = proxy_file.read().splitlines()
                proxy = file_content[index]
                if proxy.count(':') == 1:
                    proxy = proxy + '==ip:port'
                elif proxy.count(':') == 3:
                    proxy = proxy + '==ip:port:user:pass'
                else:
                    proxy = 'None'

            # Proxy toevoegen aan task zodat je geen rate limit krijgt
            self.tasks.append(asyncio.create_task(get_product_info(i['pid'], i['categorie'], proxy)))
            await asyncio.sleep(1)
            index += 1

        # Alle tasks starten

        # Wachten tot elke task klaar is
        await asyncio.gather(*self.tasks)

        # Per task product informatie aan lijst toevoegen
        for i in self.tasks:
            if not i.result()[1]:
                self.products.append(i.result()[0])
            else:
                # Als product pid een error heeft dan aan error_tasks toevoegen
                self.error_tasks.append(asyncio.create_task(get_product_info(i.result()[1]['pid'], i.result()[1]['categorie'])))

    # Functie om alle producten die een error gaven nog een keer te starten
    async def start_error_tasks(self):

        # Wachten tot alle tasks klaar zijn
        await asyncio.gather(*self.error_tasks)

        # Error producten ook aan lijst toevoegen
        for i in self.error_tasks:
            self.products.append(i.result()[0])

    # Functie om producten aan database toe te voegen
    async def insert_in_database(self):
        # Producten in database toevoegen
        for product in self.products:
            await self.database.insert_product(product)
            await self.database.insert_categorie(product)


if __name__ == "__main__":
    # Het script starten
    asyncio.get_event_loop().run_until_complete(Product().main())
