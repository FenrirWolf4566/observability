#!/usr/bin/python3
"""
This is the most simple example to showcase Containernet.
"""
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
d1 = net.addDocker('d1', ip='10.0.0.251', dimage="pinger:ubuntu1804")
d2 = net.addDocker('d2', ip='10.0.0.252', dimage="receiver:ubuntu1804")

h1 = net.addHost('h1', ip='10.0.0.1')
h2 = net.addHost('h2', ip='10.0.0.2')


info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')


info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(h1, s1)
net.addLink(h2, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, d2)


info('*** Starting network\n')
net.start()


info('*** Testing connectivity\n')
net.ping([h1, h2])
net.ping([h1, d1])
net.ping([h1, d2])
net.ping([d1, d2])
net.ping([d1, h2])
net.ping([d2, h2])


info('*** Running CLI\n')
CLI(net)


info('*** Stopping network')
net.stop()