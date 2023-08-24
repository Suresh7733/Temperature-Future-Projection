import netCDF4
from flask import Flask, render_template ,request,session,send_file
from db import result
import pandas as pd
import numpy as np
from css import is_in_india
import os

app = Flask(__name__)
@app.route('/form-handler', methods=['POST'])

def handle_form():
  lat = 0
  lon =0
  try:
     lat =float(request.form.get('lat'))
     lon =float(request.form.get('lon'))
  except:
     error_message ='please enter valid latitude and longitude'
     return render_template('index.html',error_message=error_message)
  if(is_in_india(lat,lon)):
   try:
     csv1_path, csv2_path =result(lat, lon)
     return render_template('second.html',csv1_path=csv1_path,csv2_path=csv2_path)
   except:
      error_message ='The IMD data is not available for provide latitude and longitude values. please try again'
      return render_template('index.html',error_massage=error_message)
      
  else:
     error_message = 'The provided latitude and longitude values are not within India. Please try again.'
     return render_template('index.html', error_message=error_message)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/download-csv1')
def download_csv1():
    csv1_path = 'static/Future_Temperature_Projection_2021-2060.csv'
    return send_file(csv1_path, as_attachment=True)

@app.route('/download-csv2')
def download_csv2():
    csv2_path = 'static/Future_Temperature_Projection_2061-2100.csv'
    return send_file(csv2_path, as_attachment=True)

@app.route('/Resubmit',methods=['POST'])
def Resubmit():
   return render_template('index.html')

if(__name__=='__main__'):
    app.run(debug=True,port=8000)

