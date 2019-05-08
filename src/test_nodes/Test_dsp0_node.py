from ..Node_iface import Node_iface


def create_inst(parent):
    return Test_dsp0_node(parent)

class Test_dsp0_node(Node_iface):
    def __init__(self, parent):
        super(Test_dsp0_node, self).__init__("dsp0", parent)
        self.add_port("input","in")
        self.add_port("output", "out")
        self.add_port("cfg_in", "in")
        self.add_port("cfg_out", "out")

    def _dump_architecture_declarative(self):
        return "*architecture declarative for Test_dsp0_node\n"

    def _dump_architecture_executive(self):
        return "*architecture executive for Test_dsp0_node\n"
