import os  
import socket 
from mimetypes import guess_type
class HTTPServer:
    headers = {
        'Server': "Shreeraj's server",
        
    }
    status_codes = { 
        200: 'OK',
        404: 'Not Found',
        301: 'Moved Permanently',
    }


    def __init__(self, host='127.0.0.1', port=4040):
        self.host = host
        self.port = port
        self.method = None
        self.uri = None
        self.http_version = '1.1'


    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        print("Listening at", s.getsockname())
        while True:
            c, addr = s.accept()
            print("Connected by", addr) 
            data = c.recv(2048)
            response= self.handle_request(data)
            c.sendall(response)
            c.close()

    
    def handle_request(self, data):
        lines = data.split(b'\r\n')
        request_line = lines[0] 
        words = request_line.split(b' ')
        self.method = words[0].decode() 
        if len(words) > 1:
            self.uri = words[1].decode()
        if len(words) > 2:
            self.http_version = words[2].decode()
        response = self.handle_GET()
        return response


    def handle_GET(self):
        path = self.uri.strip('/') 
        if not path:
            path = 'index.html'
        if path=="moveto.html":
            response_line = self.response_line(301)
            response_headers = self.response_headers(extra_headers={
                "Location" : "https://www.google.co.in/"
            })
            response_body =b''
        elif os.path.exists(path) and not os.path.isdir(path): 
            response_line = self.response_line(200)
            response_headers = self.response_headers(path=path)
            with open(path, 'rb') as f: 
                response_body = f.read()
        else:
            path='404.html'
            response_line = self.response_line(404) 
            response_headers = self.response_headers(path=path)
           
            with open(path, 'rb') as f: 
                response_body = f.read()
        blank_line = b'\r\n'
        response = b''.join([response_line, response_headers, blank_line, response_body])
        return response
    

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        response_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)
        return response_line.encode()

    def response_headers(self,path=None, extra_headers=None):
        headers_copy = self.headers.copy() 
        if path:
            headers_copy['Content-Type']=guess_type(path)[0]
        else:
            headers_copy['Content-Type']='text/html'
        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ''

        for h in headers_copy:
            headers += '%s: %s\r\n' % (h, headers_copy[h])

        return headers.encode() 


if __name__ == '__main__':
    server = HTTPServer()
    server.start()

