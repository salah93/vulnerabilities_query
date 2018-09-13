import json
import os
from itertools import chain
from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('localhost', 27017, connect=False)
    db = client['Vulnerabilities']
    collection = db['NVD']
    document = collection['CVE_Items']

    datafolder = 'datasets'
    cve_items = []
    for f in os.listdir(datafolder):
        path = os.path.join(datafolder, f)
        with open(path) as f:
            j = json.load(f)
            cve_items.append(j['CVE_Items'])

    document.insert_many(chain(*cve_items))
