import json
import psycopg2


class Connection:
    def __init__(self):
        with open('conf.json', 'r') as f:
            conf = json.load(f)
            self.dbname = conf['db']['dbname']
            self.username = conf['db']['username']
            self.password = conf['db']['password']
            self.host = conf['db']['host']
            self.port = conf['db']['port']
            self.connection = None
            self.cursor = None
    """
    Use this method if you wanna overwrite any db configs
    pass in a dict with items you wanna override
    - dbname
    - username
    - password
    - host
    - port (integer)
    """
    def override_configuration(self, **kwargs):
        if 'dbname' in kwargs:
            self.dbname = kwargs['dbname']
        if 'username' in kwargs:
            self.username = kwargs['username']
        if 'password' in kwargs:
            self.password = kwargs['password']
        if 'host' in kwargs:
            self.host = kwargs['host']
        if 'port' in kwargs:
            self.port = kwargs['port']

    """
    Call this method when you ready to connect to db
    """
    def connect(self):
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.username, password=self.password, host=self.host,
                                     port=self.port)
        self.cursor = self.conn.cursor()

    """
    return an instance of the connection
    """
    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def query_json(self, statement):
        self.cursor.execute("EXPLAIN (FORMAT JSON) " + statement)
        return self.cursor.fetchall()[0][0]
