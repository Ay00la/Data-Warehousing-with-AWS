import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Drops tables in AWS Redshift by running all drop table queries
    defined in sql_queries.py
    :param cur: cursor
    :param conn: connection reference
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Creates tables in AWS Redshift by running all create table queries
    defined in sql_queries.py
    :param cur: cursor
    :param conn: connection reference
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Driver main function.
    """
    # Read 'dwh.cfg' files
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
    except Exception as e:
        print(e)

    try:
        drop_tables(conn, cur)
        print("Table dropped successfully!")
    except Exception as e:
        print(e)

    try:
        create_tables(conn, cur)
        print("Table created successfully!")
    except Exception as e:
        print(e)

    # close connection and cursor
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
