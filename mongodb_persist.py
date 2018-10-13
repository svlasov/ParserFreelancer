# common work with data base
import pymongo

from pymongo import MongoClient

db_host = 'localhost'
db_name = "jobs"
coll_name = "jobs"
client = MongoClient(db_host)
db = client[db_name]

jobs_coll = db.get_collection(coll_name)
skills_coll = db.get_collection("skills")


def load_latest_jobs(limit):
    job_docs = list(db.jobs.find().sort([("created_at", pymongo.DESCENDING)]).limit(limit))
    # convert result to json and return
    return job_docs