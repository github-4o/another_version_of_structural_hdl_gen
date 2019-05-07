from .Port import Port


class Port_group:
    def __init__(self, parent, dynamic=False):
        self._dynamic=dynamic
        self._parent=parent
        self._bound_port_group=None
        self._ports=[]
        self._link=None

    @property
    def port_num(self):
        return len(self._ports)

    @property
    def name(self):
        return self._parent.get_port_name(self)

    @property
    def internal(self):
        return self._parent.is_internal(self)

    @property
    def bound_port_group(self):
        return self._bound_port_group.copy()

    @bound_port_group.setter
    def bound_port_group(self, val):
        if self._bound_port_group != None:
            raise Exception("attempt to modify bound port")
        self._bound_port_group=val

    def get_port_name(self, port):
        index=self._ports.index(port)

        return self._parent.get_port_name(self)+"_{}".format(index)

    def is_internal(self, port):
        try:
            self._ports.index(port)
            raise Exception("adding same port multiple times?")
        except:
            pass

        return self.internal

    def dump_ports(self, indent="        "):
        if len(self._ports) == 0:
            return indent+"{}: <port group with 0 ports> ;\n".format(self.name)
        else:
            ret=""
            for i in self._ports:
                ret+=i.dump_ports(indent)
            return ret

    def connect_to(self, port, link):
        if isinstance(port, Port):
            return self._connect_to_port(port, link)
        elif isinstance(port, Port_group):
            return self._connect_to_port_group(port, link)
        else:
            raise Exception("invalid type of port")

    def add_port_from_bound_port(self, portgroup):
        if self._bound_port_group != portgroup:
            raise Exception("this should never happen")

        self._ports.append(Port(self))

    def connect_subports(self):
        for i in self._ports:
            self._link.add_sublink(self, i) # remove self probably?

    def _connect_to_port(self, port, link):
        try:
            self._ports.index(port)
            raise Exception("adding same port multiple times?")
        except:
            pass

        new_port=Port(self)
        new_port=new_port.connect_to(port, link)
        self._ports.append(new_port)
        self._bound_port_group.add_port_from_bound_port(self)
        return new_port

    def _connect_to_port_group(self, portgroup, link):
        if self._link != None:
            raise Exception(
                "port reconnection detected {}\n".format(self.name)
                +" new connection {}\n".format(portgroup.name)
                +" old connection {}\n".format(self._link.other_name(self))
            )
        self._link=link
        return self

    def dump_inst_connection(self, indent):
        ret=""
        for i in self._ports:
            ret+=i.dump_inst_connection(indent)
        return ret
