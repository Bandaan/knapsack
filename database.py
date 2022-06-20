import psycopg2
import time
import os


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

    def main(self):
        self.delete_tables()
        self.create_table()

    def delete_tables(self):
        # Functie om alle tabellen te verwijderen

        # Kijken welke tabellen er allemaal in de database zitten
        self.cur.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='webshop';")

        # Alle tabellen die niet weg mogen eruit filteren
        tables = []
        for result in self.cur:
            if 'pg' in str(result[0]) or 'sql' in str(result[0]) or str(result[0]) in ["product"]:
                pass
            else:
                tables.append(result[0])

        # Gefilterde tabellen verwijderen uit database
        for table in tables:
            self.cur.execute(f"DROP table {table} CASCADE;")

        self.cur.execute("drop table product;")

        # Definitief in database zetten
        self.conn.commit()

        return

    def create_table(self):
        self.cur.execute("CREATE TABLE Product (pid bigint NOT NULL,productName varchar(255),productLink varchar(255),productPrice varchar(255), productWeight varchar(255),energie varchar(255),vet varchar(255),koolhydraten varchar(255),eiwitten varchar(255),zout varchar(255),voedingsvezel varchar(255), PRIMARY KEY (pid));")

        self.conn.commit()
        pass

    async def insert_table(self, product_info):

        insert_script = 'INSERT INTO Product (pid, productName, productLink, productPrice, productWeight, energie, vet, koolhydraten, eiwitten, zout, voedingsvezel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_value = (product_info['product_pid'], product_info['product_name'], product_info['product_link'], product_info['product_price'], product_info['product_weight'], product_info['Energie'], product_info['Vet'], product_info['Koolhydraten'], product_info['Eiwitten'], product_info['Zout'], product_info['Voedingsvezel'],)

        self.cur.execute(insert_script, insert_value)

    def first10_products(self):
        self.cur.execute("select * from product limit 10;")

        return self.cur.fetchall()

    async def commit(self):
        self.conn.commit()

