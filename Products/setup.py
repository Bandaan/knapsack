# -*- coding: utf-8 -*-
"""
@Author: Daan van Dijk
@Date: 27/06/2022
@Links: https://github.com/Bandaan/knapsack
"""


# Functie om alle tabellen te verwijderen
def delete_tables(cur, conn):

    # Kijken welke tabellen er allemaal in de database zitten
    cur.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='supermarkt';")

    # Alle tabellen die niet weg mogen eruit filteren
    tables = []
    for result in cur:
        if 'pg' in str(result[0]) or 'sql' in str(result[0]):
            pass
        else:
            tables.append(result[0])

    # Gefilterde tabellen verwijderen uit database
    for table in tables:
        cur.execute(f"DROP table {table} CASCADE;")

    # Definitief in database zetten
    conn.commit()
    return


# Functie om alle benodigde tabellen aan te maken
def create_tables(cur, conn, categories):

    # Product tabel aanmaken
    create_product(cur)

    # Categorieën tabellen aanmaken
    create_categories(cur, conn, categories)

    conn.commit()
    return


def create_product(cur):
    # Product tabel in database zetten
    cur.execute("CREATE TABLE Product (pid bigint NOT NULL,productName varchar(255),productLink varchar(255), productImage varchar(255), productPrice varchar(255), productWeight varchar(255),energie varchar(255),vet varchar(255),koolhydraten varchar(255),eiwitten varchar(255),zout varchar(255),voedingsvezel varchar(255), PRIMARY KEY (pid));")
    return


def create_categories(cur, conn, categories):

    # Categorieën tabel in database zetten
    cur.execute("CREATE TABLE categories (categoryId serial NOT NULL, categoryName varchar(255) NOT NULL,PRIMARY KEY (categoryId));")

    # Per categorie een apart nummer aanmaken en hier een nieuwe tabel mee maken
    for i in categories:
        insert_script = 'INSERT INTO categories (categoryName) VALUES (%s)'
        insert_value = (str(i).strip(),)

        # In de database zetten
        cur.execute(insert_script, insert_value)

    # Definitief in database zetten
    conn.commit()

    cur.execute("select * from categories")

    # Per categorie een nieuwe tabel maken
    lijst = []
    for i in cur:
        category = 'category_' + str(i[0]).strip()
        lijst.append(f'CREATE TABLE {category} (pid	bigint not null, categoryId	int, CONSTRAINT fk_product FOREIGN KEY(pid) REFERENCES Product(pid), CONSTRAINT fk_categories FOREIGN KEY(categoryId) REFERENCES categories(categoryId));')

    for i in lijst:
        cur.execute(i)

    # Definitief in database zetten
    conn.commit()
