import os
from importlib import import_module

from .Node_iface import Node_iface
from .Link import Link
from .service.Reporter import reporter


class Structural_node(Node_iface):
    def __init__(self, name, parent):
        super(Structural_node, self).__init__(name, parent)
        self._nodes={}
        self._links=[]

################################################################################
# public
################################################################################

    def create_node(self, name):
        reporter.print(
            "node {}: creating node {}", [self.hierarchial_name, name]
        )
        module=self._load_module(name)
        inst=module.create_inst(self)
        if inst.name in self._nodes:
            raise Exception("this should never happen")
        self._nodes[inst.name]=inst
        reporter.less_indent()
        return inst

    def dump_hdl(self):
        ret=[(self.name+".vhd", self._dump_hdl())]
        for i in self._nodes:
            ret+=self._nodes[i].dump_hdl()
        return ret

    def connect(self, one, two):
        reporter.print(
            "node {}: connecting {} and {}", [self.hierarchial_name, one, two]
        )
        (node_one, port_one)=self._split_node_port(one)
        (node_two, port_two)=self._split_node_port(two)
        link=Link(self)
        self._links.append(link)
        # this is a transaction == source of possible failures
        self._connect(node_one, port_one, link)
        self._connect(node_two, port_two, link)
        reporter.less_indent()

    def update_from_port(self, port):
        pass

################################################################################
# protected
################################################################################

    def _load_module(self, prototype):
        p=os.path.dirname(os.path.relpath(__file__))
        modulename=p+".test_nodes."+prototype
        # print("loading prototype for {} ({})".format(prototype, modulename))
        # print("loading module {}".format(modulename))
        return import_module(modulename)

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
                raise Exception("failed to find node", ar[0])
            node=self._nodes[ar[0]]

        return (node, ar[1])

    def _connect(self, node, port, link):
        if node == self:
            self.connect_int_port(port, link)
        else:
            node.connect_ext_port(port, link)
