from argparse import ArgumentParser
from pymongo import MongoClient
from bson import json_util


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--product_name')
    parser.add_argument('--vendor_name')
    parser.add_argument('--version_value')
    args = parser.parse_args()
    if not (args.product_name or args.vendor_name or args.version_value):
        parser.error('''
          No filter selected, add --product_name or
          --vendor_name or --version_value''')
    else:
        return args


def connect_database(url, mongo_dict):
    client = MongoClient(url)
    database = client[mongo_dict['database']]
    collection = database[mongo_dict['collection']]
    return collection[mongo_dict['document']]


def main(cursor, args):
    product_query, vendor_query, version_query = {}, {}, {}
    if args.product_name:
        product_query_string = \
            'cve.affects.vendor.vendor_data.product.product_data.product_name'
        product_query = {
            product_query_string: args.product_name}
    if args.vendor_name:
        vendor_query_string = \
            'cve.affects.vendor.vendor_data.vendor_name'
        vendor_query = {
            vendor_query_string: args.vendor_name}
    if args.version_value:
        version_query_string = \
            'cve.affects.vendor.vendor_data.product.product_data.version.' + \
            'version_data.version_value'
        version_query = {
            version_query_string: args.version_value}

    results = cursor.find(
        {'$and': [product_query, version_query, vendor_query]})
    with open('vulnerabilities.json', 'w') as f:
        f.write(json_util.dumps(results))


if __name__ == '__main__':
    ARGS = parse_args()
    URL = 'mongodb://CrossCompute:abc123@162.216.19.185:27017/Vulnerabilities'
    MONGO_DICT = dict(
        database='Vulnerabilities',
        collection='NVD',
        document='CVE_Items')
    CURSOR = connect_database(URL, MONGO_DICT)
    main(CURSOR, ARGS)
