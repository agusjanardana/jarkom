#!/usr/bin/python3.8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink, Link
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os
import time

class LinuxRouter( Node ):
	"""A Node with IP forwarding enabled.
	Means that every packet that is in this node, comunicate freely with its interfaces."""

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
# """	
# creates the following topology	
# +--+10.0.0.1              10.0.0.2+--+10.0.1.1              10.0.1.2+--+	
# |r1+------------------------------+r2+------------------------------+r3|	
# +--+                              +--+                              +--+	
# """

# """"""""""""""""""""""""""""""""""
# 
#  MININET 4 ROUTE WITH 2 HOST 
#  I GDE BAGUS JANARDANA ABASAN
#  1301190061
# 
# ""
    def build(self,**_opts):
        
        hA = self.addHost('hA', ip='172.16.0.0/24')
        hB = self.addHost('hB', ip='172.16.0.0/24')
      	
       #membuat router
       	r1 = self.addNode('r1', cls=LinuxRouter, ip='172.16.0.0/24')
       	r2 = self.addNode('r2', cls=LinuxRouter, ip='172.16.0.0/24')
        r3 = self.addNode('r3', cls=LinuxRouter, ip='172.16.0.0/24')
        r4 = self.addNode('r4', cls=LinuxRouter, ip='172.16.0.0/24')
        
        #add link setiap route dan host
        self.addLink(hA,r1, cls=TCLink, intfName1='hA-eth0', intfName2='r1-eth0', bw=1)
        self.addLink(hA,r2, cls=TCLink, intfName1='hA-eth1', intfName2='r2-eth0', bw=1)
        self.addLink(hB,r3, cls=TCLink, intfName1='hB-eth0', intfName2='r3-eth0', bw=1)
        self.addLink(hB,r4, cls=TCLink, intfName1='hB-eth1', intfName2='r4-eth0', bw=1)
        
        #add link antar route
        self.addLink(r1,r3, cls=TCLink, intfName1='r1-se3', intfName2='r3-se3', bw=0.5)
        self.addLink(r1,r4, cls=TCLink, intfName1='r1-se2', intfName2='r4-se2', bw=1)
        self.addLink(r2,r3, cls=TCLink, intfName1='r2-se2', intfName2='r3-se2', bw=1)
        self.addLink(r2,r4, cls=TCLink, intfName1='r2-se3', intfName2='r4-se3', bw=0.5)
       
	  

