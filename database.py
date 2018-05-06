import sqlite3
import html

class Database(object):
    conn = sqlite3.connect('slack_bot.db')
    
    def __init__(self):      
        c = Database.conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS employees (
            col0 text,
            col1 text,
            col2 text,
            col3 text,
            col4 integer,
            col5 float,
            col6 text,
            col7 text,
            col8 text
        )""")

        
    
    def insert_data(self):
        with Database.conn:
            c = Database.conn.cursor()
            c.execute("INSERT INTO employees VALUES ('David', 'Jenkins', 27000)")
            c.execute("INSERT INTO employees VALUES ('Jessica', 'Williams', 34000)")
            c.execute("INSERT INTO employees VALUES ('Alex', 'Smith', 45000)")
            c.execute("INSERT INTO employees VALUES ('Julian', 'Crosby', 34000)")
            c.execute("INSERT INTO employees VALUES ('John', 'Sawyer', 49000)")
            c.execute("INSERT INTO employees VALUES ('Martin', 'Thomas', 12000)")
            c.execute("INSERT INTO employees VALUES ('Rita', 'Thomas', 87000)")
            c.execute("INSERT INTO employees VALUES ('Paul', 'Carter', 65000)")
            c.execute("INSERT INTO employees VALUES ('Karl', 'Perry', 11500)")
            c.execute("INSERT INTO employees VALUES ('Alice', 'Jenkins', 78000)")
            c.close()
            Database.conn.commit()
        
    
    def fetch_data(self, query):
        try:       
            if query:
                with Database.conn:
                    c = Database.conn.cursor()
                    c.execute(query)
                    records = c.fetchall()
                    c.close()
                    return records
        except sqlite3.Error as e:
            return ('Database error : {}'.format(e))
        except Exception as e:
            return ('Exception in query : {}'.format(e))
    
    
if __name__ == '__main__':
    instance = Database()
    # instance.insert_data()
    print(instance.fetch_data("select * from employees where lastName='Jenkins'"))
    