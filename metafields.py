import csv
import time
import shopify

import optparse


parser = optparse.OptionParser()
parser.add_option('--api_key', action="store" )
parser.add_option('--password', action="store" )
parser.add_option('--store_name', action="store" )
parser.add_option('--csv_file', action="store" )
parser.add_option('--variant_id', action="store" )

options, args = parser.parse_args()

if not options.api_key:   
    parser.error('--api-key not given not given')
if not options.password:   
    parser.error('--password not given not given')
if not options.store_name:   
    parser.error('--store_name not given not given')
if not options.csv_file:   
    parser.error('--csv_file not given not given')

shop_url = "https://%s:%s@%s/admin" % (options.api_key, options.password, options.store_name)
shopify.ShopifyResource.set_site(shop_url)

shop = shopify.Shop.current


with open(options.csv_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(csvfile) # skip 2 lines
    next(csvfile)
    last_product_name = '';
    rowcount=0
    bad_results = []
    for row in readCSV:

        product_name = row[0]
        variant_id = row[1]

        if(options.variant_id and options.variant_id != variant_id):
            continue
        if(product_name == '' or last_product_name == product_name):
            continue

        variant_price = row[3]
        descr = "%s %s %s %s" % (row[6], row[7], row[8], row[9])

        v=shopify.Variant.find(variant_id)
        
        p=shopify.Product.find(v.product_id)
        print "Product: %s \n" % (p.title)
        
        metafield = shopify.Metafield({'value_type': 'integer', 'namespace': 'seo', 'value': 1, 'key': 'hidden'})
        p.add_metafield(metafield)
                    
        if(rowcount % 2 == 0):
            time.sleep(1)
        rowcount += 1
        last_product_name = product_name

        
        
    
print ("Error results\n")
print "\n".join(bad_results)