#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from os import environ as env
import novaclient.client
from credentials import get_nova_creds

nova = novaclient.client.Client("2", **get_nova_creds())

try:

    # odabir resursa za stvaranje instance
    image = nova.images.find(name="ubuntu_cloud15")
    flavor = nova.flavors.find(name="m1.small")
    net = nova.networks.find(label="my_net2")
    nics = [{'net-id': net.id}]
    
    # stvaranje instance
    instance = nova.servers.create(name="my_inst2", image=image,
                                   flavor=flavor, key_name="my_key1",
                                   nics=nics)

    # cekanje 5 sec. prije ispisa
    # kako bi se narede unutar nove stigle izvršiti
    print("Sleeping for 5s after create command")
    time.sleep(5)

    # ispis svih instanci
    print("List of VMs")
    print(nova.servers.list())

finally:
    print("Execution Completed")