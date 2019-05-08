from ..Structural_node import Structural_node


def create_inst(parent):
    return Test_dsp_wrap_node(parent)

class Test_dsp_wrap_node(Structural_node):
    def __init__(self, parent):
        super(Test_dsp_wrap_node, self).__init__("dsp_wrap", parent)
        self._initialize()

################################################################################
# cheats
################################################################################

    def _initialize(self):
        dsp0=self.create_node("Test_dsp0_node")
        dsp1=self.create_node("Test_dsp1_node")

        self.connect(
            "{}.output".format(dsp0.name),
            "{}.input".format(dsp1.name)
        )

        self.add_portgroup("data")

        self.connect(".data", "{}.input".format(dsp0.name))
        self.connect(".data", "{}.cfg_in".format(dsp0.name))
        self.connect(".data", "{}.cfg_out".format(dsp0.name))

        self.connect(".data", "{}.output".format(dsp1.name))
        self.connect(".data", "{}.cfg_in".format(dsp1.name))
        self.connect(".data", "{}.cfg_out".format(dsp1.name))
