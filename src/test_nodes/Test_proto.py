from ..Node_iface import Node_iface
from .Test_serdes_ar import Test_serdes_ar


def create_inst(parent):
    return Test_proto(parent)

class Test_proto(Node_iface):
    def __init__(self, parent):
        super(Test_proto, self).__init__("proto", parent)
        self._initialize()

    def update_from_port(self, port):
        pass

################################################################################
# cheats
################################################################################

    def _initialize(self):
        self.add_portgroup("from_serdes")

    def _dump_architecture_declarative(self):
        return ""

    def _dump_architecture_executive(self):
        return ""
