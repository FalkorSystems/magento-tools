#!/usr/bin/env python

# Lower amazon prices for everything by 10%

import xmlrpclib
import yaml
import csv
import getpass

server = xmlrpclib.ServerProxy( "http://store.iheartengineering.com/index.php/api/xmlrpc" )
password = getpass.getpass( "Enter API Password": )
session = server.login( 'api', password )


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
        try:
            price = float(product_info['amazon_price'])
        except TypeError as e:
            print "Error: Amazon price for %s is %s" % (sku, product_info['amazon_price'])
        else:
            amazon_price = price * 0.90

            print "Setting amazon price for %s to %4.2f from %4.2f" % ( sku, amazon_price,
                                                                        price )
            parms = [sku, {'amazon_price': "%4.2f" % amazon_price}]
            result = server.call( session, 'catalog_product.update', parms )
