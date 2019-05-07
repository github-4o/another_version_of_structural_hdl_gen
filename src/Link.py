from .Port_group import Port_group


class Link:
    __number=0

    @classmethod
    def _get_number(cls):
        ret=cls.__number
        cls.__number+=1
        return ret

    def __init__(self):
        self._name="s{}".format(self.__class__._get_number())
        self._one=None
        self._two=None
        self._sublinks=None

    @property
    def name(self):
        return self._name[:]


    def register(self, port):
        if self._one==None:
            self._one=port
        elif self._two==None:
            if isinstance(self._one, Port_group):
                self._one=self._one.connect_to(port, self)
                port=port.connect_to(self._one, self)
            else:
                port=port.connect_to(self._one, self)
                self._one=self._one.connect_to(port, self)
            self._two=port
        else:
            raise Exception("this should never happen")

    def finalize(self):
        check1=isinstance(self._one, Port_group)
        check2=isinstance(self._two, Port_group)
        if check1 == True and check2 == True:
            self._sublinks=[]
            if self._one.port_num == 0 and self._two.port_num > 0:
                self._finalize(self._two, self._one)
            elif self._one.port_num > 0 and self._two.port_num == 0:
                self._finalize(self._one, self._two)
            else:
                raise Exception("{}.finalize(): houston, we have a problem here".format(
                    __file__))

    def other_name(self, port):
        portname=port.name
        if self._one.name == portname:
            return self._two.name
        elif self._two.name == portname:
            return self._one.name
        else:
            raise Exception("failed to find port with name {}".format(portname))

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
                self.check_cfgs()
                print("{}: dump_signal() needs more love".format(__file__))
                return "    signal {}: <type>;\n".format(self.name)
        else:
            ret=""
            for i in self._sublinks:
                ret+=i.dump_signal()
            return ret

    def check_cfgs(self):
        print("{}: check_cfgs() needs more love".format(__file__))

    def _finalize(self, group_with_ports, group_without_ports):
        group_with_ports.connect_subports()

    def add_sublink(self, portgroup, port):
        if portgroup == self._one:
            target_portgroup=self._two
        elif portgroup == self._two:
            target_portgroup=self._one
        else:
            raise Exception("this should never happen")

        link=Link()
        link.register(port)
        link.register(target_portgroup)
        self._sublinks.append(link)
