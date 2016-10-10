#!/usr/bin/python

from bottle import route, run, template

@route('/hello/<name>')
def hello(name='michael'):
   return 'hello '+ name


run(host='172.20.4.112', port=8080)
