# -*- coding: utf-8 -*-
"""
@Author: Daan van Dijk
@Date: 29/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

import Products.database as db


class Knapsack:
    def __init__(self):
        self.database = db.Database()
        self.products = ''

    def dynamic_min_max(self, values, weights, capacity):

        value, weight = values, weights
        capacity = capacity // 10

        n = len(value)
        matrix = [[0 for x in range(capacity + 1)] for x in range(n + 1)]

        for i in range(1, len(matrix[0])):
            matrix[0][i] = float('inf')

        for i in range(1, len(value) + 1):
            for j in range(1, capacity + 1):

                if weight[i - 1] > j:
                    matrix[i][j] = matrix[i - 1][j]
                else:
                    matrix[i][j] = min(matrix[i - 1][j], matrix[i - 1][j - weight[i - 1]] + value[i - 1])

        res = matrix[n][capacity]

        w = capacity
        index = []
        for i in range(n, 0, -1):
            if res <= 0:
                break

            if res == matrix[i - 1][w]:
                continue
            else:
                index.append(i - 1)

                res = res - value[i - 1]
                w = w - weight[i - 1]

        return index

    def aankomen(self, product_info):

        values, weights = [], []
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append(int("".join([ch for ch in str(i['eiwitten']) if ch.isdigit()])) * 10)

        result_eiwitten = self.dynamic_min_max(values, weights, 1000)

        values, weights = [], []
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append(int("".join([ch for ch in str(i['vet']) if ch.isdigit()])) * 10)

        result_vet = self.dynamic_min_max(values, weights, 1000)

        values, weights = [], []
        for i in product_info:
            values.append(int(float(i['price']) * 10) / int("".join([ch for ch in str(i['weight']) if ch.isdigit()])))
            weights.append((int("".join([ch for ch in str(i['vet']) if ch.isdigit()])) + int("".join([ch for ch in str(i['eiwitten']) if ch.isdigit()]))) * 10)

        result_gemengd = self.dynamic_min_max(values, weights, 1000)

        return list(set(result_eiwitten + result_vet + result_gemengd))

    def normaal(self, product_info):

        values, weights = [], []
        for i in product_info:
            values.append(int(float(i['price']) * 10))
            weights.append(int("".join([ch for ch in str(i['weight']) if ch.isdigit()])) * 10)

        return self.dynamic_min_max(values, weights, 1000)

    def afvallen(self, product_info):

        values, weights = [], []
        for i in product_info:
            values.append(int(float(i['price']) * 10))
            weights.append(int("".join([ch for ch in str(i['koolhydraten']) if ch.isdigit()])) * 10)

        return self.dynamic_min_max(values, weights, 1000)

    def main(self, massa, categorie, dieet):
        products = []
        return_list = []

        product_info = self.database.get_products(categorie)

        if 'afvallen' in str(dieet):
            for i in product_info:
                if int("".join([ch for ch in str(i['koolhydraten']) if ch.isdigit()])) != 0:
                    products.append(i)

            for j in self.afvallen(products):
                return_list.append(products[j])

        elif 'aankomen' in str(dieet):
            for i in product_info:
                if int("".join([ch for ch in str(i['eiwitten']) if ch.isdigit()])) != 0 or int("".join([ch for ch in str(i['vet']) if ch.isdigit()])) != 0:
                    products.append(i)

            for j in self.aankomen(products):
                return_list.append(products[j])

        else:
            for j in self.normaal(product_info):
                return_list.append(product_info[j])

        return return_list
