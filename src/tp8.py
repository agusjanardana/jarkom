from mininet.link import TCLink #import library TClink dari mininet.link
from mininet.topo import Topo #import library Topo dari mininet.topo

#nim 1301190061 berarti, 90061 diambil untuk mac, 90:06:10:00:00:01
class MyTopo(Topo): #membangun class myTopo dengan parameter Topo
    def build(self): # Sebuah method build dengan parameter self
        h1 = self.addHost('h1', ip='192.168.1.1/24', mac='90:06:10:00:00:01')
        h2 = self.addHost('h2', ip='192.168.1.2/24', mac='90:06:10:00:00:02')
        h3 = self.addHost('h3', ip='192.168.1.3/24', mac='90:06:10:00:00:03')
        h4 = self.addHost('h4', ip='192.168.1.4/24', mac='90:06:10:00:00:04')
        h5 = self.addHost('h5', ip='192.168.1.5/24', mac='90:06:10:00:00:05')
        #h1 sampai h5 adalah sebuah variable dimana ada ekspresi untuk addhost

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        #s1 sampai s5 adalah sebuah variable untuk membuat switch

        #dictionary dengan value untuk setlink, dimana value yang ditetapkan adalah bw, delay, dan juga loss.
        linkopt = {'bw' : 20 , 'delay' : '10ms', 'loss' : 5}

        #code dibawah sampai akhir adalah untuk menyambungkan host dan switch.
        self.addLink(s1, h1, cls =TCLink, **linkopt)
        self.addLink(s1, h2, cls =TCLink, **linkopt)
        self.addLink(s2, h3, cls =TCLink, **linkopt)
        self.addLink(s3, h4, cls =TCLink, **linkopt)
        self.addLink(s4, h5, cls =TCLink, **linkopt)
        self.addLink(s1, s2, cls =TCLink, **linkopt)
        self.addLink(s2, s3, cls =TCLink, **linkopt)
        self.addLink(s4, s1, cls =TCLink, **linkopt)

#inisialisasi class dengan fitur lambda.
topos = {'mytopo' : (lambda : MyTopo () ) }