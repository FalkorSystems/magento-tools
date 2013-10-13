#!/usr/bin/env python

import xmlrpclib
import yaml
import csv
import getpass
import base64

server = xmlrpclib.ServerProxy( "http://www.iheartengineering.com/index.php/api/xmlrpc" )
password = getpass.getpass( "Enter API Password:" )
session = server.login( 'api', password )

product_list = server.call( session, 'catalog_product.list' )

for product in product_list:
    if not '71' in product['category_ids']:
        continue

    keep_trying=True
    while keep_trying:
        try:
            info=server.call(session, 'cataloginventory_stock_item.update',
                             [product['sku'],
                              { 'manage_stock': 1,
                                'use_config_manage_stock': 1,
                                'backorders': 0,
                                'use_config_backorders': 0,
                                'notify_stock_qty': 10,
                                'use_config_notify_stock_qty': 0
                                }
                              ])
            print "Manage Stock: %s" % product['sku']
            keep_trying = False
        except xmlrpclib.Fault as e:
            print "Error: %s" % e
    
