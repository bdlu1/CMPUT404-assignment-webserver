#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
    
    def handle(self):
        self.data = self.request.recv(1024).decode() # decode the data from utf-8 

    
        requests = self.data.split('\r\n') # split() data here
        requestsList = requests[0].split() # split the request into the method used and fileRequested/file

        method = requestsList[0]
        fileRequested = requestsList[1]

        root = './www'

        contentTypes = ['Content-Type: text/html\r\n',
                        'Content-Type: text/css\r\n']
        
        if method != 'GET':
            self.handle405()
        else:
            self.default(fileRequested, root, contentTypes)
        

    def default(self, fileRequested, root, contentTypes): 

        if fileRequested.endswith('/'): # open the default index.html page * this also catches the case where fileRequested only contains '/'
            try: # case 1 the extension is '/' or the file requested is just the '/' character
                fileToOpen = root + fileRequested + 'index.html'
                fileOpen = open(fileToOpen, "r")
                fileContent = fileOpen.read()
                fileOpen.close()            
                self.handle200(fileContent, contentTypes[0])
                return
            except FileNotFoundError:
                self.handle404() # throw 404 if file not found

        elif fileRequested.endswith('.html'):
            try: # case 2 the extension is .html
                fileToOpen = root + fileRequested 
                fileOpen = open(fileToOpen)
                fileContent = fileOpen.read()
                fileOpen.close()            
                self.handle200(fileContent, contentTypes[0]) # use correct mime-type

            except FileNotFoundError:
                self.handle404()
        
        elif fileRequested.endswith('.css'):
            try: # case 3 the extension is .css 
                fileToOpen = root + fileRequested 
                fileOpen = open(fileToOpen)
                fileContent = fileOpen.read()
                fileOpen.close()            
                self.handle200(fileContent, contentTypes[1]) # use css mime-type

            except FileNotFoundError:
                self.handle404()
        
        else: # this case is where path doesn't contain any of the previous extensions
              # therefore its a path that needs redirection
            fileRequested = fileRequested + '/'
            self.handle301(fileRequested)

               
        
    def handle200(self, fileContent, contentType):
        #print('inside 200')
        response = f'HTTP/1.1 200 OK\r\n{contentType}\r\n' + fileContent
        self.request.sendall(response.encode())
        return
    
    def handle301(self, location):
        response = f'HTTP/1.1 301 FILE MOVED\r\nLocation: {location}\r\n'
        self.request.sendall(response.encode())
        return

    def handle404(self):
        print('inside 404')
        response = 'HTTP/1.1 404 FILE NOT FOUND\n\n'
        self.request.sendall(response.encode())
        return 
    
    def handle405(self):
        response = 'HTTP/1.1 405 INVALID METHOD\n\nInvalid Method Used'
        self.request.sendall(response.encode())
        return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
