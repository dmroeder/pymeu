

class Driver:

    def __init__(self, ip_address=None, driver=None):

        self._cip_path = ip_address
        self.plc_driver = driver

        if self.plc_driver is None:
            # no driver specified, try both
            try:
                import pycomm3
                self.plc_driver = "pycomm3"
            except ImportError:
                try:
                    import pylogix
                    self.plc_driver = "pylogix"
                except ImportError:
                    raise ImportError("You need to install pylogix or pycomm3")
        elif self.plc_driver == "pycomm3":
            try:
                import pycomm3
            except:
                raise ImportError("pycomm3 driver was specified but is not installed on the system")
        elif self.plc_driver == "pylogix":
            try:
                import pylogix
            except:
                raise ImportError("pylogix driver was specified but is not installed on the system")
        else:
            raise ValueError("{} was specified for the driver, only pylogix and pycomm3 are supported".format(self.plc_driver))

        if self.plc_driver == "pylogix":
            self.cip = pylogix.PLC(self._cip_path)
        elif self.plc_driver == "pycomm3":
            self.cip = pycomm3.CIPDriver(self._cip_path)
            self.cip.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.plc_driver == "pylogix":
            self.cip.Close()
        if self.plc_driver == "pycomm3":
            self.cip.close()

    def generic_message(self, service, class_code, instance, request_data=b'', connected=False, route_path=None):
        if self.plc_driver == "pylogix":
            ret = self.cip.Message(service, class_code, instance, None, request_data)
            if ret.Status == "Success":
                status = None
            else:
                status = ret.Status
            response = Response(ret.Value[44:], None, status)
        elif self.plc_driver == "pycomm3":
            response = self.cip.generic_message(service=service,
                                                class_code=class_code,
                                                instance=instance,
                                                request_data=request_data,
                                                connected=connected,
                                                route_path=route_path)

        return response

    @property
    def timeout(self):
        if self.plc_driver == "pycomm3":
            return self.cip._cfg['socket_timeout']
        if self.plc_driver == "pylogix":
            return self.cip.SocketTimeout

    @timeout.setter
    def timeout(self, new_value):
        if self.plc_driver == "pycomm3":
            self.cip._cfg['socket_timeout'] = new_value

        if self.plc_driver == "pylogix":
            self.cip.SocketTimeout = new_value
    
    def open(self):
        if self.plc_driver== "pycomm3":
            self.cip.open()

    def close(self):
        if self.plc_driver == "pycomm3":
            self.cip.close()


class Response(object):

    def __init__(self, value, type, error):
        self.tag = 'generic'
        self.value = value
        self.type = type
        self.error = error