from .Port import Port
from .service.Reporter import reporter


class Port_group:
    def __init__(self, parent):
        self._parent=parent
        self._bound_port_group=None
        self._ports=[]
        self._link=None
        self._REPORT=False

    @property
    def port_num(self):
        return len(self._ports)

    @property
    def name(self):
        return self._parent.get_port_name(self)

    @property
    def hierarchial_name(self):
        if self.internal:
            add="(int)"
        else:
            add="(ext)"
        return self._parent.hierarchial_name+"."+self.name+add

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

    def add_subport(self, parent, dir):
        if parent != self._parent:
            raise Exception("this should never happen")
        port=Port(self)
        self._ports.append(port)
        self._bound_port_group.add_port_from_bound_port(self, port)

    def get_unconnected_ports(self, link):
        if link != self._link and link != self._parent:
            raise Exception("unauthorized port request")

        ret=[]
        for i in self._ports:
            if i.is_unconnected:
                ret.append(i)
        return ret

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

    def connect_to(self, link):
        reporter.print(
            "portgroup {}: connected to link {}",
            [self.hierarchial_name, link.hierarchial_name]
        )
        ret=None
        port=link.other_port(self)
        if isinstance(port, Port):
            ret=self._connect_to_port(link)
        elif isinstance(port, Port_group):
            ret=self._connect_to_port_group(port, link)
        else:
            raise Exception("invalid type of port: {}".format(port))
        reporter.less_indent()
        return ret

    # get a list of ports from the other port_group
    # get non-binded ports
    # return a list of new links
    def update_from_link(self):
        reporter.print(
            "portgroup {}: updating form link {}",
            [self.hierarchial_name, self._link.hierarchial_name]
        )
        if self._link == None:
            raise Exception("this should never happen")

        for i in self._ports:
            i.update_from_link()

        self._bound_port_group.update_from_bound_port(self)
        reporter.less_indent()

    def update_from_bound_port(self, bound_port):
        if self._bound_port_group != bound_port:
            raise Exception("this should never happen")

        reporter.print(
            "portgroup {}: pulling from bound port {}",
            [self.hierarchial_name, self._bound_port_group.hierarchial_name]
        )
        if self._link != None:
            self._link.propagate(self)
        reporter.less_indent()

    def add_port_from_bound_port(self, portgroup, port):
        reporter.print(
            "portgroup {}: updating bound port {}",
            [self.hierarchial_name, self._bound_port_group.hierarchial_name]
        )
        if self._bound_port_group != portgroup:
            raise Exception("this should never happen")

        new_port=Port(self)
        new_port.bound_port=port
        self._ports.append(new_port)
        port.bound_port=new_port
        reporter.less_indent()
        if self.internal == True:
            self._parent.update_from_port(self.name)

    def _connect_to_port(self, link):
        new_port=Port(self)
        self._ports.append(new_port)
        new_port.connect_to(link)
        bount_port=self._bound_port_group.add_port_from_bound_port(self, new_port)
        return new_port

    def _connect_to_port_group(self, portgroup, link):
        # if self.hierarchial_name == "top_0.comm_0.data(int)":
        #     raise Exception("this should never happen")
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
