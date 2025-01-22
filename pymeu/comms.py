try:
    import pylogix
    PLC_DRIVER = "pylogix"
except ImportError:
    try:
        import pycomm3
        PLC_DRIVER = "pycomm3"
    except ImportError:
        raise ImportError("You need to install pylogix or pycomm3")


class Driver:

    def __init__(self, ip_address=None):

        self._cip_path = ip_address

        if PLC_DRIVER == "pylogix":
            self.cip = pylogix.PLC(self._cip_path)
        elif PLC_DRIVER == "pycomm3":
            self.cip = pycomm3.CIPDriver(self._cip_path)
            self.cip.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if PLC_DRIVER == "pylogix":
            self.cip.Close()
        if PLC_DRIVER == "pycomm3":
            self.cip.close()

    def generic_message(self, service, class_code, instance, request_data, connected, route_path):
        if PLC_DRIVER == "pylogix":
            ret = self.cip.Message(service, class_code, instance, None, request_data)
            if ret.Status == "Success":
                status = None
            else:
                status = ret.Status
            response = Response(ret.Value[44:], None, status)
        elif PLC_DRIVER == "pycomm3":
            response = self.cip.generic_message(service=service,
                                                class_code=class_code,
                                                instance=instance,
                                                request_data=request_data,
                                                connected=connected,
                                                route_path=route_path)

        return response
    

class Response(object):

    def __init__(self, value, type, error):
        self.tag = 'generic'
        self.value = value
        self.type = type
        self.error = error