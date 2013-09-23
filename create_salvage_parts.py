#!/usr/bin/env python

import xmlrpclib
import yaml
import csv

server = xmlrpclib.ServerProxy( "http://store.iheartengineering.com/index.php/api/xmlrpc" )
session = server.login( 'api', 'testtest1' )
attribute_sets = server.call( session, 'catalog_product_attribute_set.list' )
attribute_set = attribute_sets[0]['set_id']

salvage_file = open( 'ihe_catalog.csv', 'rb' )
rows = csv.reader( salvage_file )
for row in rows:
    sku = 'IHE-RL-%06d' % row[1]
    part = [ 'simple',
             attribute_set,
             sku,
             { 'name': row[2],
               'websites': ['1'],
               'short_description': row[3],
               'description': "More information: %s\nManufacturer: %s\nDistributor: %s\nMPN: %s\nDPN: %s\n" %
               (row[4], row[5], row[6], row[7], row[8] ),
               'status': '1',
               'weight': row[10],
               'tax_class_id': '2',
               'categories': ['70'],
               'price': row[12]
               } ]
    inventory = row[1]
    image = row[9]
    server.call( session, 'catalog_product.create', part )
    server.call( session, 'catalog_product_stock.update', [ sku, { 'qty', inventory,
                                                                   'is_in_stock', 1 } ] )

    # update image
    image = { 'file': { 'name': image + ".jpg",
                        'content': base64_encode( file_get_contents( image + ".jpg" ) ),
                        'mime': => 'image/jpeg' 
                       },
              'label': 'Image',
              'position': 1,
              'types', [ 'small_image' ],
              'exclude', 0 }
    imagefilename = server.call( session, 'catalog_product_media.create', [sku, image])





