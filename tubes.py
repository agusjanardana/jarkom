#!/usr/bin/python3.8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink, Link
from mininet.cli import CLI
import os


class LinuxRouter(Node):
	def config(self,**params):
		super(LinuxRouter, self).config(**params)
		self.cmd('sysctl net.ipv4.ip_forward=1')
	
	def terminate(self):
		self.cmd('sysctl net.ipv4.ip_forward=0')
		super(LinuxRouter,self).terminate()

class NetworkTopo(Topo):
	def build(self,**_opts):
		# Membuat host
		#hA = self.addHost('hA', ip='192.168.0.18/30', defaultRoute='via 192.168.0.17')
		#hB = self.addHost('hB', ip='192.168.0.22/30', defaultRoute='via 192.167.0.21')
		hA = self.addHost('hA')
		hB = self.addHost('hB')
		
		# Membuat router
		#r1 = self.addNode('r1', cls=LinuxRouter, ip='192.168.0.17/30')
		#r2 = self.addNode('r2', cls=LinuxRouter, ip='192.168.t0.9/30')
		#r3 = self.addNode('r3', cls=LinuxRouter, ip='192.168.0.2/30')
		#r4 = self.addNode('r4', cls=LinuxRouter, ip='192.168.0.13/30')
		r1 = self.addNode('r1', cls=LinuxRouter)
		r2 = self.addNode('r2', cls=LinuxRouter)
		r3 = self.addNode('r3', cls=LinuxRouter)
		r4 = self.addNode('r4', cls=LinuxRouter)
		
		# Membuat link host-router
		self.addLink(hA,r1, intfName2='r1-eth0', params1={'bw': 1, 'ip' : '192.168.0.2/30' }, params2={'bw': 1, 'ip' : '192.168.0.1/30' })
		self.addLink(hA,r2, intfName2='r2-eth0', params1={'bw': 1, 'ip' : '192.168.0.2/30' }, params2={'bw': 1, 'ip' : '192.168.0.5/30' })
		self.addLink(hB,r3, intfName2='r3-eth0', bw=1)
		self.addLink(hB,r4, intfName2='r4-eth0', bw=1)
		
		# Membuat link router-router
		self.addLink(r1,r3, intfName1='r1-eth1', intfName2='r3-eth1', bw=0.5)
		self.addLink(r1,r4, intfName1='r1-eth2', intfName2='r4-eth1', bw=1)
		self.addLink(r2,r3, intfName1='r2-eth1', intfName2='r3-eth2', bw=1)
		self.addLink(r2,r4, intfName1='r2-eth2', intfName2='r4-eth2', bw=0.5)
        
def runTopo():
	os.system('mn -c')
	os.system('clear')
	topo = NetworkTopo()
	net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
	net.start()
	
	hA,hB = net.get('hA','hB')
	
	hA.cmd('iperf -c 192.168.0.22')
	hB.cmd('iperf -c 192.168.0.18')
	hA.cmdPrint('fg')
	hB.cmdPrint('fg')
	CLI(net)
	net.stop()
	
	
	
if __name__=='__main__':
	runTopo()