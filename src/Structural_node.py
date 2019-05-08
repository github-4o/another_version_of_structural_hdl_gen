from .Node_iface import Node_iface
from .Link import Link


class Structural_node(Node_iface):
    def __init__(self, name):
        super(Structural_node, self).__init__(name)
        self._nodes={}
        self._links=[]

################################################################################
# public
################################################################################

    def dump_hdl(self):
        ret=[(self.name+".vhd", self._dump_hdl())]
        for i in self._nodes:
            ret+=self._nodes[i].dump_hdl()
        return ret

    def connect(self, one, two):
        (node_one, port_one)=self._split_node_port(one)
        (node_two, port_two)=self._split_node_port(two)
        link=Link()
        self._links.append(link)
        self._connect(node_one, port_one, link)
        self._connect(node_two, port_two, link)
        # link.finalize()

################################################################################
# protected
################################################################################

# dump- related
    def _dump_architecture_declarative(self):
        return (
            self._dump_components()
            +self._dump_signals()
        )

    def _dump_components(self):
        ret=""
        for i in self._nodes:
            ret+=self._nodes[i].dump_component()+"\n"
        return ret

    def _dump_signals(self):
        ret=""
        for i in self._links:
            ret+=i.dump_signal()
        return ret

    def _dump_architecture_executive(self):
        ret=""
        for i in self._nodes:
            ret+=self._nodes[i]._dump_instance()+"\n"
        return ret

    def _split_node_port(self, node_port_string):
        ar=node_port_string.split(".", 2)

        if len(ar[0]) == 0:
            node=self
        else:
            if len(ar) != 2:
                raise Exception("split failed")
            if ar[0] not in self._nodes:
                raise Exception("failed to find node")
            node=self._nodes[ar[0]]

        return (node, ar[1])

    def _connect(self, node, port, link):
        if node == self:
            self.connect_int_port(port, link)
        else:
            node.connect_ext_port(port, link)
