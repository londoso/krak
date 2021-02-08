#!/usr/bin/python
import psycopg2
from load_db_config import config

def create_env():
    """ Copy CSV File Into PostgreSql Table """
    conn = None
    try:
        # Open Connection
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute('drop schema if exists repo cascade;')
        cur.execute('create schema if not exists repo;')
        #cur.execute('drop table if exists repo.indicador;')
        cur.execute('create table repo.indicador (PK SERIAL PRIMARY KEY, COUNTRYNAME varchar(80) not null, INDICATORNAME varchar(200) not null, YEAR int, VALUE numeric(100,50));')

        print('Environment repo-indicador Created')
       
        # Close Connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    create_env()