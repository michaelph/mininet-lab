#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


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
                # print str('ifconfig %s %s netmask %s' % (intf, addr, mask))
                self.cmd('ifconfig %s %s netmask %s' % (intf, addr, mask))
                self.cmd('route add default gw %s' % (gateway))
                # self.cmd('ip a add %s dev %s' % (addr, intf))
                # self.cmd('ip addr add broadcast %s dev %s' % (addr, intf))

    def terminate(self):
        self.cmd("Bye!")

        Host.terminate(self)


def myNetwork():

    net = Mininet(topo=None,
                  build=False,
                  link=TCLink,
                  ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='172.20.5.137',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch, dpid='000000000000010')
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, dpid='000000000000011')
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, dpid='000000000000012')
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, dpid='000000000000013')
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, dpid='000000000000014')
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch, dpid='000000000000015')
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch, dpid='000000000000016')

    info('*** Add hosts\n')

    # root
    root_eth0 = {'ipAddrs': ['10.0.0.1'],
                 'mask': '255.0.0.0', 'gateway': '10.0.0.1'}
    myDict_root = {'root-eth0': root_eth0}
    root = net.addHost("root", cls=MyHost,
                       inNamespace=False, intfDict=myDict_root)

    # Region 01
    # sr_01
    sr_01_eth0 = {'ipAddrs': ['10.0.1.2'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:10'}
    myDict_sr_01 = {'sr_01-eth0': sr_01_eth0}
    privateDirs_sr_01 = [
        ('/opt/ts2/etc/trafficserver', '/home/notroot/mininet-lab/topos/components/ats/configuration_02')]
    sr_01 = net.addHost("sr_01", cls=MyHost,
                        intfDict=myDict_sr_01, privateDirs=privateDirs_sr_01)

    # sr_02
    sr_02_eth0 = {'ipAddrs': ['10.0.1.3'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:11'}
    myDict_sr_02 = {'sr_02-eth0': sr_02_eth0}
    sr_02 = net.addHost("sr_02", cls=MyHost, intfDict=myDict_sr_02)

    # Region 02
    # sr_03
    sr_03_eth0 = {'ipAddrs': ['10.0.2.2'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:12'}
    privateDirs_sr_03 = [
        ('/opt/ts3/etc/trafficserver', '/home/notroot/mininet-lab/topos/components/ats/configuration_03')]
    myDict_sr_03 = {'sr_03-eth0': sr_03_eth0}
    sr_03 = net.addHost("sr_03", cls=MyHost,
                        intfDict=myDict_sr_03, privateDirs=privateDirs_sr_03)

    # sr_04
    sr_04_eth0 = {'ipAddrs': ['10.0.2.3'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:13'}
    privateDirs_sr_04 = [
        ('/opt/ts/etc/trafficserver', '/home/notroot/mininet-lab/topos/components/ats/configuration_01')]
    myDict_sr_04 = {'sr_04-eth0': sr_04_eth0}
    sr_04 = net.addHost("sr_04", cls=MyHost,
                        intfDict=myDict_sr_04, privateDirs=privateDirs_sr_04)

    # Region 03
    # sr_05
    sr_05_eth0 = {'ipAddrs': ['10.0.3.2'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:14'}
    privateDirs_sr_05 = [
        ('/opt/ts4/etc/trafficserver', '/home/notroot/mininet-lab/topos/components/ats/configuration_04')]
    myDict_sr_05 = {'sr_05-eth0': sr_05_eth0}
    sr_05 = net.addHost("sr_05", cls=MyHost,
                        intfDict=myDict_sr_05, privateDirs=privateDirs_sr_05)

    # sr_06
    sr_06_eth0 = {'ipAddrs': ['10.0.3.3'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:15'}
    myDict_sr_06 = {'sr_06-eth0': sr_06_eth0}
    sr_06 = net.addHost("sr_06", cls=MyHost, intfDict=myDict_sr_06)

    # Region 04
    # sr_07
    sr_07_eth0 = {'ipAddrs': ['10.0.4.2'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:16'}
    myDict_sr_07 = {'sr_07-eth0': sr_07_eth0}
    sr_07 = net.addHost("sr_07", cls=MyHost, intfDict=myDict_sr_07)

    # sr_08
    sr_08_eth0 = {'ipAddrs': ['10.0.4.3'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:17'}
    myDict_sr_08 = {'sr_08-eth0': sr_08_eth0}
    sr_08 = net.addHost("sr_08", cls=MyHost, intfDict=myDict_sr_08)

    # Region 05
    # sr_09
    sr_09_eth0 = {'ipAddrs': ['10.0.5.2'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:18'}
    myDict_sr_09 = {'sr_09-eth0': sr_09_eth0}
    sr_09 = net.addHost("sr_09", cls=MyHost, intfDict=myDict_sr_09)

    # sr_10
    sr_10_eth0 = {'ipAddrs': ['10.0.5.3'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:19'}
    myDict_sr_10 = {'sr_10-eth0': sr_10_eth0}
    sr_10 = net.addHost("sr_10", cls=MyHost, intfDict=myDict_sr_10)

    # sr_11
    sr_11_eth0 = {'ipAddrs': ['10.0.6.7'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:20'}
    myDict_sr_11 = {'sr_11-eth0': sr_11_eth0}
    sr_11 = net.addHost("sr_11", cls=MyHost, intfDict=myDict_sr_11)

    # sr_11
    sr_12_eth0 = {'ipAddrs': ['10.0.7.7'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:21'}
    myDict_sr_12 = {'sr_12-eth0': sr_12_eth0}
    sr_12 = net.addHost("sr_12", cls=MyHost, intfDict=myDict_sr_12)

    # sr_13
    sr_13_eth0 = {'ipAddrs': ['10.0.8.70'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:22'}
    myDict_sr_13 = {'sr_13-eth0': sr_13_eth0}
    sr_13 = net.addHost("sr_13", cls=MyHost, intfDict=myDict_sr_13)

    # sr_14
    sr_14_eth0 = {'ipAddrs': ['10.0.9.23'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:23'}
    myDict_sr_14 = {'sr_14-eth0': sr_14_eth0}
    sr_14 = net.addHost("sr_14", cls=MyHost, intfDict=myDict_sr_14)

    # sr_15
    sr_15_eth0 = {'ipAddrs': ['10.0.10.35'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:24'}
    myDict_sr_15 = {'sr_15-eth0': sr_15_eth0}
    sr_15 = net.addHost("sr_15", cls=MyHost, intfDict=myDict_sr_15)

    # sr_16
    sr_16_eth0 = {'ipAddrs': ['10.0.11.40'],
                  'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:25'}
    myDict_sr_16 = {'sr_16-eth0': sr_16_eth0}
    sr_16 = net.addHost("sr_16", cls=MyHost, intfDict=myDict_sr_16)

    # Client01
    client_01_eth0 = {'ipAddrs': ['10.0.1.5'],
                      'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:26'}
    myDict_client_01 = {'client_01-eth0': client_01_eth0}
    client_01 = net.addHost("client_01", cls=MyHost, intfDict=myDict_client_01)

    # Client02
    client_02_eth0 = {'ipAddrs': ['10.0.1.6'],
                      'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:27'}
    myDict_client_02 = {'client_02-eth0': client_02_eth0}
    client_02 = net.addHost("client_02", cls=MyHost, intfDict=myDict_client_02)

    # MAR
    mar_eth0 = {'ipAddrs': ['10.0.1.7'],
                'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:28'}
    myDict_mar = {'mar-eth0': mar_eth0}
    mar = net.addHost("mar", cls=MyHost, intfDict=myDict_mar,
                      defaultRoute='10.0.0.1')

    # Topology
    topology_eth0 = {'ipAddrs': ['10.0.1.8'],
                     'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:29'}
    myDict_topology = {'topology-eth0': topology_eth0}
    topology = net.addHost("topology", cls=MyHost, intfDict=myDict_topology)

    # Consul
    consul_eth0 = {'ipAddrs': ['10.0.1.9'],
                   'mask': '255.0.0.0', 'gateway': '10.0.0.1', 'mac': 'B6:29:CE:E1:DB:30'}
    myDict_consul = {'consul-eth0': consul_eth0}
    consul = net.addHost("consul", cls=MyHost, intfDict=myDict_consul)

    info('*** Add links\n')
    # Between switches
    # Region 1
    net.addLink(s1, s2, bw=100, delay='25us')
    net.addLink(s2, s3, bw=100, delay='25us')
    net.addLink(s3, s4, bw=100, delay='25us')
    net.addLink(s4, s1, bw=100, delay='25us')
    # Region 2
    net.addLink(s5, s6, bw=100, delay='25us')
    net.addLink(s6, s7, bw=100, delay='25us')
    net.addLink(s7, s8, bw=100, delay='25us')
    net.addLink(s8, s5, bw=100, delay='25us')
    # Region 3
    net.addLink(s9, s10, bw=100, delay='25us')
    net.addLink(s10, s11, bw=100, delay='25us')
    net.addLink(s11, s12, bw=100, delay='25us')
    net.addLink(s12, s9, bw=100, delay='25us')
    # Region 4
    net.addLink(s13, s14, bw=100, delay='25us')
    net.addLink(s14, s15, bw=100, delay='25us')
    net.addLink(s15, s16, bw=100, delay='25us')
    net.addLink(s16, s13, bw=100, delay='25us')
    # Links between regions
    net.addLink(s3, s13, bw=1000, delay='250us')
    net.addLink(s14, s12, bw=1000, delay='250us')
    net.addLink(s7, s9, bw=1000, delay='250us')
    net.addLink(s8, s2, bw=1000, delay='250us')

    # s1
    net.addLink(s1, root, bw=100, delay='25us')
    net.addLink(s1, mar, bw=100, delay='25us')
    net.addLink(s1, topology, bw=100, delay='25us')
    net.addLink(s1, consul, bw=100, delay='25us')

    # Replication servers
    net.addLink(s4, sr_01, bw=100, delay='25us')
    net.addLink(s5, sr_02, bw=100, delay='25us')
    net.addLink(s8, sr_16, bw=100, delay='25us')
    net.addLink(s9, sr_10, bw=100, delay='25us')
    net.addLink(s10, sr_03, bw=100, delay='25us')
    net.addLink(s15, sr_04, bw=100, delay='25us')
    net.addLink(s16, sr_05, bw=100, delay='25us')
    net.addLink(s11, sr_06, bw=100, delay='25us')
    net.addLink(s12, sr_07, bw=100, delay='25us')
    net.addLink(s13, sr_08, bw=100, delay='25us')
    net.addLink(s14, sr_09, bw=100, delay='25us')
    net.addLink(s3, sr_11, bw=100, delay='25us')
    net.addLink(s2, sr_12, bw=100, delay='25us')
    net.addLink(s1, sr_13, bw=100, delay='25us')
    net.addLink(s6, sr_14, bw=100, delay='25us')
    net.addLink(s7, sr_15, bw=100, delay='25us')

    # Clients
    net.addLink(s16, client_01, bw=100, delay='25us')
    net.addLink(s15, client_02, bw=100, delay='25us')

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
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    net.get('s8').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    net.get('s11').start([c0])
    net.get('s12').start([c0])
    net.get('s13').start([c0])
    net.get('s14').start([c0])
    net.get('s15').start([c0])
    net.get('s16').start([c0])

    info('*** Post configure switches and hosts\n')
    # mar.cmd('ifconfig')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
