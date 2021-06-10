from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

#nim 1301190061

class MyTopo(Topo):
    def __init__(self,**opts):
        Topo.__init__(self,**opts)

        #membuat objek host dari h1 sampai h6
        h1 = self.addHost('h1', ip = '192.168.1.1/24', mac='13:01:19:00:61:00:00:01') 
        h2 = self.addHost('h2', ip = '192.168.1.2/24', mac='13:01:19:00:61:00:00:02')
        h3 = self.addHost('h3', ip = '192.168.1.3/24', mac='13:01:19:00:61:00:00:03')
        h4 = self.addHost('h4', ip = '192.168.1.4/24', mac='13:01:19:00:61:00:00:04')
        h5 = self.addHost('h5', ip = '192.168.1.5/24', mac='13:01:19:00:61:00:00:05')
        h6 = self.addHost('h6', ip = '192.168.1.6/24', mac='13:01:19:00:61:00:00:06')

        #membuat objek switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        linkopt = {'bw' : 100} #set Bandwitchnya

        #link antar object
        self.addLink(s1,h1, cls=TCLink, **linkopt)
        self.addLink(s1,h2, cls=TCLink, **linkopt)
        self.addLink(s1,h3, cls=TCLink, **linkopt)
        self.addLink(s2,h6, cls=TCLink, **linkopt)
        self.addLink(s2,h5, cls=TCLink, **linkopt)
        self.addLink(s2,h4, cls=TCLink, **linkopt)
        self.addLink(s1,s1, cls=TCLink, **linkopt)



def runTopo():
    #memastikan mininet bersih dari cache sebelumnya
    os.system('mn -cc')

    #Membangun topologi
    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    #konfigurasi congestion control
    print (net['h1'].cmd('sysctl –w net.ipv4.tcp_congestion_control=reno'))
    print (net['h2'].cmd('sysctl -w net.ipv4.tcp_congestion_control=reno'))
    print (net['h3'].cmd('sysctl -w net.ipv4.tcp_congestion_control=reno'))
    print (net['h4'].cmd('sysctl -w net.ipv4.tcp_congestion_control=reno'))
    print (net['h5'].cmd('sysctl -w net.ipv4.tcp_congestion_control=reno'))
    print (net['h6'].cmd('sysctl -w net.ipv4.tcp_congestion_control=reno'))

    #memasukkan objek host pada variabel
    H1,H2,H3,H4,H5,H6 = net.get('h1','h2','h3','h4','h5','h6')

    #menjalankan Iperf pada background process
    H6.cmd('iperf -s&')
    H5.cmd('iperf -c 192.168.1.6&')
    H4.cmd('iperf -c 192.168.1.6&')
    H3.cmd('iperf -c 192.168.1.6&')
    H2.cmd('iperf -c 192.168.1.6&')
    H1.cmd('iperf -c 192.168.1.6 -i 1&')

    #Menampilkan hasil iPerf dari H1 ke H4
    H1.cmdPrint('fg')
    CLI(net)
    net.stop()

if __name__=='__main__':
       setLogLevel('info')
       runTopo()
topos = {'mytopo' : (lambda : MyTopo())}
