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
        if request.form.get('dropdownitem') == 'ApS':
            if JsonLoader(request.form['textfield']) != "" and request.form['emailfield'] != "":
                insertjson(request.form['textfield'], request.form['emailfield'])
                return redirect('/processor')
            else:
                flash('Invalid JSON and/or e-mail')
        if request.form.get('dropdownitem') == 'Enkeltmandsvirksomhed':
            if JsonLoader(request.form['textfield']) != "" and request.form['vat'] != "":
                pass
            else:
                flash('Invalid JSON')
    return render_template('home.html')

@app.route('/processor')
def processor():
    jsondata, email = getjson()
    legalOwnerList, managementList, company, jsondata = JsonParser(jsondata)
    time, ID = browser(legalOwnerList, managementList, company, jsondata, email)
    return render_template('processor.html', time = time, ID = ID)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)