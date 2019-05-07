from ..Node_iface import Node_iface


class Test_dsp1_node(Node_iface):
    def __init__(self):
        super(Test_dsp1_node, self).__init__("test_dsp1_node")
        self.add_port("input", "in")
        self.add_port("output", "out")
        self.add_port("cfg_in", "in")
        self.add_port("cfg_out", "out")

    def _dump_architecture_declarative(self):
        return "*architecture declarative for Test_dsp1_node\n"

    def _dump_architecture_executive(self):
        return "*architecture executive for Test_dsp1_node\n"
