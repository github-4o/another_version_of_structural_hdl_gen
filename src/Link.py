from .Port import Port
from .Port_group import Port_group
from .service.Reporter import reporter


class Link:
    __number=0

    @classmethod
    def _get_number(cls):
        ret=cls.__number
        cls.__number+=1
        return ret

    def __init__(self, parent):
        self._name="s{}".format(self.__class__._get_number())
        self._one=None
        self._two=None
        self._sublinks=None
        self._parent=parent
        self._lock=False

    @property
    def name(self):
        return self._name[:]

    @property
    def hierarchial_name(self):
        if self._parent == None:
            return self.name
        else:
            return self._parent.hierarchial_name+"."+self.name

##########################
# this is a mess right now
    def register(self, port, update_other_port=True):
        if self._lock == True:
            raise Exception("loop detected")

        if self._one == None:
            reporter.print(
                "link {}: connecting first port {}",
                [self.hierarchial_name, port.hierarchial_name]
            )
            self._one=port
        elif self._two == None:
            reporter.print(
                "link {}: connecting second port {}",
                [self.hierarchial_name, port.hierarchial_name]
            )
            self._two=port
            if isinstance(self._one, Port):
                if isinstance(self._two, Port):
                    self._connect_port_port(self._one, self._two)
                elif isinstance(self._two, Port_group):
                    self._connect_port_group(self._one, self._two)
                else:
                    raise Exception("this should never happen")
            elif isinstance(self._one, Port_group):
                if isinstance(self._two, Port):
                    self._connect_port_group(self._two, self._one)
                elif isinstance(self._two, Port_group):
                    self._connect_group_group(self._one, self._two)
                else:
                    raise Exception("this should never happen")
            else:
                raise Exception("this should never happen")
            self._lock=True
            if update_other_port == True:
                self._one.update_from_link()
            self._two.update_from_link()
            self._lock=False
        else:
            raise Exception("this should never happen")
        reporter.less_indent()

    def update_other_port(self, port):
        if port == self._one:
            if self._two == None:
                raise Exception("this should never happen")
            self._two.update_from_link()
        elif port == self._two:
            if self._one == None:
                raise Exception("this should never happen")
            self._one.update_from_link()
        else:
            raise Exception("this should never happen")

    def propagate(self, portgroup):
        if self._one != portgroup and self._two != portgroup:
            raise Exception("this should never happen")

        check1=isinstance(self._one, Port_group)
        check2=isinstance(self._two, Port_group)

        if check1 == False or check2 == False:
            raise Exception("this should never happen")

        self._connect_group_group_ordered(
            self.other_port(portgroup), portgroup, False
        )

    def _connect_port_port(self, portA, portB):
        self._one=portA
        self._two=portB
        self._one.connect_to(self)
        self._two.connect_to(self)

    def _connect_port_group(self, port, group):
        self._one=port
        self._two=group
        self._one.connect_to(self)
        self._two=group.connect_to(self)

    def _connect_group_group(self, groupA, groupB):
        if groupA == None or groupB == None:
            raise Exception("this should never happen")
        self._one=groupA
        self._two=groupB
        self._one.connect_to(self)
        self._two.connect_to(self)

        self._connect_group_group_ordered(self._one, self._two)
        self._connect_group_group_ordered(self._two, self._one)

    def _connect_group_group_ordered(
        self, empty_group, nonempty_group, push_to_nonempty=True
    ):
        if self._sublinks == None:
            self._sublinks=[]

        ports=nonempty_group.get_unconnected_ports(self)
        for i in ports:
            link=Link(self)
            link.register(i)
            link.register(empty_group, push_to_nonempty)
            self._sublinks.append(link)

# up to here
##########################

    def other_port(self, port):
        if self._one == port:
            if self._two == None:
                raise Exception("hit 1")
            return self._two
        elif self._two == port:
            if self._one == None:
                raise Exception("hit 2")
            return self._one
        else:
            raise Exception("this should never happen", port)
            return None

    def connection_name(self, port):
        if port == self._one:
            return self._connection_name(self._two)
        elif port == self._two:
            return self._connection_name(self._one)
        else:
            raise Exception("this should never happen")

    def _connection_name(self, port):
        if port.internal == True:
            return port.name
        else:
            return self.name

    def _register_worst_case(self, port):
        raise Exception("not implemented")

    def dump_signal(self):
        if self._sublinks == None:
            if self._one.internal == True or self._two.internal == True:
                return ""
            else:
                self._check_cfgs()
                print("{}: dump_signal() needs more love".format(__file__))
                return "    signal {}: <type>;\n".format(self.name)
        else:
            ret=""
            for i in self._sublinks:
                ret+=i.dump_signal()
            return ret

    def _check_cfgs(self):
        print("{}: check_cfgs() needs more love".format(__file__))
