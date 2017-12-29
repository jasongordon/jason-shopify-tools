import csv
import time
import shopify

import optparse


parser = optparse.OptionParser()
parser.add_option('--api_key', action="store" )
parser.add_option('--password', action="store" )
parser.add_option('--store_name', action="store" )
parser.add_option('--csv_file', action="store" )

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
    rowcount=0
    bad_results = []
    for row in readCSV:
        
        variant_id = row[1]
        variant_price = row[3]
        descr = "%s %s %s %s" % (row[6], row[7], row[8], row[9])
        
        v=shopify.Variant.find(variant_id)
        
        print(variant_id, variant_price, v.price)
        if(float(v.price) != float(variant_price)):
            my_err = "%s - %s - csv price: %s, shopify price: %s" % (variant_id, descr, float(variant_price), float(v.price))
            bad_results.append(my_err)
                    
        if(rowcount % 2 == 0):
            time.sleep(1)
        rowcount += 1

        
        
    
print ("Error results\n")
print "\n".join(bad_results)