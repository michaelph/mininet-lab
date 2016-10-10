#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
from mininet.node import Host
import logging
import os
import json

from bottle import route, run

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
topo = "topology_object"
net = "net_object"


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


class FatTopo(Topo):
    logger.debug("Class FatTopo")
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    HostList = []
    iNUMBER = 0

    def __init__(self):
        logger.debug("Class FatTopo init")
        iNUMBER = 4

        self.iNUMBER = iNUMBER
        self.iCoreLayerSwitch = iNUMBER
        self.iAggLayerSwitch = iNUMBER * 2
        self.iEdgeLayerSwitch = iNUMBER * 2
        self.iHost = self.iEdgeLayerSwitch * 2
        # Init Topo
        Topo.__init__(self)

    def createTopo(self):
        logger.debug("Start create Core Layer Swich")
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        logger.debug("Start create Agg Layer Swich ")
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        logger.debug("Start create Edge Layer Swich ")
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        logger.debug("Start create Host")
        self.createHost(self.iHost)

    """
    Create Switch and Host
    """

    def createCoreLayerSwitch(self, NUMBER):
        logger.debug("Create Core Layer")
        for x in range(1, NUMBER + 1):
            PREFIX = "100"
            if x >= int(10):
                PREFIX = "10"
            self.CoreSwitchList.append(self.addSwitch(PREFIX + str(x)))

    def createAggLayerSwitch(self, NUMBER):
        logger.debug("Create Agg Layer")
        for x in range(1, NUMBER + 1):
            PREFIX = "200"
            if x >= int(10):
                PREFIX = "20"
            self.AggSwitchList.append(self.addSwitch(PREFIX + str(x)))

    def createEdgeLayerSwitch(self, NUMBER):
        logger.debug("Create Edge Layer")
        for x in range(1, NUMBER + 1):
            PREFIX = "300"
            if x >= int(10):
                PREFIX = "30"
            self.EdgeSwitchList.append(self.addSwitch(PREFIX + str(x)))

    def createHost(self, NUMBER):
        logger.debug("Create Host")
        # root
        root_eth0 = {'ipAddrs': ['10.0.0.1'], 'mask': '255.0.0.0', 'gateway': '10.0.0.1'}
        myDict_root = {'root-eth0': root_eth0}
        root = self.addHost("root", cls=MyHost, inNamespace=False, intfDict=myDict_root)
        self.HostList.append(root)
        for x in range(2, NUMBER + 2):
            PREFIX = "400"
            if x >= int(10):
                PREFIX = "40"
            hostname = PREFIX + str(x)
            eth0 = {'ipAddrs': ['10.0.0.' + str(x)], 'mask': '255.0.0.0', 'gateway': '10.0.0.1'}
            myDict = {hostname + '-eth0': eth0}
            self.HostList.append(self.addHost(hostname, cls=MyHost, intfDict=myDict))

    """
    Create Link
    """
    def createLink(self):
        logger.debug("Create Core to Agg")
        self.addLink(self.CoreSwitchList[0], self.HostList[0], bw=1000)
        for x in range(0, self.iAggLayerSwitch, 2):
            self.addLink(self.CoreSwitchList[0], self.AggSwitchList[x], bw=1000)
            self.addLink(self.CoreSwitchList[1], self.AggSwitchList[x], bw=1000)
        for x in range(1, self.iAggLayerSwitch, 2):
            self.addLink(self.CoreSwitchList[2], self.AggSwitchList[x], bw=1000)
            self.addLink(self.CoreSwitchList[3], self.AggSwitchList[x], bw=1000)

        logger.debug("Create Agg to Edge")
        for x in range(0, self.iAggLayerSwitch, 2):
            self.addLink(self.AggSwitchList[x], self.EdgeSwitchList[x], bw=1000)
            self.addLink(self.AggSwitchList[x], self.EdgeSwitchList[x + 1], bw=1000)
            self.addLink(self.AggSwitchList[x + 1], self.EdgeSwitchList[x], bw=1000)
            self.addLink(self.AggSwitchList[x + 1], self.EdgeSwitchList[x + 1], bw=1000)

        logger.debug("Create Edge to Host")
        for x in range(0, self.iEdgeLayerSwitch):
            # limit = 2 * x + 1
            self.addLink(self.EdgeSwitchList[x], self.HostList[2 * x], bw=1000)
            self.addLink(self.EdgeSwitchList[x], self.HostList[2 * x + 1], bw=1000)


def enableSTP():
    """
    //HATE: Dirty Code
    """
    for x in range(1, 5):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % ("100" + str(x))
        os.system(cmd)
        print cmd

    for x in range(1, 9):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % ("200" + str(x))
        os.system(cmd)
        print cmd
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % ("300" + str(x))
        os.system(cmd)
        print cmd


def iperfTest(net, topo):
    logger.debug("Start iperfTEST")
    h1000, h1015, h1016 = net.get(topo.HostList[0], topo.HostList[14], topo.HostList[15])

    # iperf Server
    h1000.popen('iperf -s -u -i 1 > iperf_server_differentPod_result', shell=True)

    # iperf Server
    h1015.popen('iperf -s -u -i 1 > iperf_server_samePod_result', shell=True)

    # iperf Client
    h1016.cmdPrint('iperf -c ' + h1000.IP() + ' -u -t 10 -i 1 -b 100m')
    h1016.cmdPrint('iperf -c ' + h1015.IP() + ' -u -t 10 -i 1 -b 100m')


def pingTest(net):
    logger.debug("Start Test all network")
    net.pingAll()


def createTopo():
    logging.debug("Create FatTopo")
    global topo
    topo = FatTopo()
    topo.createTopo()
    topo.createLink()

    logging.debug("Start Mininet")
    CONTROLLER_IP = "127.0.0.1"
    CONTROLLER_PORT = 6633
    global net
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController('controller', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    net.start()

    logger.debug("dumpNode")
    # enableSTP()
    dumpNodeConnections(net.hosts)

    # pingTest(net)
    # iperfTest(net, topo)
    root = net.get(topo.HostList[0])
    root.cmd('java -jar ../ncintents-bridge.jar 9000 &')

    run(host='172.20.4.112', port=8080)
    CLI(net)
    net.stop()


@route('/register')
def register():
    host1 = net.get(topo.HostList[0])
    host2 = net.get(topo.HostList[1])
    request = {"ncTrafficClassId": "0",
               "mainNcFlow": {"source": "srcMac1", "destination": "dstMac1",
                              "destinationPort": "3456", "sourcePort": "4000",
                              "burst": "23", "rate": "12", "type": "TCP"
                              },
               "ackNcFlow": {"source": "srcMac", "destination": "srcMac",
                             "destinationPort": "43", "sourcePort": "34",
                             "burst": "45", "rate": "56", "type": "UDP"
                             },
               "maxLatencyAllowed": "120"
               }
    requestJson = "'" + json.dumps(request, ensure_ascii=False) + "'"
    host2.cmd("echo " + requestJson + " | telnet 172.20.4.112 9000")
    return "Sent: '" + json.dumps(request, ensure_ascii=False) + "'"


@route('/cli/<host>/<command>')
def cli(host='root', command='ls'):
    return net.get(host).cmd(command)


@route('/info/<host>')
def info(host='host1'):
    hostname = net.get(host).name
    hostMac = net.get(host).MAC()
    hostIp = net.get(host).IP()
    hostDict = {'hostname': hostname, 'hostmac': hostMac, 'hostip': hostIp}
    return json.dumps(hostDict, ensure_ascii=False)


if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        logger.debug("You are NOT root")
    elif os.getuid() == 0:
        createTopo()
