import json
import socket
import threading

class JsonRPCException(Exception):
    def __init__(self, err):
        self.code = err["code"]
        self.message = err["message"]

    def __str__(self):
        return self.message + " (code: " + repr(self.code) + ")"

class JsonRPCProxy:
    def __init__(self, conn = None, root = None, method = ""):
        """
        conn - tuple (hostname, port) or socket
        The root and method parameters are only used on sub proxies.
        """

        self._method = method

        if root is not None:
            self._root = root
            return

        self._root = self
        self._socket = socket.create_connection(conn)
        self._lock = threading.Lock()

    def __getattr__(self, name):
        if self._method != "":
            name = self._method + "." + name
        return JsonRPCProxy(method = name, root = self._root)

    def __call__(self, *args, **kwargs):
        root = self._root
        obj = {"jsonrpc": "2.0", "method": self._method, "id": 0}

        if len(args) and len(kwargs):
            raise Exception("You can't have both named and positional parameters")
        elif len(args):
            obj["params"] = args
        elif len(kwargs):
            obj["params"] = kwargs

        data = json.dumps(obj)

        with root._lock:
            root._socket.sendall(data)
    
            try:
                root._socket.settimeout(10)
                data = root._socket.recv(4096)
                root._socket.settimeout(0.1)
                while True:
                    data += root._socket.recv(4096)
            except socket.timeout:
                pass

        response = json.loads(data)

        if response.has_key("error"):
            raise JsonRPCException(response["error"])

        return response["result"]
