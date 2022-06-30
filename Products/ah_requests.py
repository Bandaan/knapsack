# -*- coding: utf-8 -*-
"""
@Author: Daan van Dijk
@Date: 28/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

import requests
import aiohttp
import asyncio


# Functie om alle pids van de albert heijn te krijgen
async def get_product_pids(categorie):
    # Request met categorie naar AH maken
    req = requests.get(f"https://www.ah.nl/zoeken/api/products/search?taxonomySlug={categorie}&size=1000")

    # Product PIDS lijst maken
    product_ids = []
    products = req.json()['cards']

    # Product pids aan lijst toevoegen
    for i in range(len(products)):
        # Als dubbele pid is dan splitsen en allebei toevoegen
        if len(str(products[i]['id'])) > 6:
            product_ids.append({'pid': int(str(products[i]['id'])[:len(str(products[i]['id'])) // 2]), 'categorie': categorie})
            product_ids.append({'pid': int(str(products[i]['id'])[len(str(products[i]['id'])) // 2:]), 'categorie': categorie})
        else:
            product_ids.append({'pid': products[i]['id'], 'categorie': categorie})

    # Als de categorie meer dan 1000 producten heeft
    if int(req.json()["page"]["totalElements"]) > 1000:
        # Kijken hoeveel producten die heeft
        elements = int(req.json()["page"]["totalElements"])

        # Lijst met nieuwe links aanmaken
        links = [f"https://www.ah.nl/zoeken/api/products/search?page=1&taxonomySlug={categorie}&size=1000"]

        elements -= 1000
        index = 2
        # Per 1000 producten een nieuwe link toevoegen met een nieuwe index
        while elements != 0:
            if elements >= 1000:
                links.append(f"https://www.ah.nl/zoeken/api/products/search?page={index}&taxonomySlug={categorie}&size=1000")
                elements -= 1000
                index += 1
            else:
                links.append(f"https://www.ah.nl/zoeken/api/products/search?page={index}&taxonomySlug={categorie}&size={elements}")
                elements = 0

        # Per nieuwe link een request maken
        for endpoint in links:
            req = requests.get(endpoint)

            # Data is niet erg mooi georganiseerd, dus try except om error te voorkomen
            try:
                products = req.json()['cards']
            except Exception:
                # Als error is dan request overslaan
                pass

            # Product pids aan lijst toevoegen
            for j in range(len(products)):
                # Als dubbele pid is dan splitsen en allebei toevoegen
                if len(str(products[j]['id'])) > 6:
                    product_ids.append({'pid': int(str(products[j]['id'])[:len(str(products[j]['id'])) // 2]), 'categorie': categorie})
                    product_ids.append({'pid': int(str(products[j]['id'])[len(str(products[j]['id'])) // 2:]), 'categorie': categorie})
                else:
                    product_ids.append({'pid': products[j]['id'], 'categorie': categorie})

    # Product pids teruggeven
    return product_ids


# Functie om product informatie van een pid te krijgen
async def get_product_info(pid, categorie, proxy, database):

    # Dictionary aanmaken
    error_list = {}
    product_info = {}

    # Kijken of het een DC of een residential proxy is
    # Deze in de juiste format zetten
    try:
        if str(proxy).split('==')[1] == 'ip:port':
            ip = str(proxy.split(':')[0])
            port = str(proxy.split(':')[1].split('==')[0])
            proxies = f"http://{ip}:{port}"
        elif str(proxy).split('==')[1] == 'ip:port:user:pass':
            ip = str(proxy.split(':')[0])
            port = str(proxy.split(':')[1])
            user = str(proxy.split(':')[2])
            pw = str(proxy.split(':')[3].split('==')[0])
            proxies = f'http://{user}:{pw}@{ip}:{port}'
        else:
            proxies = None
    except Exception:
        # Als een proxy geen goeie format heeft dan geen proxy
        proxies = None

    # Try except, want data is erg onbetrouwbaar
    try:
        # Aiohttp sessie aanmaken
        async with aiohttp.ClientSession() as session:
            # error index aan 0 stellen
            error = 0
            while True:
                # Als error index groter dan 2 is dan stoppen en error teruggeven
                if error > 2:
                    error_list = {'pid': pid, 'categorie': categorie}
                    return product_info, error_list

                # Request met juiste pid naar AH maken
                try:
                    result = await session.get(f'https://www.ah.nl/zoeken/api/products/product?webshopId={pid}', proxy=proxies)
                except Exception:
                    # Error index + 1 en opnieuw beginnen
                    error += 1
                    continue
                else:
                    print(result.status)
                    # Als de status goed is uit de loop
                    if result.status == 200:
                        break
                    else:
                        # Zo niet error index + 1 en opnieuw
                        error += 1
                        continue

            # Wachten tot de request klaar is
            response = await result.json(content_type=None)

            # Er wordt gebruik gemaakt van erg veel try except, dit is niet de beste methode
            # Maar de data is erg slordig waardoor er geen andere optie is

            # Als een product de informatie heeft dan die toevoegen aan de dict product info
            try:
                voedingsstoffen = len(response['card']['meta']['nutritions'][0]['nutrients'])
            except KeyError:
                voedingsstoffen = 0

            # voedingsstoffen aan product info toevoegen
            for p in range(voedingsstoffen):
                product_info[response['card']['meta']['nutritions'][0]['nutrients'][p]['name']] = response['card']['meta']['nutritions'][0]['nutrients'][p]['value']

            try:
                product_info['product_image'] = response['card']['products'][0]['images'][3]['url']
            except Exception:
                product_info['product_image'] = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Albert_Heijn_Logo.svg'

            # Naam, link, prijs en gewicht toevoegen aan product info
            try:
                product_info['product_name'] = response['card']['products'][0]['title']
                product_info['product_link'] = response['card']['products'][0]['link']
                product_info['product_price'] = response['card']['products'][0]['price']['now']
                product_info['product_weight'] = response['card']['products'][0]['price']['unitSize']

            except KeyError:
                # Als error dan alles aan 0 vaststellen
                product_info['product_name'] = 0
                product_info['product_link'] = 0
                product_info['product_price'] = 0
                product_info['product_weight'] = 0

        # Pid en categorie toevoegen aan product info
        product_info['product_pid'] = pid
        product_info['categorie'] = categorie

        # Als een product niet alle voedingsstoffen heeft dan vast stellen aan 0
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

        # Als product niet de juiste eenheid heeft dan deze omrekenen en veranderen
        if "x" in str(product_info.get("product_weight")):
            if "kg" in str(product_info.get("product_weight")):
                aantal = int(str(product_info.get("product_weight")).split("x")[0].strip())
                gewicht = "".join([ch for ch in str(product_info.get("product_weight")).split("x")[1] if ch.isdigit()])
                product_info["product_weight"] = f"{aantal * gewicht * 1000} g"
            elif "g" in str(product_info.get("product_weight")):
                aantal = int(str(product_info.get("product_weight")).split("x")[0].strip())
                gewicht = "".join([ch for ch in str(product_info.get("product_weight")).split("x")[1] if ch.isdigit()])
                product_info["product_weight"] = f"{int(aantal) * int(gewicht)} g"
        # Als product niet de juiste eenheid heeft dan deze omrekenen en veranderen
        if "kg" in str(product_info.get("product_weight")):
            s_nums = "".join([ch for ch in str(product_info.get("product_weight")) if ch.isdigit()])
            product_info["product_weight"] = f"{int(s_nums) * 1000} g"

        # Als product niet de juiste eenheid heeft dan deze omrekenen en veranderen
        if "stuk" in str(product_info.get("product_weight")) or "per" in str(product_info.get("product_weight")):
            if response['card'].get("meta"):
                try:
                    gewicht = response['card']['meta']['contents']['netContents'][0]

                except Exception:
                    gewicht = 0
                    pass

                s_nums = "".join([ch for ch in str(gewicht) if ch.isdigit()])
                product_info["product_weight"] = f"{int(s_nums)} g"

    except asyncio.TimeoutError:
        # Error teruggeven
        error_list = {'pid': pid, 'categorie': categorie}
        return product_info, error_list

    await database.insert_product(product_info)
    await database.insert_categorie(product_info)

    # Product informatie en eventuele error teruggeven
    return product_info, error_list
