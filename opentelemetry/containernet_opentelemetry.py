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
d1 = net.addDocker('d1_tracer', ip='10.0.0.251', dimage="tracer:ubuntu")
d2 = net.addDocker('d2_server', ip='10.0.0.252', dimage="server:ubuntu")
d3 = net.addDocker('d3_random', ip='10.0.0.1', dimage="client:random")
d4 = net.addDocker('d4_ddos', ip='10.0.0.2', dimage="client:ddos")


info('*** Adding switches\n')
s1 = net.addSwitch('s1')


info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(d2, s1)
net.addLink(d3, s1)
net.addLink(d4, s1)


info('*** Starting network\n')
net.start()


info('*** Testing connectivity\n')
net.ping([d1, d2, d3, d4])


info('*** Running CLI\n')
CLI(net)


info('*** Stopping network')
net.stop()

