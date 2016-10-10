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


class MyHost(Host):
    def __init__(self, name, intfDict, *args, **kwargs):
        Host.__init__(self, name, *args, **kwargs)

        self.intfDict = intfDict

    def config(self, **kwargs):
        Host.config(self, **kwargs)
        self.cmd('sysctl net.ipv4.ip_forward=1')

        for intf, attrs in self.intfDict.items():
            self.cmd('ip addr flush dev %s' % intf)
            if 'mac' in attrs:
                self.cmd('ip link set %s down' % intf)
                self.cmd('ip link set %s address %s' % (intf, attrs['mac']))
                self.cmd('ip link set %s up ' % intf)
            for addr in attrs['ipAddrs']:
            	print str(attrs)
            	mask = attrs['mask']
            	gateway = attrs['gateway']
            	#print str('ifconfig %s %s netmask %s' % (intf, addr, mask))
                self.cmd('ifconfig %s %s netmask %s' % (intf, addr, mask))
                self.cmd('route add default gw %s' % (gateway))
                #self.cmd('ip a add %s dev %s' % (addr, intf))
                #self.cmd('ip addr add broadcast %s dev %s' % (addr, intf))


    def terminate(self):
        self.cmd("Bye!")

        Host.terminate(self)

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='192.168.103.11',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')

    # sr_03 = net.addHost('sr_03', cls=Host, ip='10.0.0.4/24', defaultRoute='10.0.0.1')
    # client_02 = net.addHost('client_02', cls=Host, ip='10.0.0.6/24', defaultRoute='10.0.0.1')
    # client_01 = net.addHost('client_01', cls=Host, ip='10.0.0.5/24', defaultRoute='10.0.0.1')
    # sr_01 = net.addHost('sr_01', cls=Host, ip='10.0.0.2/24', defaultRoute='10.0.0.1')
    # sr_02 = net.addHost('sr_02', cls=Host, ip='10.0.0.3/24', defaultRoute='10.0.0.1')
    # mar = net.addHost('mar', cls=Host, ip='10.0.0.7/24', defaultRoute='10.0.0.1')
    # topology = net.addHost('topology', cls=Host, ip='10.0.0.9/24', defaultRoute='10.0.0.1')
    # consul = net.addHost('consul', cls=Host, ip='10.0.0.8/24', defaultRoute='10.0.0.1')
    # root = net.addHost('root', inNamespace=False, ip='10.0.0.1/24' )

    #root
    root_eth0 = { 'ipAddrs' : ['10.0.0.1'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_root = { 'root-eth0' : root_eth0 }
    root = net.addHost("root", cls=MyHost, inNamespace=False, intfDict=myDict_root)

    #Region 01
    #sr_01
    sr_01_eth0 = { 'ipAddrs' : ['10.0.1.2'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_01 = { 'sr_01-eth0' : sr_01_eth0 }
    sr_01 = net.addHost("sr_01", cls=MyHost,  intfDict=myDict_sr_01, defaultRoute='10.0.0.1')

    #sr_02
    sr_02_eth0 = { 'ipAddrs' : ['10.0.1.3'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_02 = { 'sr_02-eth0' : sr_02_eth0 }
    sr_02 = net.addHost("sr_02", cls=MyHost,  intfDict=myDict_sr_02)

    #Region 02
    #sr_03
    sr_03_eth0 = { 'ipAddrs' : ['10.0.2.2'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_03 = { 'sr_03-eth0' : sr_03_eth0 }
    sr_03 = net.addHost("sr_03", cls=MyHost,  intfDict=myDict_sr_03)

    #sr_04
    sr_04_eth0 = { 'ipAddrs' : ['10.0.2.3'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_04 = { 'sr_04-eth0' : sr_04_eth0 }
    sr_04 = net.addHost("sr_04", cls=MyHost,  intfDict=myDict_sr_04)

    #Region 03
    #sr_05
    sr_05_eth0 = { 'ipAddrs' : ['10.0.3.2'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_05 = { 'sr_05-eth0' : sr_05_eth0 }
    sr_05 = net.addHost("sr_05", cls=MyHost,  intfDict=myDict_sr_05)

    #sr_06
    sr_06_eth0 = { 'ipAddrs' : ['10.0.3.3'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_06 = { 'sr_06-eth0' : sr_06_eth0 }
    sr_06 = net.addHost("sr_06", cls=MyHost,  intfDict=myDict_sr_06)

    #Region 04
    #sr_07
    sr_07_eth0 = { 'ipAddrs' : ['10.0.4.2'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_07 = { 'sr_07-eth0' : sr_07_eth0 }
    sr_07 = net.addHost("sr_07", cls=MyHost,  intfDict=myDict_sr_07)

    #sr_08
    sr_08_eth0 = { 'ipAddrs' : ['10.0.4.3'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_08 = { 'sr_08-eth0' : sr_08_eth0 }
    sr_08 = net.addHost("sr_08", cls=MyHost,  intfDict=myDict_sr_08)

    #Region 05
    #sr_09
    sr_09_eth0 = { 'ipAddrs' : ['10.0.5.2'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_09 = { 'sr_09-eth0' : sr_09_eth0 }
    sr_09 = net.addHost("sr_09", cls=MyHost,  intfDict=myDict_sr_09)

    #sr_10
    sr_10_eth0 = { 'ipAddrs' : ['10.0.5.3'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_sr_10 = { 'sr_10-eth0' : sr_10_eth0 }
    sr_10 = net.addHost("sr_10", cls=MyHost,  intfDict=myDict_sr_10)


    #Client01
    client_01_eth0 = { 'ipAddrs' : ['10.0.1.5'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_client_01 = { 'client_01-eth0' : client_01_eth0 }
    client_01 = net.addHost("client_01", cls=MyHost,  intfDict=myDict_client_01)

    #Client02
    client_02_eth0 = { 'ipAddrs' : ['10.0.1.6'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_client_02 = { 'client_02-eth0' : client_02_eth0 }
    client_02 = net.addHost("client_02", cls=MyHost,  intfDict=myDict_client_02)

    #MAR
    mar_eth0 = { 'ipAddrs' : ['10.0.1.7'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_mar = { 'mar-eth0' : mar_eth0 }
    mar = net.addHost("mar", cls=MyHost,  intfDict=myDict_mar, defaultRoute='10.0.0.1')

    #Topology
    topology_eth0 = { 'ipAddrs' : ['10.0.1.8'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_topology = { 'topology-eth0' : topology_eth0 }
    topology = net.addHost("topology", cls=MyHost,  intfDict=myDict_topology)

    #Consul
    consul_eth0 = { 'ipAddrs' : ['10.0.1.9'], 'mask' : '255.0.0.0', 'gateway' : '10.0.0.1' }
    myDict_consul = { 'consul-eth0' : consul_eth0 }
    consul = net.addHost("consul", cls=MyHost,  intfDict=myDict_consul)
    
   # mar_Eth0 = { 'ipAddrs' : ['10.0.0.7/24'] }
   # mar_Eth1 = { 'ipAddrs' : ['10.10.10.1/24'] }
   # myDict = { 'mar-eth0' : mar_Eth0, 'mar-eth1' : mar_Eth1 }
   #  mar = net.addHost("mar", cls=MyHost, intfDict=myDict)

    

    info( '*** Add links\n')
    #Between switches
    net.addLink(s1, s2)
    net.addLink(s1, s4)
    net.addLink(s2, s3)
    net.addLink(s3, s5)
    net.addLink(s5, s4)
    net.addLink(s5, s6)
    net.addLink(s4, s6)
    net.addLink(s6, s7)
    net.addLink(s7, s8)
    net.addLink(s8, s9)
    net.addLink(s9, s10)
    net.addLink(s9, s11)
    net.addLink(s11, s1)

    #s1
    net.addLink(s1, root)
    net.addLink(s1, sr_01)
    net.addLink(s1, sr_02)
    net.addLink(s1, client_01)
    net.addLink(s1, client_02)
    net.addLink(s1, mar)
    net.addLink(s1, topology)
    net.addLink(s1, consul)
    
    #s2
    net.addLink(s2, sr_03)
    
    #s3
    net.addLink(s3, sr_04)
    
    #s4
    net.addLink(s4, sr_05)
    
    #s5
    net.addLink(s5, sr_06)
    
    #s6
    
    #s7
    net.addLink(s7, sr_07)
    
    #s8
    net.addLink(s8, sr_08)
    
    #s9
    net.addLink(s9, sr_09)
    
    #s10
    net.addLink(s10, sr_10)
    
    #s11
    
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
    net.get('s8').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    net.get('s11').start([c0])

    info( '*** Post configure switches and hosts\n')
    #mar.cmd('ifconfig

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

