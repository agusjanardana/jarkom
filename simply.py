from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


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
"""	
creates the following topology	
+--+10.0.0.1              10.0.0.2+--+10.0.1.1              10.0.1.2+--+	
|r1+------------------------------+r2+------------------------------+r3|	
+--+                              +--+                              +--+	
"""
	def build( self, **_opts ):
		

		r1=self.addNode("r1",cls=LinuxRouter,ip=None)
		r2=self.addNode("r2",cls=LinuxRouter,ip=None)
		r3=self.addNode("r3",cls=LinuxRouter,ip=None)

		self.addLink(r1,r2,params1={ 'ip' : '10.0.0.1/24' },params2={ 'ip' : '10.0.0.2/24' })
		self.addLink(r2,r3,params1={ 'ip' : '10.0.1.1/24' },params2={ 'ip' : '10.0.1.2/24' })

topo = NetworkTopo()
net = Mininet( topo=topo )
net.start()

#ip route add ipA via ipB dev INTERFACE
#every packet going to ipA must first go to ipB using INTERFACE
net["r1"].cmd("ip route add 10.0.1.2 via 10.0.0.2 dev r1-eth0")
net["r3"].cmd("ip route add 10.0.0.1 via 10.0.1.1 dev r3-eth0")
#this command is just to r3 ping r2 work, because it will use the correct ip
net["r3"].cmd("ip route add 10.0.0.2 via 10.0.1.1 dev r3-eth0")
net.pingAll()
CLI( net )
net.stop()