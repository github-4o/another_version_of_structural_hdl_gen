from ..Structural_node import Structural_node

from .Test_dsp_wrap_node import Test_dsp_wrap_node
from .Test_comm_node import Test_comm_node


class Test_top_structural_node(Structural_node):
    def __init__(self):
        super(Test_top_structural_node, self).__init__("test_top_node")
        self._initialize()

################################################################################
# cheats
################################################################################

    def _initialize(self):
        self._nodes["test_dsp_wrap_node"]=Test_dsp_wrap_node()
        self._nodes["test_comm_node"]=Test_comm_node()
        self.connect("test_comm_node.data", "test_dsp_wrap_node.data")