def runTopo():
    os.system('mn-c')
    os.system('clear')
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    
    # mendapatkan data host
    hA,hB,r1,r2,r3,r4 = net.get('hA','hB','r1','r2','r3','r4')
    
    # Nambahin IP pada router-router yang tersedia
    r1.cmd('ifconfig r1-eth0 0')
    r1.cmd('ifconfig r1-se2 0')
    r1.cmd('ifconfig r1-se3 0')
    r1.cmd( 'ifconfig r1-eth0 172.16.0.1/24' ) #artinya tambahin ip route dengan prefix 24 dan ke ethernet0
    r1.cmd( 'ifconfig r1-se2 172.16.4.1/30' ) # artinya nambahin ip dengan prefix 30 ke serial2
    r1.cmd( 'ifconfig r1-se3 172.16.4.5/30' ) 
    
    r2.cmd('ifconfig r2-eth0 0')
    r2.cmd('ifconfig r2-se2 0')
    r2.cmd('ifconfig r2-se3 0')
    r2.cmd('ifconfig r2-eth0 172.16.1.1/24 ')
    r2.cmd('ifconfig r2-se2 172.16.4.9/30  ')
    r2.cmd('ifconfig r2-se3 172.16.4.13/30 ')
    
    r3.cmd('ifconfig r3-eth0 0')
    r3.cmd('ifconfig r3-se2 0')
    r3.cmd('ifconfig r3-se3 0')
    r3.cmd( 'ifconfig r3-eth0 172.16.2.1/24 ')
    r3.cmd( 'ifconfig r3-se3 172.16.4.6/30 ')
    r3.cmd( 'ifconfig r3-se2 172.16.4.10/30 ')
    
    r4.cmd('ifconfig r4-eth0 0')
    r4.cmd('ifconfig r4-se2 0')
    r4.cmd('ifconfig r4-se3 0')
    r4.cmd( 'ifconfig r4-eth0 172.16.3.1/24 ')
    r4.cmd( 'ifconfig r4-se2 172.16.4.2/30 ')
    r4.cmd( 'ifconfig r4-se3 172.16.4.14/30 ')
    
    #sambungkan host dan route
    hA.cmd('ifconfig hA-eth0 0')
    hA.cmd('ifconfig hA-eth1 0')
    hA.cmd('ifconfig hA-eth0 172.16.0.2/24 ')
    hA.cmd('ifconfig hA-eth1 172.16.1.2/24 ')
    
    hB.cmd('ifconfig hB-eth0 0')
    hB.cmd('ifconfig hB-eth1 0')
    hB.cmd('ifconfig hB-eth0 172.16.2.2/24 ')
    hB.cmd('ifconfig hB-eth1 172.16.3.2/24 ')
    
    
    # proses routing r1
    r1.cmd('route add -net 172.16.2.0/24 gw 172.16.4.6')
    r1.cmd('route add -net 172.16.4.8/30 gw 172.16.4.6')
    r1.cmd('route add -net 172.16.3.0/24 gw 172.16.4.2')
    r1.cmd('route add -net 172.16.4.12/30 gw 172.16.4.2')
    r1.cmd('route add -net 172.16.1.0/24 gw 172.16.4.6')
    
    #proses routing r2
    r2.cmd('route add -net 172.16.2.0/24 gw 172.16.4.10')
    r2.cmd('route add -net 172.16.3.0/24 gw 172.16.4.14')
    r2.cmd('route add -net 172.16.4.0/30 gw 172.16.4.14')
    r2.cmd('route add -net 172.16.4.4/30 gw 172.16.4.10')
    r2.cmd('route add -net 172.16.0.0/24 gw 172.16.4.10')
    
    #proses routing r3
    r3.cmd('route add -net 172.16.0.0/24 gw 172.16.4.5')
    r3.cmd('route add -net 172.16.4.12/30 gw 172.16.4.9')
    r3.cmd('route add -net 172.16.1.0/24 gw 172.16.4.9')
    r3.cmd('route add -net 172.16.3.0/24 gw 172.165.4.5')
    r3.cmd('route add -net 172.16.4.0/30 gw 172.16.4.5')
    
    #proses routing r4
    r4.cmd('route add -net 172.16.4.8/30 gw 172.16.4.13')
    r4.cmd('route add -net 172.16.1.0/24 gw 172.16.4.13')
    r4.cmd('route add -net 172.16.0.0/24 gw 172.16.4.1')
    r4.cmd('route add -net 172.16.4.4/30 gw 172.16.4.1')
    r4.cmd('route add -net 172.16.2.0/24 gw 172.16.4.1')
    
    
    
    hA.cmd('ip rule add from 172.16.0.2 table 1')
    hA.cmd('ip rule add from 172.16.1.2 table 2')
    hA.cmd('ip route add 172.16.0.0/24 dev hA-eth0 scope link table 1')
    hA.cmd('ip route add default via 172.16.0.1 dev hA-eth0 table 1 ')
    hA.cmd('ip route add 172.16.1.0/24 dev hA-eth1 scope link table 2')
    hA.cmd('ip route add default via 172.16.1.1 dev hA-eth0 table 2')
    hA.cmd('ip route add default scope global nexthop via 172.16.0.1 dev hA-eth0')
    hA.cmd('ip route add default scope global nexthop via 172.16.1.1 dev hA-eth1')
    
    hB.cmd('ip rule add from 172.16.2.2 table 1')
    hB.cmd('ip rule add from 172.16.3.2 table 2')
    hB.cmd('ip route add 172.16.2.0/24 dev hB-eth0 scope link table 1')
    hB.cmd('ip route add default via 172.16.2.1 dev hB-eth0 table 1')
    hB.cmd('ip route add 172.16.3.0/24 dev hB-eth1 scope link table 2')
    hB.cmd('ip route add default via 172.16.3.1 dev hB-eth1 table 2')
    hB.cmd('ip route add default scope global nexthop via 172.16.2.1 dev hB-eth0')
    hB.cmd('ip route add default scope global nexthop via 172.16.3.1 dev hB-eth1')
    
    net.start()
    
    # info('\n',net.ping(),'\n')
    # TRACE ROUTE dari hA ke hB
    info( '\n*** TRACE ROUTE :\n' )
    hA.cmdPrint('traceroute 172.16.2.2')
    hA.cmdPrint('traceroute 172.16.3.2')
    
    #Traceroute dari hB ke HA
    hB.cmdPrint('traceroute 172.16.0.2')
    hB.cmdPrint('traceroute 172.16.1.2')
    
    info( '\n*** Queue Discipline untuk R1 :\n' )
    
    r1.cmdPrint('tc qdisc del dev r1-eth0 root')
    r1.cmdPrint('tc qdisc add dev r1-eth0 root netem delay 20ms')
    # 20 ms di ganti jadi 40,60,80,100 nanti.
    
    time.sleep(2)
    
    info('\n*** running iperf di server background :\n')
    hB.cmd('iperf -s &')
    hA.cmd('iperf -c 172.16.2.2 -t 90 &')
    
    time.sleep(2)
    
    
    CLI(net)
    net.stop()
    
    
if __name__=='__main__':
    setLogLevel('info')
    runTopo()