#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ as env
import novaclient.client
from neutronclient.v2_0 import client as neutronclient
from credentials import get_creds, get_nova_creds

nova = novaclient.client.Client("2", **get_nova_creds())

neutron = neutronclient.Client(**get_creds())

#korištenje find metode nova objekta za tohvat ID-a privatne i javne mreže
network_id = nova.networks.find(label='my_net2').id
public_network_id = nova.networks.find(label='public').id

#definiranje formata zahtjeva
neutron.format = 'json'

#pisanje zahtjeva za stvaranjem routera
request = {'router': {'name': 'my_router2',
                      'admin_state_up': True}}

#izvršavanje zahtjeva i pohrana rezultata
router = neutron.create_router(request)
router_id = router['router']['id']

#ispis podataka o stvorenom router-u
router = neutron.show_router(router_id)
print(router)

#definiranje porta koji ce router spajati sa privatnom mrežom
body_value = {'port': {
    'admin_state_up': True,
    'device_id': router_id,
    'name': 'port1',
    'network_id': network_id
    }}

#stvaranje porta
response = neutron.create_port(body=body_value)

print(response)

#stvaranje gateway-a putem kojega ce router imati pristup javnoj mreži
response = neutron.add_gateway_router(router=router_id, body={"network_id":public_network_id})

print(response)
print("Execution Completed")