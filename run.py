from argparse import ArgumentParser
from pymongo import MongoClient
from bson import json_util


class QueryException(Exception):
    pass


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--product_name')
    parser.add_argument('--vendor_name')
    parser.add_argument('--version_value')
    args = parser.parse_args()
    return dict(
        product_name=args.product_name,
        vendor_name=args.vendor_name,
        version_value=args.version_value)


def connect_database(url, mongo_dict):
    client = MongoClient(url)
    database = client[mongo_dict['database']]
    collection = database[mongo_dict['collection']]
    return collection[mongo_dict['document']]


def query_nvd(cursor, product_name=None, vendor_name=None, version_value=None):
    product_query, vendor_query, version_query = {}, {}, {}
    if not (product_name or vendor_name or version_value):
        return None
    if product_name:
        product_query_string = \
            'cve.affects.vendor.vendor_data.product.product_data.product_name'
        product_query = {
            product_query_string: product_name}
    if vendor_name:
        vendor_query_string = \
            'cve.affects.vendor.vendor_data.vendor_name'
        vendor_query = {
            vendor_query_string: vendor_name}
    if version_value:
        version_query_string = \
            'cve.affects.vendor.vendor_data.product.product_data.version.' + \
            'version_data.version_value'
        version_query = {
            version_query_string: version_value}

    return cursor.find(
        {'$and': [product_query, version_query, vendor_query]})


if __name__ == '__main__':
    ARGS = parse_args()
    URL = 'mongodb://CrossCompute:abc123@162.216.19.185:27017/Vulnerabilities'
    MONGO_DICT = dict(
        database='Vulnerabilities',
        collection='NVD',
        document='CVE_Items')
    CURSOR = connect_database(URL, MONGO_DICT)
    RESULTS = query_nvd(CURSOR, **ARGS)
    if RESULTS is None:
        raise QueryException('''
          No filter selected, add --product_name or
          --vendor_name or --version_value''')
    with open('vulnerabilities.json', 'w') as f:
        f.write(json_util.dumps(RESULTS))
