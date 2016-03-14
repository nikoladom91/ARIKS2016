#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dohvaćanje vanjskih funkcija
from os import environ as env
import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
from credentials import get_creds

# instanciranje keystone objekta putem enviorment varijabli
keystone = ksclient.Client(**get_creds())

# dohvaćanje URL adrese glance API-ja
glance_endpoint = keystone.service_catalog.url_for(service_type='image')

# instanciranje glance objekta putem keystone usluga
glance = glclient.Client(glance_endpoint, token=keystone.auth_token)
 
# korištenje glance metode za kreaciju elementa OS slike
image = glance.images.create(name="ubuntu_cloud15", visibility="public",
                            disk_format="qcow2",
                            container_format="bare")
# korištenje glance metode za dodavanje OS slike prethodno kreiranom elementu
glance.images.upload(image.id, open('wily-server-cloudimg-amd64-disk1.img', 'rb'))

print "Image Created"