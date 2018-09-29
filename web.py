from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# instead of db

jobs_idx = {}


@app.route("/")
def hello():

    unsorted_list = list(jobs_idx.values())

    format = "%a %b %d %H:%M:%S %Z %Y"

    for d in unsorted_list:
        created_at_str = d['created_at']
        d['created_at_dt'] = datetime.datetime.strptime(created_at_str,format)

    # Source for the lambda:
    # def sort_dict_by_created_at(d):
    #     return d['created_at_dt']
    
    sort_dict_by_created_at = lambda d: d['created_at_dt']
    
    sorted_by_created_at = sorted(unsorted_list, key=sort_dict_by_created_at, reverse=True)

    return jsonify(sorted_by_created_at)


@app.route("/search")
def search():
    data = request.args

    description = data.get("description", "")
    location = data.get("location", "")

    url = "https://jobs.github.com/positions.json?description={description}&location={location}".format(
        description=description,
        location=location
    )

    ext_resp = requests.get(url)

    json_resp = ext_resp.json()

    for job in json_resp:
        job_id = job['id']
        if job_id not in jobs_idx:
            jobs_idx[job_id] = job
            
    return jsonify(json_resp)
    
   

if __name__=="__main__":
    port = 8000
    app.run(port=port, debug=True)