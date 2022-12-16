from sqlalchemy import create_engine

query1 = \
'''CREATE TABLE USERS (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);'''


query3 = \
'''ALTER TABLE articles  ADD UNIQUE (_id);'''

query2 = \
'''CREATE TABLE ua_inter (id integer REFERENCES users, article_id TEXT REFERENCES articles (_id));'''



def create_tab_users():
    engine = create_engine('postgresql://flaskdbusr:flaskdbpw@127.0.0.1:5432/flaskdb')
    engine.connect()
    engine.execute(query1)

    engine.dispose()


def create_tab_users_likes():
    engine = create_engine('postgresql://flaskdbusr:flaskdbpw@127.0.0.1:5432/flaskdb')
    engine.connect()
    engine.execute(query3)
    engine.execute(query2)

    engine.dispose()


if __name__ == '__main__':
    create_tab_users()
    create_tab_users_likes()
    pass
