from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__) #inits flask app with name and enrypoint
sio = SocketIO(app, async_mode='eventlet') #inits socket io,  and uses eventlet as concurency server

colors = {
    'red':128,
    'green':128,
    'blue':128
}

links = {
    'home': {'href':'/', 'text':'Home'},
    'config':{'href':'/cfg', 'text':'Config'},
    'files':{'href':'/files','text':'File Browser'}
}

@app.route('/') #basic routes with variables as <type:var>
def index():
    return render_template("index.html", title="Index", colors=colors, links=links)

@app.route('/cfg')
def cfg():
    return render_template("base.html", page=links['config']['text'], links=links)

@app.route('/files')
def files():
    return render_template("base.html", page=links['files']['text'], links=links)

@app.route('/remote')
def remote():
    return render_template("remote.html", colors=colors, links=links)
"""
in perfect world commands, api, and data are 3 different namespaces
"""
@sio.on('colors', namespace='/flask') #namespace must start with /
def change_colors(msg):
    global colors
    colors[msg['color']] = msg['value'] #deconstructs json on the fly and rebuilds it as dict
    sio.emit('update_sliders', msg, namespace='/flask')
    sio.emit('square', colors, namespace='/flask')

@sio.on('main', namespace='/flask')
def screen(clk):
    sio.emit('main', clk, namespace='/flask')

if __name__=="__main__":
    sio.run(app, debug=True)