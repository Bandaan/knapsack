# -*- coding: utf-8 -*-

"""
@Author: Daan van Dijk
@Date: 29/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

import unittest
from App.algoritme import Knapsack


class TestAlgoritme(unittest.TestCase):
    """"
    Het algoritme testen. Ik heb de tests eerst op papier uitgewerkt om te kijken
    wat de beste oplossing is. Deze staan in de projectsamenvatting.
    """

    def test_algoritme_1(self):
        algoritme = Knapsack()
        values = [540, 1100, 600, 2250, 2300, 1900]
        weight = [1, 2, 1, 3, 3, 1]

        result = []
        for i in algoritme.dynamic_min_max(values, weight, 5):
            result.append(values[i])

        self.assertEqual(result, [2250, 1100])

    def test_algoritme_2(self):
        algoritme = Knapsack()
        values = [240, 300, 1000, 900, 580]
        weight = [2, 3, 1, 4, 2]

        result = []
        for i in algoritme.dynamic_min_max(values, weight, 5):
            result.append(values[i])

        self.assertEqual(result, [300, 240])

    def test_algoritme_3(self):
        algoritme = Knapsack()
        values = [10, 12, 32, 29, 70, 63, 97, 110, 134]
        weight = [1, 1, 2, 2, 4, 6, 7, 7, 9]

        result = []
        for i in algoritme.dynamic_min_max(values, weight, 10):
            result.append(values[i])

        self.assertEqual(result, [63, 29, 12, 10])


if __name__ == "__main__":
    unittest.main()
