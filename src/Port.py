from .service.Reporter import reporter


def invert_dir(dir):
    if dir == "in":
        return "out"
    elif dir == "out":
        return "in"
    else:
        raise Exception("invalid dir:", dir)

class Port:
    def __init__(self, parent, dir=None, cfg=None):
        self._parent=parent
        self._cfg=cfg
        self._bound_port=None
        self._dir=dir
        self._link=None

    @property
    def is_unconnected(self):
        return self._link == None

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
    def cfg(self):
        if self._cfg == None:
            return None
        else:
            return self._cfg.copy()

    @property
    def bound_port(self):
        raise Exception("restricted")
        return self._bound_port.copy()

    @property
    def dir(self):
        if self._dir == None:
            return None
        else:
            return self._dir[:]

    @bound_port.setter
    def bound_port(self, val):
        if self._bound_port != None:
            raise Exception("attempt to modify bound port")
        self._bound_port=val

    def dump_ports(self, indent="        "):
        if self._cfg == None:
            return indent+"{}: {} <port with empty cfg> ;\n".format(
                self.name, self._dir)
        else:
            raise Exception("this should never happen")

    def connect_to(self, link):
        reporter.print(
            "port {}: connected to link {}",
            [self.hierarchial_name, link.hierarchial_name]
        )
        # access check. it IS overengineering, to catch hypothetical
        # invalid call sequences
        if self._link != None:
            raise Exception(
                "port reconnection detected {}\n".format(self.hierarchial_name)
                +" new connection {}\n".format(link.other_port(self).hierarchial_name)
                +" old connection {}\n".format(self._link.other_port(self).hierarchial_name)
            )
        self._link=link
        reporter.less_indent()

    def update_from_link(self):
        reporter.print(
            "port {}: updating from link {}",
            [self.hierarchial_name, self._link.hierarchial_name]
        )
        if self._link == None:
            raise Exception("this should never happen")

        other_port=self._link.other_port(self)
        if other_port == None:
            raise Exception("this should never happen")

        if other_port != None:
            self._update_from_port(other_port)
        else:
            raise Exception("this should never happen")
        reporter.less_indent()

    def update_from_bound_port(self, bound_port, port):
        reporter.print(
            "port {}: updating from bound port {}",
            [self.hierarchial_name, self._bound_port.hierarchial_name]
        )
        if self._bound_port != bound_port:
            raise Exception("this should never happen")

        self._update_from_port(port, trigger_chain_update=False)
        reporter.less_indent()

    def _update_from_port(self, port, trigger_chain_update=True):
        self._update_cfg(port)
        self._update_dir(port)
        if trigger_chain_update == True:
            if self._bound_port != None:
                self._bound_port.update_from_bound_port(self, port)

    def _update_cfg(self, port):
        other_cfg=port.cfg
        if other_cfg != None:
            for name in other_cfg:
                if name in self._cfg:
                    if self._cfg[name] != other_cfg[name]:
                        raise Exception("failed to update cfg on _update_cfg()")
                else:
                    self._cfg[name]=other_cfg[name]

    def _update_dir(self, port):
        if self.internal == False:
            if port.internal == True:
                do_inversion=False
            else:
                do_inversion=True
        else:
            do_inversion=False

        other_port_dir=port.dir
        if other_port_dir != None:
            if self._dir == None:
                if do_inversion:
                    self._dir=invert_dir(other_port_dir)
                else:
                    self._dir=other_port_dir
            else:
                if do_inversion:
                    if self._dir != invert_dir(other_port_dir):
                        raise Exception("dir mismatch")
                else:
                    if self._dir != other_port_dir:
                        raise Exception("dir mismatch")


    def dump_inst_connection(self, indent):
        if self._link == None:
            print (
                "****dumping inst connection of a port with no link detected\n"
                +"    this *may* be caused by unconnected port\n"
                +"    port {}\n".format(self.name)
                +"    parent name {}\n".format(self._parent.name)
            )
            return indent+"{} => <no link>,\n".format(self.name)

        if self._cfg == None:
            return indent+"{} => {},\n".format(
                self.name, self._link.connection_name(self))
        else:
            raise Exception("not implemented")
