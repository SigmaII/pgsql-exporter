import psycopg2
import json
import os
from time import sleep
from datetime import datetime, timezone

DBNAME = os.environ['DBNAME']
USER = os.environ['USER']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
PASSWD = os.environ['PASSWD']
SCRAPING = (int)(os.environ['SCRAPING'])

def get_active_connections(cur):
    try:
        cur.execute(f"SELECT count(*) AS active_connections FROM pg_stat_activity WHERE datname='{DBNAME}'")
        rows = cur.fetchall()
        print("[INFO] GET ACTIVE CONN",rows)
        active_connections = rows[0][0]
        return active_connections
    except psycopg2.Error as e:
        print("Error executing SELECT statement:", e)
        return 0

def get_cache_hit(cur):
    try:
        cur.execute("SELECT sum(blks_hit) / nullif(sum(blks_hit + blks_read),0) * 100 AS cache_hit_percent FROM pg_stat_database")
        rows = cur.fetchall()
        print("[INFO] GET CACHE HIT]",rows)
        cache_hit = rows[0][0]
        return cache_hit
    except psycopg2.Error as e:
        print("Error executing SELECT statement:", e)
        return 0
    
def get_db_size(cur):
    try:
        cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
        rows = cur.fetchall()
        print("[INFO] GET DB SIZE",rows)
        db_size = rows[0][0]
        return db_size
    except psycopg2.Error as e:
        print("[ERROR] Error executing SELECT statement:", e)
        return 0

def connection_db():
    try:
        conn = psycopg2.connect(f"dbname='{DBNAME}' user='{USER}' host='{HOST}' port='{PORT}' password='{PASSWD}'")
        return conn
    except Exception as e:
        print("[ERROR] DB connection failed:", e)
        return 0

def run_exporter():
    while(True):
        cur = connection_db().cursor()
        output = {
            "active_connections": get_active_connections(cur),
            "cache_hit": get_cache_hit(cur),
            "db_size": get_db_size(cur)
            }
        
        with open('output.json', 'w') as f:
            f.write(json.dumps(output, indent=4, sort_keys=True, default=str))
            f.close()
        cur.close()
        connection_db().close()
        sleep(SCRAPING)
