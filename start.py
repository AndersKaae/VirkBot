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
        if JsonLoader(request.form['textfield']) != "" and request.form['emailfield'] != "":
            insertjson(request.form['textfield'], request.form['emailfield'])
            return redirect('/processor')
        else:
            flash('Invalid JSON and/or e-mail')
    return render_template('home.html')

@app.route('/processor')
def processor():
    jsondata = getjson()
    legalOwnerList, managementList, company, jsondata = JsonParser(jsondata)
    time = browser(legalOwnerList, managementList, company, jsondata)
    return render_template('processor.html', time = time)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)