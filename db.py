import psycopg2
import sys


class DB(object):
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def create_table(self):
        # cursor
        self.cur = self.conn.cursor()

        # delete the table if it exists
        # overwrite ?? TODO
        try:
            self.cur.execute("""
                (SELECT * FROM deva);
            """)
            rows = self.cur.fetchall()
            if rows:
                # delete table
                self.cur.execute("""DROP TABLE IF EXISTS deva""")
                self.cur.execute("""
                    CREATE TABLE DEVA
                       (ID INT PRIMARY KEY NOT NULL,
                       WORD TEXT NOT NULL,
                       TF REAL NOT NULL,
                       IDF REAL NOT NULL,
                       TFIDF REAL NOT NULL);
                   """)
                print 'Table created successfully!'
                self.conn.commit()
        except Exception, e:
            print e

    def insert_to_table(self):
        self.cur.execute("""
           INSERT INTO DEVA (ID, WORD, TF, IDF, TFIDF)
           VALUES (1, 'sita', 0.23313646, 0.2326226, 0.4323626);
           """)

        self.conn.commit()
        print 'Records added successfully!'

    def display_table(self):
        self.cur.execute("""
            (SELECT * FROM deva);
        """)
        rows = self.cur.fetchall()
        for row in rows:
            print row


if __name__ == '__main__':
    connection = None
    try:
        connection = psycopg2.connect(database='aakash', user='arunprasathshankar', password='', host='127.0.0.1',
                                      port='5432')
        db = DB(connection)
        db.create_table()
        db.insert_to_table()
        db.display_table()

    except psycopg2.DatabaseError, e:
        if connection:
            connection.rollback()
        print e
        sys.exit(1)

    finally:
        if connection:
            connection.close()
