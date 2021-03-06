# -*- coding: utf-8 -*-
"""
@Author: Daan van Dijk
@Date: 27/06/2022
@Links: https://github.com/Bandaan/knapsack
"""

import psycopg2
import time
import os
import Products.setup as initialize
import json


class Database:
    def __init__(self):
        # Connectie maken met de sql database

        # Uit lezen van config file
        try:
            with open('config.json') as file:
                data = json.loads(file.read())
                self.database_host = str(data["database_host"])
                self.database_name = str(data["database_name"])
                self.database_password = str(data["database_password"])
                self.database_port = int(data["database_port"])

        except Exception:
            self.database_host = "localhost"
            self.database_name = "supermarkt"
            self.database_password = ""
            self.database_port = "5432"

        try:
            self.conn = psycopg2.connect(
                host=self.database_host,
                dbname=self.database_name,
                user='postgres',
                password=self.database_password,
                port=self.database_port
            )
            self.cur = self.conn.cursor()

        # Error met het connecten van een van de databases
        except Exception as error:

            # De error laten zien aan de client
            print(f'Unable to connect to the database {error}')
            time.sleep(5)

            # Het programma stoppen
            os._exit(0)

    # Functie om database te organiseren
    def setup(self, categories):
        # Tabellen in de database verwijderen
        initialize.delete_tables(self.cur, self.conn)

        # Tabellen aan database toevoegen
        initialize.create_tables(self.cur, self.conn, categories)

    # Functie om producten toe te voegen aan de tabel
    async def insert_product(self, product_info):

        # Product aan tabel toevoegen
        insert_script = 'INSERT INTO Product (pid, productName, productLink, productImage, productPrice, productWeight, energie, vet, koolhydraten, eiwitten, zout, voedingsvezel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_value = (product_info['product_pid'], product_info['product_name'], product_info['product_link'], product_info['product_image'], product_info['product_price'], product_info['product_weight'], product_info['Energie'], product_info['Vet'], product_info['Koolhydraten'], product_info['Eiwitten'], product_info['Zout'], product_info['Voedingsvezel'],)

        try:
            self.cur.execute(insert_script, insert_value)
        except Exception:
            # Als er een error is dan product overslaan
            pass

        self.conn.commit()

    # Functie om product bij de juiste categorie toe te voegen
    async def insert_categorie(self, product_info):

        # Opvragen bij welk categoryID het product past
        self.cur.execute("SELECT categoryId FROM categories WHERE categoryName = %s", (str(product_info['categorie']).strip(),))
        number = str(self.cur.fetchone()[0])

        self.conn.commit()

        # Het product bij de juiste category plaatsen
        insert_script = f'INSERT INTO category_{number} (pid, categoryId) VALUES (%s, %s)'
        insert_value = (product_info['product_pid'], number,)

        # Product in database zetten
        self.cur.execute(insert_script, insert_value)
        self.conn.commit()

    # Functie om producten op te vragen
    def get_products(self, categorie):
        # Opvragen bij welk categoryID het product past
        self.cur.execute("SELECT categoryId FROM categories WHERE categoryName = %s", (str(categorie).strip(),))

        number = str(self.cur.fetchone()[0])

        self.conn.commit()

        self.cur.execute(f"SELECT * FROM product, category_{number} WHERE product.pid = category_{number}.pid")

        product_info = []

        for i in self.cur:
            if any(char.isdigit() for char in str(i[5])):
                if int("".join([ch for ch in str(i[5]) if ch.isdigit()])) == 0:
                    pass
                else:
                    product_info.append({'pid': i[0], 'name': i[1], 'link': i[2], 'image': i[3], 'price': i[4], 'weight': i[5], 'energie': i[6], 'vet': i[7], 'koolhydraten': i[8], 'eiwitten': i[9], 'zout': i[10], 'voedingsvezel': i[11]})

        return product_info
