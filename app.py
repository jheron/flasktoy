from flask import Flask
import psycopg2
import os
import socket
import time

connected = False
conn_error = ""

def connect(pwd):
    global conn_error, connected
    """ Connect to the PostgreSQL database server 
    """
    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="jheron")
        cur = conn.cursor()
        
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
       
        connected = True
    except (Exception, psycopg2.DatabaseError) as error:
        connected = False
        conn_error = error
    finally:
        if conn is not None:
            conn.close()


app = Flask(__name__)

@app.route("/")
def hello():
    global conn_error
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"  \
           "<p>Error: {error}</p>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(),error=conn_error)

@app.route('/health', methods=['GET'])
def get_tasks():
    global connected
    if connected:
        return "1",200,{'ContentType':'text/plain'}
    else:
        return "0",200,{'ContentType':'text/plain'}

if __name__ == "__main__":
#    time.sleep(90)
    try:
        password = os.environ['PASSWORD']
    except KeyError:
        password = "secret"

    connect(password)
    app.run(host='0.0.0.0', port=80)
