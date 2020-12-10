import os
from socket import *
import tqdm
import os
# device's IP address


class sendFiles:
    def __init__(self,directory,filesRequired,filesRequiredClients):
        self.SERVER_PORT = 5000
        self.directory=directory
        self.list1=filesRequired
        self.filesRequiredClients=filesRequiredClients
        
    def checkForFiles(self):
        print("waiting for rquired files")
        while(len(self.list1)>0):
            for filename in os.listdir(self.directory):
                if(filename in self.list1):
                    print("obtained ",filename)
                    if(filename in self.filesRequiredClients):
                        print("sending this file to all clients")
                        self.send(filename)
                    self.list1.remove(filename)
        print("obtained required files")



    def send(self,filename):
        SERVER_HOST = "192.168.7.19"
        global SERVER_PORT
        BUFFER_SIZE = 4096
        connected_clients=0
        s = socket()
        s.bind((SERVER_HOST, self.SERVER_PORT))
        self.SERVER_PORT+=1
        s.listen(5)
        while(True):
            print("hi")
            print(f"[*] Listening as {SERVER_HOST}:{self.SERVER_PORT}")
                
            client_socket, address = s.accept() 
            print(f"[+] {address} is connected.")
            connected_clients+=1
            with open(filename, "rb") as f:
                client_socket.send(f"{filename}".encode())
                while(True):
                    bytes_read = f.read(BUFFER_SIZE)
                    if(not bytes_read):break
                    client_socket.sendall(bytes_read)
                
            # close the client socket
            client_socket.close()
            # close the server socket
            
            if(connected_clients==1):
                print("completed sending",filename,"to all clients")
                s.close()
                break
        




directory="C:\\Users\\SAIRAM\\Desktop\\pytorchDistributedCode\\server"
requiredFiles=["model.py","modelTraining.py","userFile.py"]
requirementsClients=["model.py","modelTraining.py"]

sendfile=sendFiles(directory,requiredFiles,requirementsClients)
sendfile.checkForFiles()        
print("executing prgram")
os.system("python userFile.py")
