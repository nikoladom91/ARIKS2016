#!/usr/bin/env python
import time
from os import environ as env
import novaclient.client

nova = novaclient.client.Client("2", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                region_name=env['OS_REGION_NAME'])

try:

    #odabir resursa za stvaranje instance
    image = nova.images.find(name="ubuntu_cloud15")
    flavor = nova.flavors.find(name="m1.small")
    net = nova.networks.find(label="my_net2")
    nics = [{'net-id': net.id}]
    
    #stvaranje instance
    instance = nova.servers.create(name="vm2", image=image,
                                   flavor=flavor, key_name="my_key",
                                   nics=nics)

    #cekanje 5 sec. prije ispisa kako bi se narede unutar nove
    #stigle izvršiti
    print("Sleeping for 5s after create command")
    time.sleep(5)

    #ispis svih instanci
    print("List of VMs")
    print(nova.servers.list())

finally:
    print("Execution Completed")