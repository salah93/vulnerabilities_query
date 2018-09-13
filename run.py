from argparse import ArgumentParser
from pymongo import MongoClient
from bson import json_util


if __name__ == '__main__':
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
        uri = "mongodb://162.216.19.185:27017"
        client = MongoClient(uri)
        db = client['Vulnerabilities']
        collection = db['NVD']
        document = collection['CVE_Items']

        product_query, vendor_query, version_query = {}, {}, {}
        if args.product_name:
            product_query = {
                'cve.affects.vendor.vendor_data.product.product_data.product_name':
                    args.product_name}
        if args.vendor_name:
            vendor_query = {
                'cve.affects.vendor.vendor_data.vendor_name':
                    args.vendor_name}
        if args.version_value:
            version_query = {
                'cve.affects.vendor.vendor_data.product.product_data.version.version_data.version_value':
                    args.version_value}

        results = document.find(
            {'$and': [product_query, version_query, vendor_query]})
        with open('vulnerabilities.json', 'w') as f:
            f.write(json_util.dumps(results))
