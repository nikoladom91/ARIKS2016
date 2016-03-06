#!/usr/bin/env python

from os import environ as env
import glanceclient.v2.client as glclient
import keystoneclient.v2_0.client as ksclient
import novaclient.v2.client as nvclient
import novaclient.client

keystone = ksclient.Client(auth_url=env['OS_AUTH_URL'],
                           username=env['OS_USERNAME'],
                           password=env['OS_PASSWORD'],
                           tenant_name=env['OS_TENANT_NAME'],
                           region_name=env['OS_REGION_NAME'])

glance_endpoint = keystone.service_catalog.url_for(service_type='image')
glance = glclient.Client(glance_endpoint, token=keystone.auth_token)

#instanciranje nova objekta, argument "2" se odnosi na verziju klase #koja ce biti korištena za stvaranje objekta
nova = novaclient.client.Client("2", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                region_name=env['OS_REGION_NAME'])

#ispis teksta na terminal
print "List of all images by name and size:"

#dohvacanje liste koja opisuje sve pohranjene slike unutar glance usluge
images = glance.images.list()

#for petlja koja se izvodi za svaki element (image) unutar liste (images)
for image in images:
        print ""

        #Ispis atributa imena i velicine pojedine pohranjene OS slike
        print image[u'name']
        print image[u'size']

#traženje unosa preko terminala od strane korisnika
name = raw_input('Search for image by name: ')

print('\nLooking for %s...\n' % name)

#pocetak try bloka
try:
        #dohvacanje specificne OS slike putem njezinog imena
        image = nova.images.find(name=name)
        print('Image found, id is:%s' % image.id)

#izvršava se ukoliko dode do greške unutar try bloka
except:
        print "Image Not Found"