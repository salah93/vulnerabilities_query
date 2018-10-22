import json
from flask import Flask, render_template, jsonify, request
from run import query_nvd, connect_database
from functools import lru_cache

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@lru_cache(maxsize=32)
def query(vendor, product, version):
    return query_nvd(
            app.config['cursor'],
            vendor,
            product,
            version)


@app.route('/query')
def get_query():
    form = request.args
    vendor = form.get('vendor', None)
    product = form.get('product', None)
    version = form.get('version', None)
    page = int(form.get('page', 1))
    size = int(form.get('size', 20))

    vulnerabilities = query(vendor, product, version)
    last_page = len(vulnerabilities) / size
    data = vulnerabilities[(page - 1) * size: page * size]
    return jsonify(dict(last_page=last_page, data=data))


if __name__ == '__main__':
    URL = 'mongodb://CrossCompute:abc123@162.216.19.185:27017/Vulnerabilities'
    MONGO_DICT = dict(
        database='Vulnerabilities',
        collection='NVD',
        document='CVE_Items')
    CURSOR = connect_database(URL, MONGO_DICT)
    app.config['cursor'] = CURSOR
    app.run(debug=True)
