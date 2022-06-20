import database as db
import numpy as np
import pandas as pd
import ListingObjectExample

database = db.Database()

items = [('avocado', 2.2, -170), ('pomelo', 8, -1500), ('durian', 22, -1500), ('cucamelon', 0.26, -15), ('lychee', 0.4, -20), ('star apple', 1, -200)]


def get_products():
    products = database.first10_products()

    listing_dict = []

    for i in products:
        listing_dict.append({'weight': int("".join([ch for ch in str(i[4]) if ch.isdigit()])), 'price':i[3]})

    df = pd.DataFrame(listing_dict)
    return df.sort_values(by=['weight'],ascending = False).reset_index()

def minimumCost(items, capacity):

    #v = items[0]
    #w = items[1]

    v = items['price']
    w = items['weight']


    matrix = np.zeros((len(v) + 1, capacity + 1))
    matrix[0][1:] = float('inf')

    for i in range(1, len(v) + 1):
        for j in range(1, capacity + 1):

            if w[i - 1] > j:
                matrix[i][j] = matrix[i - 1][j]
            else:
                matrix[i][j] = min(matrix[i - 1][j], matrix[i - 1][j - w[i - 1]] + v[i - 1])

    chosen_items = []
    tmp = matrix

    while not np.all((tmp == 0)):
        chosen_item_index = np.where(tmp[:, len(tmp[0]) - 1] == min(tmp[:, len(tmp[0]) - 1]))[0][0] - 1

        chosen_items.append(items.iloc[chosen_item_index])
        tmp = tmp[:-len(tmp) + chosen_item_index + 1, :-w[chosen_item_index]]

    return chosen_items


def main():
    listing = get_products()


    #listing = ListingObjectExample.main()
    print(listing)

    print(minimumCost(listing, 1000))


if __name__ == '__main__':
    main()