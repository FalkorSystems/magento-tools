#!/usr/bin/env python

import xmlrpclib
import yaml
import csv
import getpass
import base64

server = xmlrpclib.ServerProxy( "http://www.iheartengineering.com/index.php/api/xmlrpc" )
password = getpass.getpass( "Enter API Password:" )
session = server.login( 'api', password )

attribute_sets = server.call( session, 'catalog_product_attribute_set.list' )
attribute_set = attribute_sets[0]['set_id']
imagedirectory = "/mnt/hgfs/sameer/Google Drive/IHE/Catalog"

catalog = server.call( session, 'catalog_product.list' )
sku_index = {}
for product in catalog:
    sku_index[product['sku']] = True

salvage_file = open( 'catalog.csv', 'rb' )
rows = csv.reader( salvage_file )
for row in rows:
    sku = 'IHE-RD-%06d' % float(row[1])
    description = "%s (Lot of %d)" % (row[4], float(row[3]))
    parameters = { 'name': description,
                   'websites': ['1'],
                   'short_description': description,
                   'description': "<P>Lot Size: %d</P><P>More information: <a href=\"%s\">%s</a></p><p>Manufacturer: %s</p><p>Distributor: %s</p><p>MPN: %s</p><p>DPN: %s</p>" %
                   (float(row[3]), row[5], row[5], row[6], row[7], row[8], row[9] ),
                   'status': '1',
                   'weight': row[11],
                   'tax_class_id': '2',
                   'categories': ['71', '72'],
                   'price': row[14]
                   } 

    if sku not in sku_index:
        print "Creating: %s:%s" % (sku,description)
        part = [ 'simple',
                 attribute_set,
                 sku,
                 parameters ]
        server.call( session, 'catalog_product.create', part )
    else:
        print "Updating: %s:%s" % (sku,description)
        server.call( session, 'catalog_product.update', [ sku, parameters ] )

    imagename = "%d.JPG" % (float(row[1]))
    imagedata = open( imagedirectory + "/" + imagename, "r" ).read()
    image = { 'file': { 'name': imagename,
                        'content': base64.b64encode( imagedata ),
                        'mime': 'image/jpeg' 
                        },
              'label': 'Image',
              'position': 1,
              'types': [ 'small_image', 'image', 'thumbnail' ],
              'exclude': 0 }
    
    print "Uploading image for %s:%s - %s" % (sku, description, imagename)
    imagefilename = server.call( session, 'catalog_product_attribute_media.create', [sku, image])

    inventory = row[2]
    update = [ sku, { 'qty': inventory,
                      'is_in_stock': 1 } ]
    print "Updating %s:%s with stock %d" % (sku, description, float(inventory))
    server.call( session, 'cataloginventory_stock_item.update', update )







