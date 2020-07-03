from flask import Flask, render_template, flash, request, redirect, url_for
import time
from browser import *
from webfunctions import *
from data import *
from database import *
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        if JsonLoader(request.form['textfield'], strict=False) != "":
            insertjson(request.form['textfield'])
            return redirect('/processor')
        else:
            flash('Invalid JSON')
    return render_template('home.html')

@app.route('/processor')
def processor():
    jsondata = getjson()
    o1, r1, l1, c1 = JsonParser(jsondata)
    browser(o1, r1, l1, c1)
    return render_template('processor.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)