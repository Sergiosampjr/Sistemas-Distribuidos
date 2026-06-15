from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink


class DroneTopo(Topo):
    def build(self):
        switch = self.addSwitch("s1", failMode="standalone")

        for i in range(1, 11):
            host = self.addHost("h{}".format(i), ip="10.0.0.{}/24".format(i))
            self.addLink(host, switch)


if __name__ == "__main__":
    topo = DroneTopo()

    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=None,
        link=TCLink,
        autoSetMacs=True
    )

    net.start()
    CLI(net)
    net.stop()
