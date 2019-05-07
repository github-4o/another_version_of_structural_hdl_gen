from ..Structural_node import Structural_node

from .Test_dsp1_node import Test_dsp1_node
from .Test_dsp0_node import Test_dsp0_node


class Test_dsp_wrap_node(Structural_node):
    def __init__(self):
        super(Test_dsp_wrap_node, self).__init__("test_dsp_wrap_node")
        self._initialize()

################################################################################
# cheats
################################################################################

    def _initialize(self):
        self._nodes["test_dsp0_node"]=Test_dsp0_node()
        self._nodes["test_dsp1_node"]=Test_dsp1_node()

        self.connect("test_dsp0_node.output", "test_dsp1_node.input")

        self.add_portgroup("data")

        self.connect(".data", "test_dsp0_node.input")
        self.connect(".data", "test_dsp0_node.cfg_in")
        self.connect(".data", "test_dsp0_node.cfg_out")
        self.connect(".data", "test_dsp1_node.output")
        self.connect(".data", "test_dsp1_node.cfg_in")
        self.connect(".data", "test_dsp1_node.cfg_out")
