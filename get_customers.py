#!/usr/bin/env python

import xmlrpclib
import yaml
import getpass

server = xmlrpclib.ServerProxy( "http://store.iheartengineering.com/index.php/api/xmlrpc" )
password = getpass.getpass( "Enter API Password": )
session = server.login( 'api', password )


customers = server.call( session, 'customer.list' )
for cust in customers:
    print cust['email']
