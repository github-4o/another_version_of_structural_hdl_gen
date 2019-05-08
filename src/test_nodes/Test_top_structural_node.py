from ..Structural_node import Structural_node


class Test_top_structural_node(Structural_node):
    def __init__(self):
        super(Test_top_structural_node, self).__init__("top", None)
        self._initialize()

################################################################################
# cheats
################################################################################

    def _initialize(self):
        dsp_wrap_node=self.create_node("Test_dsp_wrap_node")
        comm_node=self.create_node("Test_comm_node")
        self.connect(
            "{}.data".format(comm_node.name),
            "{}.data".format(dsp_wrap_node.name)
        )
