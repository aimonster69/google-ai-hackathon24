from flask import Flask, jsonify, request
from flask_cors import CORS


import sys
sys.path.insert(0, '../')

from Factory.Factory import Jobs, Job

app = Flask(__name__)
CORS(app) 

try:
  @app.route('/Jobs/Add', methods=['POST'])
  def Add():
    data = request.get_json()
    if not data:
      return jsonify({'message': 'No data provided'}),

    title = data.get('title')
    dataurl = data.get('dataurl')
    prompt = data.get('prompt')
    columns = data.get('columns')
    rows = data.get('rows')
    
    job = Job(title)
    job.Title = title
    job.Database.append(dataurl)
    job.Prompt.append(prompt)
    job.Columns.append(columns)
    job.Rows.append(rows)

    Jobs.Jobs.append(job)

    print("STATUS = " + job.Status)

    count = 0
    while(job.Status == "Running"):
      count += 1
      #print("Waiting " + str(count))
    return jsonify({'message': job.Response}), 201

except Exception as e:
  #print(e)
  s = e


# class APIs:

class APIs:

  def RunJobsAdd(self):
    try:
      app.run(debug=True)
      print("Live on port")
    except Exception as e:
      #print(e)
      s = e

    
