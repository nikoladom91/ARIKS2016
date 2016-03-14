#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ as env
import novaclient.client
from neutronclient.v2_0 import client as neutronclient
from credentials import get_creds, get_nova_creds

nova = novaclient.client.Client("2", **get_nova_creds())

neutron = neutronclient.Client(**get_creds())

# korištenje find metode nova objekta za tohvat ID-a privatne i javne mreže
network_id = nova.networks.find(label='my_net2').id
public_network_id = nova.networks.find(label='public').id

# pisanje zahtjeva za stvaranjem routera
body_router = {'router': {'name': 'my_router2',
                      'admin_state_up': True}}

router = neutron.create_router(body=body_router)
router_id = router['router']['id']

# pisanje zahtjeva za stvaranjem porta
# koji na privatnoj mreži sa adresom 10.20.1.1 (gateway)
body_port = {'port': {
    'admin_state_up': True,
    'network_id': network_id,
    'fixed_ips': [{"ip_address": "10.20.1.1"}]
    }}
	
port = neutron.create_port(body=body_port)
port_id = port['port']['id']

# stvaranje gateway-a putem kojega ce router imati pristup javnoj mreži
neutron.add_gateway_router(router=router_id, body={"network_id": public_network_id})

# stvaranje interface-a putem kojega ce router imati pristup privatnoj mreži
neutron.add_interface_router(router=router_id, body={"port_id": port_id})

# ispis podataka o stvorenom router-u
router = neutron.show_router(router_id)
print(router)
print("\nExecution Completed\n")