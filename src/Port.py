def invert_dir(dir):
    if dir == "in":
        return "out"
    elif dir == "out":
        return "in"
    else:
        raise Exception("invalid dir")

class Port:
    def __init__(self, parent, dir=None, cfg=None):
        self._parent=parent
        self._cfg=cfg
        self._bound_port=None
        self._dir=dir
        self._link=None

    @property
    def name(self):
        return self._parent.get_port_name(self)

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
            return indent+"{}: {} <port with empty cfg> ;\n".format(self.name, self._dir)
        else:
            raise Exception("this should never happen")

    def connect_to(self, port, link):
        if self._link != None:
            raise Exception(
                "port reconnection detected {}\n".format(self.name)
                +" new connection {}\n".format(port.name)
                +" old connection {}\n".format(self._link.other_name(self))
            )
        self._update_cfg(port)
        self._update_dir(port)
        self._link=link
        return self

    def _update_cfg(self, port):
        other_cfg=port.cfg
        if other_cfg != None:
            for name in other_cfg:
                if name in self._cfg:
                    if self._cfg[name] != other_cfg[name]:
                        raise Exception("failed to update cfg on connect_to()")
                else:
                    self._cfg[name]=other_cfg[name]

    def _update_dir(self, port):
        if self.internal == False:
            if port.internal == True:
                do_inversion=False
            else:
                do_inversion=True
        else:
            if port.internal == True:
                raise Exception("this should never happen")
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
