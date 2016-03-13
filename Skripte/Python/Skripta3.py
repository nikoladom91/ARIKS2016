#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ as env
import novaclient.client
from neutronclient.v2_0 import client as neutronclient
from credentials import get_creds, get_nova_creds

nova = novaclient.client.Client("2", **get_nova_creds())

#instanciranje neutron objekta
neutron = neutronclient.Client(**get_creds())

network_name = 'my_net2'

try:
      #pohrana podataka o mreži koju želimo stvoriti unutar
      #dvodimenzionalnog asocijativnog polja
      body_net = {'network': {'name': network_name,
                   'admin_state_up': True}}

      #kreacija mreže te pohrana podataka o toj mreži
	netw = neutron.create_network(body=body_net)

      #dohvacanje ID kreirane mreže
	net_dict = netw['network']
	network_id = net_dict['id']

	print('Network %s created' % network_id)

      #pohrana podataka o podmreži koju želimo stvoriti unutar
      #dvodimenzionalnog asocijativnog polja
	body_subnet = {'subnets': [{'name':'my_subnet1',
                            'cidr':'10.20.1.0/24',
                            'ip_version': 4,
                            'network_id': network_id}]}

      #kreacija podmreže te pohrana podataka o toj mreži
	subnet = neutron.create_subnet(body=body_subnet)
    
	print('\nCreated subnet %s\n' % subnet)

#izvršava se nakon što se try blok izvrši bez greške
finally:
    print("Execution completed")