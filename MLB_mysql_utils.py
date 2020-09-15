# -*- coding: utf-8 -*-
"""

Author: Daniel R. Ciarrocki, Copyright (c) 2020
License: MIT License


Description:
    Basic databasue utilities for the mysql database that holds all project 
    data.


Function List:
    get_connection
    create_tables
    delete_all_tables
    delete_table
    create_database
    delete_database

"""




### Run following command in mysql command line to enable mysql-client
#       ALTER USER 'yourusername'@'localhost' 
#       IDENTIFIED WITH mysql_native_password BY 'youpassword';




### Imports and Dependencies

import MySQLdb
from MLB_mysql_definitions import TABLES




### Main Functions

def get_connection(env_file_path = "dev_environment.env"):

    env_variables = parse_env_file(env_file_path)

    db = MySQLdb.connect(host = env_variables['HOST'],
                         port = int(env_variables['PORT']),
                         user = env_variables['USER'],
                         passwd = env_variables['PASSWORD'],
                         db = env_variables['DATABASE'])

    return db




def create_tables(tables = TABLES, table_list = TABLES.keys()):

    conn = get_connection()
    cursor = conn.cursor()

    for table_name in table_list:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except MySQLdb.connections.Error as err:
            print("Error:", err)
        else:
            print("OK")

    conn.commit()
    cursor.close()
    conn.close()




def delete_all_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS PAs")
    cursor.execute("DROP TABLE IF EXISTS Players")
    cursor.execute("DROP TABLE IF EXISTS Games")

    conn.commit()
    cursor.close()
    conn.close()




def delete_table(table_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS " + table_name)

    conn.commit()
    cursor.close()
    conn.close()




def create_database(env_file_path = "dev_environment.env", 
                    database_name = 'mlb1'):

    conn = get_connection(env_file_path)
    cursor = conn.cursor()

    try:
        print("Creating database", database_name, end=': ')
        cursor.execute("CREATE DATABASE " + database_name)
    except MySQLdb.connections.Error as err:
        print("Error:", err)
    else:
        print("OK")

    cursor.close()
    conn.close()




def delete_database(env_file_path = "dev_environment.env", 
                    database_name = 'mlb1'):

    conn = get_connection(env_file_path)
    cursor = conn.cursor()

    try:
        print("Dropping database", database_name, end=': ')
        cursor.execute("DROP DATABASE " + database_name)
    except MySQLdb.connections.Error as err:
        print("Error:", err)
    else:
        print("OK")

    cursor.close()
    conn.close()




### Helper Functions

def parse_env_file(file_path = "dev_environment.env"):

    env_variables = {}

    with open(file_path, 'r') as f:
        for row in f:
            if '=' in row:
                equals_index = row.index("=")
                if equals_index >= len(row) - 1: continue
                var_name = row[:equals_index]
                env_variables[var_name] = row[equals_index+1:].strip()

    return env_variables

