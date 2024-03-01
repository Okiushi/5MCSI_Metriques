from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world(): # To test :)
    return render_template('hello.html')
  
@app.route("/contact/")
def contact():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("graphique2.html")

@app.route('/commitsdata/')
def commitsdata():
    response = urlopen('https://api.github.com/repos/Okiushi/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    commits_per_min = {}
    results = []
    for list_element in json_content:
        dt_value = list_element.get('commit', {}).get('author', {}).get('date')
        minutes = datetime.strptime(dt_value, '%Y-%m-%dT%H:%M:%SZ')
        if minutes in commits_per_min:
            commits_per_min[minutes] += 1
        else:
            commits_per_min[minutes] = 1
    for key in commits_per_min:
        results.append({'date': key, 'commits': commits_per_min[key]})
    print(results)
    print(json.dumps(results))
    return jsonify(results=results)

@app.route("/commits/")
def commits():
    return render_template("commits.html")
    

if __name__ == "__main__":
  app.run(debug=True)
