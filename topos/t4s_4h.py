#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def myNetwork():

    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    info('*** switches protocols')
    openFlowVersions = []
    openFlowVersions.append('OpenFlow13')
    protoList = ",".join(openFlowVersions)
    switchParms = {}
    switchParms['protocols'] = protoList

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, **switchParms)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, **switchParms)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, **switchParms)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, **switchParms)

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', mac='B6:29:CE:E1:DB:51')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', mac='B6:29:CE:E1:DB:52')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', mac='B6:29:CE:E1:DB:53')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', mac='B6:29:CE:E1:DB:54')

    info('*** Add links\n')
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s4)
    net.addLink(s4, s1)

    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])

    info('*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
