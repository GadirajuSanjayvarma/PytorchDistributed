from socket import *
import pickle
import tqdm
import os

class FileReceiver:
    def recieveFile(self,port):
        """
        This function takes files from server 
        and create same files in this commp[uter with same names.]
        """ 
        host = '10.0.45.47'
        """
        We implemented only onle computer as server.
        So thae variable host holds is the ipv4 address
        of that server computer.
        You can change host value to receive the files from
        other computer.
        
        """
        s = socket()
        s.connect((host, port))
        BUFFER_SIZE = 4096
        with s,s.makefile('rb') as clientfile:
            filename = s.recv(BUFFER_SIZE).decode()
            """
            That server computer should first send the file name.
            server sends like this : socke.send(filename.encode())
            """
            f=open(filename,"wb")
            while True:
                raw = clientfile.read()
                if not raw: break # no more files, server closed connection.
                f.write(raw)
                print("Received",filename)
            f.close()
        s.close()
    

    def receiveFiles(self,num=2):
        """
        It receives 'num' number of files
        if num is not given
        it receives two files.
        """
        i=0
        print("Started receiving files........")
        while(i<num):
            """
            It should receive two files
            1.model.py
            2.modelTraining.py
            from the server computer
            """
            try:
                self.recieveFile(5000+i)
                i+=1
            except:
                pass
        """
        After receiving two files it should run client_file.py where 
        training and passing final parameters to server computer is implemented.
        """
