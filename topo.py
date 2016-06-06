#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='192.168.56.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    info('*** switches protocols')
    openFlowVersions = []
    openFlowVersions.append('OpenFlow13')
    protoList = ",".join(openFlowVersions)
    switchParms={}
    switchParms['protocols'] = protoList

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, **switchParms)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, **switchParms)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, **switchParms)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, **switchParms)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, **switchParms)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, **switchParms)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, **switchParms)
   
    info( '*** Add hosts\n')
    h1_1 = net.addHost('h1_1', cls=Host, ip='10.0.1.1', mac='B6:29:CE:E1:DB:51', defaultRoute=None)
    h1_2 = net.addHost('h1_2', cls=Host, ip='10.0.1.2', mac='B6:29:CE:E1:DB:52', defaultRoute=None)
    h1_3 = net.addHost('h1_3', cls=Host, ip='10.0.1.3', mac='B6:29:CE:E1:DB:53', defaultRoute=None)
   
    h2_1 = net.addHost('h2_1', cls=Host, ip='10.0.2.1', mac='92:88:E9:9C:0D:81', defaultRoute=None)
    h2_2 = net.addHost('h2_2', cls=Host, ip='10.0.2.2', mac='92:88:E9:9C:0D:82', defaultRoute=None)
    h2_3 = net.addHost('h2_3', cls=Host, ip='10.0.2.3', mac='92:88:E9:9C:0D:83', defaultRoute=None)
    

    info( '*** Add links\n')
    net.addLink(s1, s2)
    net.addLink(s1, s6)
    net.addLink(s2, s5)
    net.addLink(s2, s7)
    net.addLink(s2, s4)
    net.addLink(s2, s3)
    net.addLink(s3, s6)
    net.addLink(s4, s6)
    net.addLink(s6, s5)
    net.addLink(s6, s7)
    
    #hosts links group 1
    net.addLink(h1_1, s2)
    net.addLink(h1_2, s2)
    net.addLink(h1_3, s2)
    #hosts links group 2
    net.addLink(h2_1, s6)
    net.addLink(h2_2, s6)
    net.addLink(h2_3, s6)

    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    
    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

