import os
from flask import Flask, request, redirect, g, render_template, jsonify
import twilio.twiml
import sqlite3


DATABASE = 'database.db'
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    cur = g.db.execute('select * from projects order by id desc') 
    projects = [dict(id=row[0], title=row[1], desc=row[2], votes=[3]) for row in cur.fetchall()]
    return render_template('index.html', projects=projects)

@app.route('/list')
def list():
    cur = g.db.execute('select * from projects order by id desc') 
    projects = [dict(id=row[0], title=row[1], desc=row[2], votes=[3]) for row in cur.fetchall()]
    return jsonify(projects=projects)

app.route('/vote')
def vote():
    from_number = request.args.get('From', None)
    cur = g.db.execute('select * from numbers where num=?', from_number)
    # number exists
    if len(cur.fetch.all()) != 0:
        resp = twilio.twiml.Response()
        resp.sms('Thanks, but you already voted!') 
    else:
        try:
            ident = int(request.args.get('Body', ''))
            cur = g.db.execute('select * from projects')
            numProjects = cur.rowcount
            # valid id number
            if ident <=  numProjects:
                g.db.execute('update projects set vote=vote+1 where id=?', ident)
                # add phone number to db
                g.db.execute('insert into numbers (num) values (?)', from_number)
                g.db.commit()
                resp = twilio.twiml.Response()
                resp.sms('Thanks for the vote!') 
        except ValueError:
            resp = twilio.twiml.Response()
            resp.sms("That isn't a valid project id.") 

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
