import Algoritme.database as db


class Knapsack:
    def __init__(self):
        self.database = db.Database()
        self.products = ''

    def get_products(self):
        self.products = self.database.first10_products()

        product_info = []

        for i in self.products:
            if any(char.isdigit() for char in str(i[5])):
                product_info.append({'pid': i[0], 'name': i[1], 'link': i[2], 'image': i[3], 'price': i[4], 'weight': i[5]})

        return product_info

    def dynamic_fruit(self, product_info, capacity):

        value, weight = [], []

        for i in product_info:
            value.append(float(i['price']) * 100)
            weight.append(round(int("".join([ch for ch in str(i['weight']) if ch.isdigit()])) / 10))

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

    def main(self):
        product_info = self.get_products()

        return_list = []
        for i in self.dynamic_fruit(product_info, 3000):
            return_list.append(product_info[i])

        return return_list


if __name__ == '__main__':
    Knapsack().main()
