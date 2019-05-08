from .Port_group import Port_group
from .Port import Port
from .service.Reporter import reporter


slv_lib_string="library ieee;\nuse ieee.std_logic_1164.all;\n"

def check_list_keys(a, b, do_reverse=True):
    for i in a:
        if i not in b:
            return False
    if do_reverse == True:
        return check_list_keys(b, a, False)
    else:
        return True

class Node_iface:
    __number=0

    @classmethod
    def _get_number(cls):
        ret=cls.__number
        cls.__number+=1
        return ret

    def __init__(self, name, parent):
        self._name=name+"_{}".format(self.__class__._get_number())
        self._ports={}
        self._int_port_groups={}
        self._ext_port_groups={}
        self._parent=parent

    @property
    def name(self):
        return self._name[:]

    @property
    def hierarchial_name(self):
        if self._parent == None:
            return self.name
        else:
            return self._parent.hierarchial_name+"."+self.name

# graph modification
    def add_portgroup(self, name):
        reporter.print(
            "node {}: adding portgroup {}", [self.hierarchial_name, name]
        )
        # access check. it IS overengineering, to catch hypothetical
        # invalid call sequences
        if name in self._int_port_groups or name in self._ext_port_groups:
            raise Exception("re-adding port with existing name detected")

        int_port=Port_group(self)
        ext_port=Port_group(self)

        int_port.bound_port_group=ext_port
        ext_port.bound_port_group=int_port

        self._int_port_groups[name]=int_port
        self._ext_port_groups[name]=ext_port
        reporter.less_indent()

    def add_port(self, name, dir):
        reporter.print(
            "node {}: adding {} port {}", [self.hierarchial_name, dir, name]
        )
        # access check. it IS overengineering, to catch hypothetical
        # invalid call sequences
        if name in self._int_port_groups or name in self._ext_port_groups:
            raise Exception("re-adding port with existing name detected")

        int_port=Port(self, dir=dir)
        ext_port=Port(self, dir=dir)

        int_port.bound_port_group=ext_port
        ext_port.bound_port_group=int_port

        self._int_port_groups[name]=int_port
        self._ext_port_groups[name]=ext_port
        reporter.less_indent()

    def connect_ext_port(self, portname, link):
        # access check. it IS overengineering, to catch hypothetical
        # invalid call sequences
        if portname not in self._ext_port_groups:
            raise Exception(
                "failed to find port {} link {}".format(portname, link.hierarchial_name)
            )
        link.register(self._ext_port_groups[portname])

    def connect_int_port(self, portname, link):
        if portname not in self._int_port_groups:
            raise Exception("node {}: failed to find port {}".format(
                self.name, portname))
        link.register(self._int_port_groups[portname])

# dump
    def dump_component(self):
        self._verify_ports()
        return (
            "    component {} is\n".format(self.name)
            +"        port (\n"
            +self._dump_ext_ports()
            +"            iClk: in std_logic;\n"
            +"            iReset: in std_logic\n"
            +"        );\n"
            +"    end component;\n"
        )

    def dump_hdl(self):
        return [(self.name+".vhd", self._dump_hdl())]

    def _dump_hdl(self):
        return (
            slv_lib_string
            +"\n\n"
            +self._dump_entity()
            +"\n"
            +self._dump_architecture()
        )

    def _dump_entity(self):
        self._verify_ports()
        return (
            "entity {} is\n".format(self.name)
            +"    port (\n"
            +self._dump_int_ports()
            +"\n"
            +"        iClk: in std_logic;\n"
            +"        iReset: in std_logic\n"
            +"    );\n"
            +"end entity;\n"
        )

    def _verify_ports(self):
        check=check_list_keys(self._int_port_groups, self._ext_port_groups)
        if check == False:
            raise Exception("port consistency check failed")
        # we need to go deeper
        print("{}: warning: port check requires more love".format(__file__))

    def _dump_int_ports(self, indent="        "):
        ret=""
        for i in self._int_port_groups:
            ret+=self._int_port_groups[i].dump_ports(indent)
        return ret

    def _dump_ext_ports(self, indent="            "):
        ret=""
        for i in self._ext_port_groups:
            ret+=self._ext_port_groups[i].dump_ports(indent)+"\n"
        return ret

    def _dump_architecture(self):
        return (
            "architecture v1 of {} is\n".format(self.name)
            +"\n"
            +self._dump_architecture_declarative()
            +"\n"
            +"begin\n"
            +"\n"
            +self._dump_architecture_executive()
            +"end v1;\n"
        )

    def _dump_instance(self):
        return (
            "    {}_inst: {}\n".format(self.name, self.name)
            +"        port map (\n"
            +self.dump_inst_ports()
            +"\n"
            +"            iClk => iClk,\n"
            +"            iReset => iReset\n"
            +"        );\n"
        )

# utility

    def get_port_name(self, port_or_port_group):
        for i in self._int_port_groups:
            if self._int_port_groups[i]==port_or_port_group:
                return i

        for i in self._ext_port_groups:
            if self._ext_port_groups[i]==port_or_port_group:
                return i

        # access check. it IS overengineering, to catch hypothetical
        # invalid call sequences
        raise Exception("get_port_name(): unregistered port or port group")

    def is_internal(self, port_or_port_group):
        for i in self._int_port_groups:
            if self._int_port_groups[i]==port_or_port_group:
                return True

        for i in self._ext_port_groups:
            if self._ext_port_groups[i]==port_or_port_group:
                return False

        # access check. it IS overengineering, to catch hypothetical
        # invalid call sequences
        raise Exception("is_internal(): unregistered port or port group")

    def dump_inst_ports(self, indent="            "):
        ret=""
        for i in self._ext_port_groups:
            ret+=self._ext_port_groups[i].dump_inst_connection(indent)
        return ret
