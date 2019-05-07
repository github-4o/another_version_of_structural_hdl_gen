from ..Structural_node import Structural_node


class Test_comm_node(Structural_node):
    def __init__(self):
        super(Test_comm_node, self).__init__("test_comm_node")
        self._initialize()

################################################################################
# cheats
################################################################################

    def _initialize(self):
        self.add_portgroup("data")
