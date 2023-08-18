from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
import psycopg2
import os
import requests as make_request


from forums import LoginForm, SearchForm, AddRocket


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lmao'
bootstrap = Bootstrap(app)

#app.config.from_pyfile('settings.py')
os.environ["FLASK_DEBUG"]="1"
os.environ["WERKZEUG_DEBUG_PIN"]="off"

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='missile_silo',
                            user='silo_admin',
                            password='nebula')
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/launch', methods=['GET', 'POST'])
def launch():
    return render_template('launch.html')

@app.route('/forumtest/', methods=['GET', 'POST'])
def forumtest():
    form = LoginForm()
    if form.validate_on_submit():
        return 'wow. Thank you {}'.format(form.username.data)


    return render_template('forum.html', form=form)

@app.route('/display/', methods=['GET'])
def display():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM rockets')
    rockets = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('display.html', rockets=rockets)

@app.route('/api/', methods=['POST'])
def api():
    #Instead of a POST request, we could do a GET request with specific queries. It would make it a lot easier
    if request.method == 'POST':
        command = request.form.get('command')
        conn = get_db_connection()
        cur = conn.cursor()
        #Failing below. Attempting to execute blank queries???
        cur.execute(command)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    
@app.route('/api2/', methods=['GET'])
def api2():
    #Instead of a POST request, we could do a GET request with specific queries. It would make it a lot easier
    if request.method == 'GET':
        command = request.args.get('command')
        querytype = request.args.get('type')
        if command != 'None':
            if querytype == 'SELECT':
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(command)
                #Result stored as a list of tuples
                result = cur.fetchall()
                cur.close()
                conn.close()
                return result   
            elif querytype == 'INSERT':
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(command)
                conn.commit()
                cur.close()
                conn.close()
                return '1'

 

@app.route('/search/', methods=['GET', 'POST'])
def search():

    form = SearchForm()
    result = [tuple()]

    #Use a csrf token to allow validation on submit
    if form.validate_on_submit():

        #Maybe to get SQLI command injection to work, we can have this send a premade command to a "postgres api" that we can also just send direct commands to :p
        #query = {'command':'SELECT * FROM rockets WHERE id = {}'.format(form.query.data)}
        #res = make_requests.post('http://localhost:5000/api')
        #result = 'res.text'

        #Need error handling when ID doesn't exist
        query = {'command':'SELECT * FROM rockets WHERE ID = {}'.format(form.query.data),'type':'SELECT'}
        res = make_request.get('http://localhost:5000/api2', params=query)

        #I have no idea what converting to json does, but it will break if its not here
        output = res.json()

        #If there is a valid query, then we recieve the output [[1, laksjdas, alskdjaklsd]]
        #If the query is empty, then we get [].
        #It fails because the empty is only a single list, not a list of tuples. We can possibly check for an empty list and have result equal something else if its empty
        if output: 
            result = output
        #Currently all counting as one thing. Need to store as list since thats what wtforms seems to use

        

        

    #It's rendering the result text, but its not updating it with the above thing        
    return render_template('search.html', form=form, result=result )

@app.route('/addrocket', methods=['GET', 'POST'])
def addrocket():
    
    form = AddRocket()
    if form.validate_on_submit():
        current_time = datetime.now()
        query = {'command':'INSERT INTO rockets(launch_time,destination,comments,active) VALUES(\'{}\',\'{}\',\'{}\',true)'.format(current_time,form.destination.data,form.comments.data),'type':'INSERT'}
        res = make_request.get('http://localhost:5000/api2', params=query)
        #Probably good to do some confirmation stuff but not needed for functionality
        # I give up on flash 
        #flash('Fired missile', 'info')
        return redirect(request.path)
    return render_template('addrocket.html', form=form)
    

        
@app.route('/rockets', methods=['GET'])
def rockets():
        query = {'command':'SELECT * FROM rockets','type':'SELECT'}
        res = make_request.get('http://localhost:5000/api2', params=query)
        output = res.json()
        return render_template('rockets.html', rockets=output)
# Could do something like for rocket in rockets in the html page if I wanted to do something that showed all rockets
# Need to test and see if the api2 endpoint gives [[],[]] (Multiple tuples) if we do a SELECT * FROM rockets or something of the sort