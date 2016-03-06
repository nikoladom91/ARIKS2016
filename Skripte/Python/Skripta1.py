#!/usr/bin/env python

from os import environ as env
import glanceclient as glclient
import keystoneclient.v2_0.client as ksclient

#instanciranje keystone objekta putem enviorment varijabli
keystone = ksclient.Client(auth_url=env['OS_AUTH_URL'],
                           username=env['OS_USERNAME'],
                           password=env['OS_PASSWORD'],
                           tenant_name=env['OS_TENANT_NAME'],
                           region_name=env['OS_REGION_NAME'])

#dohvaćanje URL adrese glance API-ja
glance_endpoint = keystone.service_catalog.url_for(service_type='image')

#instanciranje glance objekta putem keystone usluga
glance = glclient.Client('1', glance_endpoint, token=keystone.auth_token)
 
#kreacija string varijable koja sadrži ime OS slike
imagefile = "wily-server-cloudimg-amd64-disk1.img"

with open(imagefile) as fimage:
	#korištenje glance metode za kreaciju OS slike
	glance.images.create(name="ubuntu-cloud15", is_public=False,
                            disk_format="qcow2",
                            container_format="bare",
                            data=fimage)