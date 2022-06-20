import ListingObjectExample
import numpy as np
import pandas as pd


def minimumCost(items: pd.DataFrame, capacity):

    v = items['buy_price']
    w = items['bcx']

    print(v[4])

    #print(v)
    #print(w)

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
    listing = ListingObjectExample.main()
    print(minimumCost(listing, 5))


if __name__ == '__main__':
    main()