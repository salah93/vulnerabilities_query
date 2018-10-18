import pandas as pd
from argparse import ArgumentParser
from os.path import join
from pymongo import MongoClient


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('assets_table_path')
    parser.add_argument('--target_folder', default='/tmp')
    args = parser.parse_args()
    return args.assets_table_path, args.target_folder


def connect_database(url, mongo_dict):
    client = MongoClient(url)
    database = client[mongo_dict['database']]
    collection = database[mongo_dict['collection']]
    return collection[mongo_dict['document']]


def query_nvd(cursor, vendor_name=None, product_name=None, version_value=None):
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

    return list(cursor.find(
        {'$and': [product_query, version_query, vendor_query]}))


if __name__ == '__main__':
    ASSETS_TABLE_PATH, TARGET_FOLDER = parse_args()
    TARGET_PATH = join(TARGET_FOLDER, 'results.csv')
    T = pd.read_csv(ASSETS_TABLE_PATH)
    TABLE = T.where(pd.notnull(T), None)
    URL = 'mongodb://CrossCompute:abc123@162.216.19.185:27017/Vulnerabilities'
    MONGO_DICT = dict(
        database='Vulnerabilities',
        collection='NVD',
        document='CVE_Items')
    CURSOR = connect_database(URL, MONGO_DICT)

    def f(row):
        return {
            'vulnerabilities': query_nvd(CURSOR, *row.values),
            'query': 'vendor: %s, product: %s, version: %s' % tuple(
                row.values)}

    RESULTS = TABLE.apply(f, axis=1, result_type='expand')
    RESULTS.to_csv(TARGET_PATH, index=False)
    print('results_table_path = %s' % TARGET_PATH)
