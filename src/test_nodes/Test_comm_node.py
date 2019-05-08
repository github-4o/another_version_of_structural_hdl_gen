from ..Structural_node import Structural_node
from .Test_serdes_ar import Test_serdes_ar


def create_inst(parent):
    return Test_comm_node(parent)

class Test_comm_node(Structural_node):
    def __init__(self, parent):
        super(Test_comm_node, self).__init__("comm", parent)
        self._initialize()

    def update_from_port(self, port):
        pass

################################################################################
# cheats
################################################################################

    def _initialize(self):
        serdes=self.create_node("Test_serdes_ar")
        proto=self.create_node("Test_proto")
        self.add_portgroup("data")
        self.connect(".data", "{}.data".format(serdes.name))
        self.connect(
            "{}.to_proto".format(serdes.name),
            "{}.from_serdes".format(proto.name)
        )
