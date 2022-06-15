import psycopg2
import time
import os


class Database:
    def __init__(self):
        try:
            # Connectie maken met de sql database
            self.conn = psycopg2.connect(
                host='localhost',
                dbname='webshop',
                user='postgres',
                password='Johidagamuk.',
                port='5432'
            )
            self.cur = self.conn.cursor()

        # Error met het connecten van een van de databases
        except Exception as error:

            # De error laten zien aan de client
            print(f'%sUnable to connect to the database {error}%s' % (fg(196), attr(0)))
            time.sleep(5)

            # Het programma stoppen
            os._exit(0)

    def main(self):
        pass

    def delete_tables(self):
        # Functie om alle tabellen te verwijderen

        # Kijken welke tabellen er allemaal in de database zitten
        self.cur.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='webshop';")

        # Alle tabellen die niet weg mogen eruit filteren
        tables = []
        for result in self.cur:
            if 'pg' in str(result[0]) or 'sql' in str(result[0]) or str(result[0]) in []:
                pass
            else:
                tables.append(result[0])

        # Gefilterde tabellen verwijderen uit database
        for table in tables:
            self.cur.execute(f"DROP table {table} CASCADE;")

        # Definitief in database zetten
        self.conn.commit()

        return


    def create_table(self):
        pass
