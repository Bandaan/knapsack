# -*- coding: utf-8 -*-

"""
@Author: Daan van Dijk
@Date: 29/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

import Products.database as db


class Knapsack:
    def __init__(self):

        # Constructor van database
        self.database = db.Database()
        self.products = ''

    # Functie met het algoritme om beste producten te berekenen
    def dynamic_min_max(self, values, weights, capacity):

        # Value, gewicht en capaciteit gelijk stellen aan parameters
        value, weight = values, weights
        capacity = capacity

        # Lengte van de lijst
        n = len(value)

        # 2 Dimensionale matrix maken van de lengte van de capaciteit en lengte van gewichten
        matrix = [[0 for x in range(capacity + 1)] for x in range(n + 1)]

        # Alle elementen van de eerste rij gelijk stellen aan oneindig
        for i in range(1, len(matrix[0])):
            matrix[0][i] = float('inf')

        # Hele matrix afgaan om te kijken wat de ideale producten zijn
        for i in range(1, len(value) + 1):
            for j in range(1, capacity + 1):

                # Als het gewicht van de bovenste rij groter is dan het huidige dan omwisselen
                if weight[i - 1] > j:
                    matrix[i][j] = matrix[i - 1][j]
                else:
                    # Kijken wat de kleinste prijs is bij het maximale gewicht
                    matrix[i][j] = min(matrix[i - 1][j], matrix[i - 1][j - weight[i - 1]] + value[i - 1])

        print(matrix)
        res = matrix[n][capacity]

        w = capacity
        index = []

        # De terug weg berekenen om te kijken welke producten gekozen zijn
        for i in range(n, 0, -1):
            if res <= 0:
                # Als elke element 0 is dan is de berekening klaar
                break

            # laatste element in de matrix gelijk aan element in rij erboven
            if res == matrix[i - 1][w]:
                continue
            else:
                # Product gevonden en toevoegen aan lijst
                index.append(i - 1)

                # Laatste element veranderen naar een rij naar boven
                res = res - value[i - 1]
                w = w - weight[i - 1]

        # Alle indexen van product terug geven
        return index

    # Functie om aankom dieet te berekenen
    def aankomen(self, product_info):
        # Lege lijsten van gewicht en values
        values, weights = [], []

        # (Prijs / gewicht) en eiwit gewicht toevoegen
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append(int("".join([ch for ch in str(i['eiwitten']) if ch.isdigit()])) * 10)

        # Resultaat van algoritme
        result_eiwitten = self.dynamic_min_max(values, weights, 500)

        # Lege lijsten van gewicht en values
        values, weights = [], []

        # (Prijs / gewicht) en vet gewicht toevoegen
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append(int("".join([ch for ch in str(i['vet']) if ch.isdigit()])) * 10)

        # Resultaat van algoritme
        result_vet = self.dynamic_min_max(values, weights, 500)

        # Lege lijsten van gewicht en values
        values, weights = [], []

        # (Prijs / gewicht) en vet + eiwit gewicht toevoegen
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append((int("".join([ch for ch in str(i['vet']) if ch.isdigit()])) + int("".join([ch for ch in str(i['eiwitten']) if ch.isdigit()]))) * 10)

        # Resultaat van algoritme
        result_gemengd = self.dynamic_min_max(values, weights, 500)

        # Producten berekenen met algoritme
        return list(set(result_eiwitten + result_vet + result_gemengd))

    # Functie om normaal dieet te berekenen
    def normaal(self, product_info):
        # Lege lijsten van gewicht en values
        values, weights = [], []

        # Prijs en gewicht van product toevoegen
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append(int("".join([ch for ch in str(i['weight']) if ch.isdigit()])) * 10)

        # Producten berekenen met algoritme
        return self.dynamic_min_max(values, weights, 1000)

    # Functie om afval dieet te berekenen
    def afvallen(self, product_info):
        # Lege lijsten van gewicht en values
        values, weights = [], []

        # Prijs en gewicht koolhydraten toevoegen
        for i in product_info:
            values.append(int(float(i['price']) * 10))
            weights.append(int("".join([ch for ch in str(i['koolhydraten']) if ch.isdigit()])) * 10)

        # Producten berekenen met algoritme
        return self.dynamic_min_max(values, weights, 5000)

    # Functie die API aanroept om beste producten te krijgen
    # Deze functie is het regelpunt van de class
    def main(self, massa, categorie, dieet):

        # Lege lijsten maken voor return lijst en producten
        products = []
        return_list = []

        # Producten krijgen met de meegegeven categorie
        product_info = self.database.get_products(categorie)

        # Als client afvallen of cut als dieet heeft gekozen
        if 'afvallen' in str(dieet) or 'cut' in str(dieet):
            # Bij het dieet afvallen horen producten met veel koolhydraten
            for i in product_info:
                # Als een product geen koolhydraten bevat niet aan product lijst toevoegen
                if int("".join([ch for ch in str(i['koolhydraten']) if ch.isdigit()])) != 0:
                    products.append(i)

            # Functie aanroepen die het verder berekent en de beste producten terug geeft
            # Producten worden aan return lijst toegevoegd
            for j in self.afvallen(products):
                return_list.append(products[j])

        # Als client aankomen of bulk als dieet heeft gekozen
        elif 'aankomen' in str(dieet) or 'bulk' in str(dieet):
            # Bij het dieet aankomen horen producten met veel eiwitten en vetten
            for i in product_info:
                # Als een product geen vetten of eiwitten bevat niet aan product lijst toevoegen
                if int("".join([ch for ch in str(i['eiwitten']) if ch.isdigit()])) != 0 or int("".join([ch for ch in str(i['vet']) if ch.isdigit()])) != 0:
                    products.append(i)

            # Functie aanroepen die het verder berekent en de beste producten terug geeft
            # Producten worden aan return lijst toegevoegd
            for j in self.aankomen(products):
                return_list.append(products[j])

        # Als client niks heeft gekozen
        else:
            # Bij dit dieet wordt producten gekozen waar je maximale massa hebt en minimale prijs
            # Functie aanroepen die het verder berekent en de beste producten terug geeft
            # Producten worden aan return lijst toegevoegd
            for j in self.normaal(product_info):
                return_list.append(product_info[j])

        # Return lijst met producten terug geven
        return return_list
