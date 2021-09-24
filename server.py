#  coding: utf-8 
import socketserver
from os import path
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, 2021 Rain Wu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def get_file(self,file_path):
            f = open(file_path)
            file = f.readlines()
            file_content = '\n'.join(file)
            f.close()
            return file_content
    
    def handle(self):
        #the request is available as self.request;
        # the client address as self.client_address;
        # and the server instance as self.server
        self.data = self.request.recv(1024).strip()

        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray(f"{self.data}",'utf-8'))


        recv_data = self.data.decode().split()

        #Check whether the received data is empty
        if recv_data == []:
            self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            
        method = recv_data[0]
        address = recv_data[1]

        #We do not want other methods except "Get"
        if method != "GET":
            self.request.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode())

        #We do not want ../../../ in our html
        if "../" in address:
            self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        addr_path = os.path.abspath('www') + address
        
        if path.isdir(addr_path) == True:
            #If the path not include with /, we will redirect the path
            if not addr_path.endswith('/'):
                address += '/'
                header = (f"HTTP/1.1 301 Moved Permanently\r\nLocation: {address}\r\n\r\n")
                self.request.sendall(header.encode())
                addr_path += '/'
            #If the path end with /, then we will read the file and send it
            #else:
            addr_path += 'index.html'
            content_type  = 'text/html'
            header = (f"HTTP/1.1 200 OK\r\nContent-type: {content_type}\r\n\r\n")
            response = self.get_file(addr_path)
            self.request.sendall(f"{header + response}".encode()) 
        elif path.isfile(addr_path) == True:
            if addr_path.endswith(".css") == True:
                content_type = 'text/css'
                header = (f"HTTP/1.1 200 OK\r\nContent-type: {content_type}\r\n\r\n")
                response = self.get_file(addr_path)
                self.request.sendall(f"{header + response}".encode()) 
            elif addr_path.endswith(".html") == True: 
                content_type = 'text/html'
                header = (f"HTTP/1.1 200 OK\r\nContent-type: {content_type}\r\n\r\n")
                response = self.get_file(addr_path)
                self.request.sendall(f"{header + response}".encode()) 
            else:
                self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        else:
           self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode()) 

        
        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
