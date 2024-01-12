#!/usr/bin/python3


from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel


setLogLevel('info')


path_docker="./"
net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')


info('*** Adding docker containers\n')
d1 = net.addDocker('d1_zipkin', ip='10.0.0.251', dimage="zipkin:ubuntu")
d2 = net.addDocker('d2_serveur', ip='10.0.0.252', dimage="server:ubuntu")
h1 = net.addHost('h1_sender', ip='10.0.0.1')


info('*** Adding switches\n')
s1 = net.addSwitch('s1')


info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(d2, s1)
net.addLink(h1, s1)


info('*** Starting network\n')
net.start()


info('*** Testing connectivity\n')
net.ping([h1, d1, d2])


info('*** Running CLI\n')
CLI(net)


info('*** Stopping network')
net.stop()