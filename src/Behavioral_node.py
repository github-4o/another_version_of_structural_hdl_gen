from .Node_iface import Node_iface


class Behavioral_node(Node_iface):
    def __init__(self, name, parent):
        super(Behavioral_node, self).__init__(name, parent)
