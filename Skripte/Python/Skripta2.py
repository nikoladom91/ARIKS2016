#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ as env
import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
import novaclient.client
from credentials import get_creds, get_nova_creds

keystone = ksclient.Client(**get_creds())

glance_endpoint = keystone.service_catalog.url_for(service_type='image')
glance = glclient.Client(glance_endpoint, token=keystone.auth_token)

# instanciranje nova objekta, argument "2" se odnosi na verziju klase
# koja ce biti korištena za stvaranje objekta
nova = novaclient.client.Client("2", **get_nova_creds())

# ispis teksta na terminal
print "List of all images by name and size:"

# dohvacanje liste koja opisuje sve pohranjene slike unutar glance usluge
images = glance.images.list()

# for petlja koja se izvodi za svaki element (image) unutar liste (images)
for image in images:

        # Ispis atributa imena i velicine pojedine pohranjene OS slike
        print("\n%s\n%s" % (image[u'name'], image[u'size']))

# traženje unosa preko terminala od strane korisnika
name = raw_input('\nSearch for image by name: ')

print('\nLooking for %s...\n' % name)

# pocetak try bloka
try:
        #dohvacanje specificne OS slike putem njezinog imena
        image = nova.images.find(name=name)
        print('Image found, id is:%s' % image.id)

#izvršava se ukoliko dode do greške unutar try bloka
except:
        print "Image Not Found"