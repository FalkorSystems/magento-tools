#!/usr/bin/env python

import xmlrpclib
import yaml
import csv
import getpass

server = xmlrpclib.ServerProxy( "http://store.iheartengineering.com/index.php/api/xmlrpc" )
password = getpass.getpass( "Enter API Password": )
session = server.login( 'api', password )

pricefile = open( 'amazon_prices.csv', 'rb' )
amazon_price_list = {}
rows = csv.reader( pricefile )
for row in rows:
    amazon_price_list[row[1]] = float(row[0])

# get product list
product_list = server.call( session, 'catalog_product.list' )


for product in product_list:
    sku = product['sku']
    try:
        product_info = server.call( session, 'catalog_product.info', sku )
    except:
        print "Warning: unable to get product %s" % sku
    else:
        # Check amazon price list first, otherwise
        price = float(product_info['price'])
        if sku in amazon_price_list:
            amazon_price = amazon_price_list[sku]
            print "Got price for %s from list %4.2f" % ( sku, amazon_price )
        else:
            amazon_price = price * 1.15

        print "Setting amazon price for %s to %4.2f from %4.2f" % ( sku, amazon_price,
                                                                    price )
        parms = [sku, {'amazon_price': "%4.2f" % amazon_price}]
        result = server.call( session, 'catalog_product.update', parms )
