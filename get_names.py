import pandas as pd
from run import connect_database


if __name__ == '__main__':
    URL = 'mongodb://CrossCompute:abc123@162.216.19.185:27017/Vulnerabilities'
    MONGO_DICT = dict(
        database='Vulnerabilities',
        collection='NVD',
        document='CVE_Items')
    CURSOR = connect_database(URL, MONGO_DICT)
    VULNERABILITIES = CURSOR.find({})
    vendor_names = set()
    product_names = set()
    for vuln in VULNERABILITIES:
        for vendor in vuln['cve']['affects']['vendor']['vendor_data']:
            vendor_names.add(vendor['vendor_name'])
            for product in vendor['product']['product_data']:
                product_names.add(product['product_name'])
    with open('product_names.txt', 'w') as f:
        for product in sorted(list(product_names)):
            f.write(product + '\n')
    with open('vendor_names.txt', 'w') as f:
        for vendor in sorted(list(vendor_names)):
            f.write(vendor + '\n')
