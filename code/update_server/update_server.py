import BaseHTTPServer
import urlparse
import urllib 
import SocketServer
import threading
import ssl

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 443

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
	print "[+] GET"
	print self.path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == '/version':
            self.wfile.write('{"result": true, "api_version": 1}')
            return
	elif self.path == '/manifest':
            self.wfile.write(open("manifest", "rb").read())
            return
        return    

    def do_POST(self):
	print "[+] POST"
	print self.path
        pass

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


if __name__ == '__main__':
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), Handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='root-ca.key', certfile='root-ca.crt', server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    print "Server Stopped - %s:%s" % (HOST_NAME, PORT_NUMBER)