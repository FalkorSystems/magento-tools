#!/usr/bin/env python

import yaml
name_stream = open( '/var/www/learn.iheartengineering.com/extensions/YAML/data/product_name.yaml' )
names = yaml.load( name_stream )

for sku, name in names.items():
    print "%s,%s" % (sku, name)
