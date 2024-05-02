from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random

import sys
sys.path.insert(0, '../')

from Factory.Factory import Jobs, Job

app = Flask(__name__)
CORS(app) 

try:
  @app.route('/Jobs/Add', methods=['POST'])
  def Add():
    #data = request.get_json()
    #if not data:
      # return jsonify({'message': 'No data provided'}),

    if 'datafile' not in request.files:
        return 'No file part in the request', 400
    
    excel_file = request.files['datafile']
    
    if excel_file.filename == '':
        return 'No file selected for uploading', 400
    
    save_directory = 'uploads' 

    # Ensure the directory exists, create it if not
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Construct the file path where the file will be saved
    file_path = os.path.join(save_directory, excel_file.filename)
    
    # Save the file to the specified directory
    excel_file.save(file_path)

    r1 = random.randint(0, 100)

    #title = request.form.get('title')
    title = "job" + str(r1)
    dataurl = file_path
    prompt = request.form.get('anlysisprompt')
    tabledescription = request.form.get('tabledescription')
    #columns = request.get('columns')
    #rows = request.get('rows')

    
    job = Job(title)
    job.Title = title
    job.Database.append(dataurl)
    job.Prompt.append(prompt)
    job.TableDescription.append(tabledescription)
    #job.Columns.append(columns)
    #job.Rows.append(rows)

    Jobs.Jobs.append(job)

    print("STATUS = " + job.Status)

    count = 0
    while(job.Status == "Running"):
      count += 1
      #print("Waiting " + str(count))
    return jsonify({'Response': job.Response, 'Images': job.Images, 'OutputFiles': job.OutputFiles, 'Codes': job.Codes, 'Status': job.Status}), 201

except Exception as e:
  #print(e)
  s = e


# class APIs:

class APIs:

  def RunJobsAdd(self):
    try:
      app.run(debug=False, use_reloader=False)
      print("Live on port")
    except Exception as e:
      #print(e)
      s = e

    
