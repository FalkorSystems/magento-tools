#!/usr/bin/env python

# Lower amazon prices for everything by 10%

import xmlrpclib
import yaml
import csv
import getpass
from datetime import *
import math

server = xmlrpclib.ServerProxy( "http://www.iheartengineering.com/index.php/api/xmlrpc" )
password = 'Ada9aez9'
session = server.login( 'auction', password )
endauction = datetime(2013,10,31)
now = datetime.now()
delta = endauction-now
deltahours = delta.seconds/3600 + delta.days*24
auction_category = '71'
oneday = timedelta(1)

# get product list
product_list = server.call( session, 'catalog_product.list' )

for product in product_list:
    if not '71' in product['category_ids']:
        continue

    sku = product['sku']
    try:
        product_info = server.call( session, 'catalog_product.info', sku )
    except:
        print "Warning: unable to get product %s" % sku
    else:
        regular_price = float(product_info['price'])
        try:
            special_price = float(product_info['special_price'])
        except TypeError as e:
            print "WARNING: %s doesn't have a special price yet" % sku
            special_price = regular_price

        if product_info['special_to_date'] != None:
            special_to_date = datetime.strptime(product_info['special_to_date'], '%Y-%m-%d %H:%M:%S')
        else:
            special_to_date = datetime(2013,1,1)

        if special_to_date < now:
            print "WARNING: %s special price is expired. Resetting" % sku
            special_price = regular_price

        final_price = regular_price * 0.01
        final_factor = final_price / special_price
        factor = math.exp(math.log(final_factor)/deltahours)

        new_special_price = special_price * factor
        print "Setting new special price for %s by factor %6.6f to %4.2f from %4.2f" % ( sku,
                                                                                         factor,
                                                                                         special_price,
                                                                                         new_special_price )
        
        yesterday = (now-oneday).strftime('%Y-%m-%d %H:%M:%S')
        tomorrow = (now+oneday).strftime('%Y-%m-%d %H:%M:%S')

        parms = [sku, {'special_price': "%4.2f" % new_special_price,
		       'amazon_price': "%4.2f" % new_special_price,
                       'special_to_date': tomorrow,
                       'special_from_date': yesterday }]
        print parms
        keep_trying = True
        while keep_trying:
            try:
#                result = server.call( session, 'catalog_product.update', parms )
                keep_trying = False
            except xmlrpclib.Fault as e:
                print "Error: %s" % e
                keep_trying = True
