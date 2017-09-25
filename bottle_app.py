#!/usr/bin/env python3

import sqlite3
from bottle import default_app ,route, run, debug, template, request, static_file, error, redirect
import requests
import json

db_location = '/home/stuladha/mysite/todo.db' #for PythonAnywhere
#db_location = 'todo.db'  #for Local


@route('/')
def get_index():
    stream="beta"
    #return template('<b>Hello {{name}}</b>!', name=name)
    url = "http://drdelozier.pythonanywhere.com/stream/query/"
    payload = {
        'userid': 0,
        'city': 0,
        'state': 0,
        'lat': 0,
        'lon': 0,
        'temp': 0,
        'humidity': 0,
        'light': 0,
        'outdoors': 0,
    }
    response = requests.get(url + stream)
    #print(response.status_code)
    #print(response.url)
    #print(response.text)
    data = response.json()
    data = data['result']
    for key in payload.keys():
        data = [item for item in data if key in item]
    print(data)

    return template('make_dict_table.tpl', header=payload.keys(), rows=data)

@route('/stream/json')
def get_index_json():
    stream="beta"
    #return template('<b>Hello {{name}}</b>!', name=name)
    url = "http://drdelozier.pythonanywhere.com/stream/query/"
    payload = {
        'userid': 0,
        'city': 0,
        'state': 0,
        'lat': 0,
        'lon': 0,
        'temp': 0,
        'humidity': 0,
        'light': 0,
        'outdoors': 0,
    }
    response = requests.get(url + stream)
    #print(response.status_code)
    #print(response.url)
    #print(response.text)
    data = response.json()
    data = data['result']
    for key in payload.keys():
        data = [item for item in data if key in item]
    print(data)
    data['result'] = data
    return json.dumps(data)
    
@route('/todo', method = 'GET')
def todo_list():
    conn = sqlite3.connect(db_location) 
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows = result)
    return output

@route('/todo/closed', method = 'GET')
def closed_todo_list():
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
    result = c.fetchall()
    c.close()
    output = template('make_table_closed', rows = result)
    return output

@route('/new', method='GET')
def new_item():
    if request.GET.save:
        new = request.GET.task.strip()
        conn = sqlite3.connect(db_location)
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid

        conn.commit()
        c.close()
        redirect('/todo')
        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id
    else:
        return template('new_task.tpl')

@route('/edit/<no:int>', method='GET')
def edit_item(no):
    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()
        redirect('/todo')
    else:
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        c.execute("SELECT task, status FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)
    
@route('/delete/<no:int>', method='GET')
def delete_item(no):
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        c.execute("DELETE FROM todo WHERE id LIKE ?", (str(no)))
        conn.commit()
        redirect('/todo')

@route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    c.close()
    if not result:
        return 'This item number does not exist!'
    else:
        return 'Task: %s' % result[0]

@route('/help')
def help():
    return static_file('help.html', root='static')

@route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}

@route('/json')
def show_all_json():
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("SELECT * FROM todo")
    result = c.fetchall()
    c.close()

    if not result:
        return {'todo_count' : 0 ,'task': 'This item number does not exist!'}
    else:
        return {'todo_count' : len(result) ,'task': result}

@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

#PythonAnywhere
application = default_app()   

# Local
# debug(True)
# run(reloader = True) 
