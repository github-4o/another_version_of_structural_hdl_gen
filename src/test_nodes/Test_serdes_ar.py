from ..Behavioral_node import Behavioral_node
from ..Port import invert_dir


def create_inst(parent):
    return Test_serdes_ar(parent)

class Test_serdes_ar(Behavioral_node):
    def __init__(self, parent):
        super(Test_serdes_ar, self).__init__("serdes_ar", parent)
        self._initialize()

    def update_from_port(self, port):
        print("***hit:", port)
        if port=="data":
            len_source=self._ext_port_groups["data"].port_num
            len_sink=self._ext_port_groups["to_proto"].port_num
            print("****node {}: updating from port {}. {}:{}".format(
                self.hierarchial_name, port, len_source, len_sink))
            if len_source > len_sink:
                print ("adding {} more ports".format(
                    len_source, len_sink, len_source-len_sink
                ))
                one_sied_ports=self._int_port_groups["data"].get_unconnected_ports(self)
                # for i in one_sied_ports:
                #     self._int_port_groups["to_proto"].add_subport(
                #         self, invert_dir(i.dir))

################################################################################
# cheats
################################################################################

    def _initialize(self):
        self.add_portgroup("data")
        self.add_portgroup("to_proto")

    def _dump_architecture_declarative(self):
        return ""

    def _dump_architecture_executive(self):
        return ""
