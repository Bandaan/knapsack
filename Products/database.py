import psycopg2
import time
import os
import setup as initialize


class Database:
    def __init__(self):
        try:
            # Connectie maken met de sql database
            self.conn = psycopg2.connect(
                host='localhost',
                dbname='supermarkt',
                user='postgres',
                password='AjaxDaan23@',
                port='5432'
            )
            self.cur = self.conn.cursor()

        # Error met het connecten van een van de databases
        except Exception as error:

            # De error laten zien aan de client
            print(f'Unable to connect to the database {error}')
            time.sleep(5)

            # Het programma stoppen
            os._exit(0)

    def setup(self, categories):
        initialize.delete_tables(self.cur, self.conn)
        initialize.create_tables(self.cur, self.conn, categories)

    async def push_products(self, products):

        for product in products:
            await self.insert_product(product)
            await self.insert_categorie(product)

        self.conn.commit()

    async def insert_product(self, product_info):

        insert_script = 'INSERT INTO Product (pid, productName, productLink, productImage, productPrice, productWeight, energie, vet, koolhydraten, eiwitten, zout, voedingsvezel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_value = (product_info['product_pid'], product_info['product_name'], product_info['product_link'], product_info['product_image'], product_info['product_price'], product_info['product_weight'], product_info['Energie'], product_info['Vet'], product_info['Koolhydraten'], product_info['Eiwitten'], product_info['Zout'], product_info['Voedingsvezel'],)

        self.cur.execute(insert_script, insert_value)

    async def insert_categorie(self, product_info):

        self.cur.execute("SELECT categoryId FROM categories WHERE categoryName = %s", (str(product_info['categorie']).strip(),))
        number = str(self.cur.fetchone()[0])

        insert_script = f'INSERT INTO category_{number} (pid, categoryId) VALUES (%s, %s)'
        insert_value = (product_info['product_pid'], number,)

        # Product in database zetten
        self.cur.execute(insert_script, insert_value)

    def get_products(self):
        self.cur.execute("select * from product limit 100;")

        return self.cur.fetchall()

    async def commit(self):
        self.conn.commit()