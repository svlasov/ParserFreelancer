from flask import Flask, request, jsonify
import requests

from mongodb_persist import load_latest_jobs

app = Flask(__name__)



@app.route("/")
def index():
    # find latest n (n=5) jobs
    # find jobs in db and sort by created_at
    # db.jobs.find().sort({created_at: -1}).limit(1)

    limit = int(request.args.get("limit", 5))

    job_docs = load_latest_jobs(limit)

    return jsonify(job_docs)


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