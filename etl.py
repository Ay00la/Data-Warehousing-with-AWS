import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_into_staging_tables(cur, conn):
    """Copy data from AWS s3 bucket to Redshift for staging by running all
    copy table queries defined in sql_queries.py
    :param cur: cursor
    :param conn: connection reference
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_into_tables(cur, conn):
    """Insert data from AWS Redshift staging table into Reshift relational
    database table by running all insert table queries defined in sql_queries.py
    :param cur: cursor
    :param conn: connection reference
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Driver main function.
    """
    # Read 'dwh.cfg' files
    try:
        config = configparser.ConfigParser()
        config.read('dwh.cfg')
    except Exception as e:
        print(e)

    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
    except Exception as e:
        print(e)

    try:
        load_into_staging_tables(cur, conn)
    except Exception as e:
        print(e)

    try:
        insert_into_tables(cur, conn)
    except Exception as e:
        print(e)

    # close connection and cursor
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
