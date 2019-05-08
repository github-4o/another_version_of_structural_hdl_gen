class Reporter:
    def __init__(self):
        self._indent=""
        self._increments=0
        self._decrements=0
        self._DEBUG=False

    def print(self, str, format=None, more_indent=True):
        if format != None:
            for i in range(0, len(format)):
                format[i]=underline(format[i])
            str=str.format(*format)
        print(self._indent+str)
        if more_indent == True:
            self.more_indent()

    def more_indent(self):
        self._indent+="   "
        self._increments+=1

    def less_indent(self):
        self._indent=self._indent[3:]
        self._decrements+=1
        if self._DEBUG == True:
            print("{}/{}:less indent '{}'".format(
                self._increments, self._decrements, self._indent))

reporter=Reporter()


def underline(str):
    return "\033[4m"+str+"\033[0m"
