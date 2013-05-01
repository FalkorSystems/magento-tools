#!/usr/bin/env python

import xmlrpclib
import yaml

server = xmlrpclib.ServerProxy( "http://store.iheartengineering.com/index.php/api/xmlrpc" )
session = server.login( 'api', 'testtest1' )

                                
                            
asin_stream = open( '/var/www/learn.iheartengineering.com/extensions/YAML/data/product_asin.yaml' )
asins = yaml.load( asin_stream )

for sku, asin in asins.items():
    # make sure the product exists
    try:
	server.call( session, 'catalog_product.info', sku )
    except:
	print "Warning: %s does not exist" % sku
    else:
        parms = [sku, {'asin': asin}]
        print "Updating %s with %s" % (sku, asin)
	result = server.call( session, 'catalog_product.update', parms )
	if not result:
            print "Warning: unable to update %s" % sku
