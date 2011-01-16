import json
import socket

class JsonRPCException(Exception):
    def __init__(self, err):
        self.code = err["code"]
        self.message = err["message"]

    def __str__(self):
        return self.message + " (code: " + repr(self.code) + ")"

class JsonRPCProxy:
    def __init__(self, conn, method = ""):
        """
            conn - tuple (hostname, port) or socket
        """
        if isinstance(conn, socket.socket):
            self._socket = conn
        else:
            self._socket = socket.create_connection(conn)
            # TODO: This timeout thing is not cool :-)
        
        self._method = method

    def __getattr__(self, name):
        if self._method != "":
            name = self._method + "." + name
        return JsonRPCProxy(self._socket, name)

    def __call__(self, *args, **kwargs):
        obj = {"jsonrpc": "2.0", "method": self._method, "id": 0}


        if len(args) and len(kwargs):
            raise Exception("You can't have both named and positional parameters")
        elif len(args):
            obj["params"] = args
        elif len(kwargs):
            obj["params"] = kwargs

        data = json.dumps(obj)
        self._socket.sendall(data)

        try:
            self._socket.settimeout(10)
            data = self._socket.recv(4096)
            self._socket.settimeout(0.1)
            while True:
                data += self._socket.recv(4096)
        except socket.timeout:
            pass

        response = json.loads(data)

        if response.has_key("error"):
            raise JsonRPCException(response["error"])

        return response["result"]
