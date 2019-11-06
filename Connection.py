import json
import psycopg2


class Connection:
    def __init__(self):
        with open('conf.json', 'r') as f:
            conf = json.load(f)
            self.conn = psycopg2.connect(dbname=conf['db']['dbname'], user=conf['db']['username'],
                                         password=conf['db']['password'], host=conf['db']['host'],
                                         port=conf['db']['port'])
            self.cursor = self.conn.cursor()

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def query_json(self, statement):
        self.cursor.execute("EXPLAIN (FORMAT JSON) " + statement)
        return self.cursor.fetchall()[0][0][0]