from flask_dash import create_app
from flask_socketio import SocketIO
from flask import g
from flask_dash.db import get_engine
import pandas as pd
from flask_dash import queries

app = create_app()

sio = SocketIO(app, async_mode='eventlet')

i = 0
@sio.on("change_likes_debug", namespace='/flask')
def change_likes_debug(msg):
    print('here we are')
    print(msg)
    # bd
    global i
    i = i + 1
    sio.emit('change_heart', {'id': msg['id'], 'liked': i%2}, namespace='/flask' )


@sio.on("change_likes", namespace='/flask')
def change_likes(msg):
    db = get_engine()
    df_likes = pd.read_sql_query(
        queries.q_user_likes,
        con=db,
        params={'userid': msg["user_id"]}
    )

    if msg['_id'] in df_likes.article_id.to_list():
        liked = 0
        db.execute(queries.q_remove_like, {'userid': msg["user_id"], 'articleid': msg['_id']})
    else:
        liked = 1
        db.execute(queries.q_insert_like, {'userid': msg["user_id"], 'articleid': msg['_id']})
    sio.emit('change_heart', {'_id': msg['_id'], 'liked': liked}, namespace='/flask' )


if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=True)
    sio.run(app, host='0.0.0.0', debug=True)
    pass
