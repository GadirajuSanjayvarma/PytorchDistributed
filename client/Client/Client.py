from __future__ import print_function
from socket import *
import os
import pickle
from tqdm import tqdm



class Client:
    client_dict = {'10.0.45.44' : 4999,"10.0.44.240":5999,"10.0.44.169":6999,"192.168.7.13":7999,"10.0.47.208":8999,"10.0.27.111":9999 }

    def __init__(self,model,trainer):
        """
        Constructor initialises trainer object,
        serverIp,serverPort,ClientIp,Clientport 
        Throughout this program client is this computer and
        server is the one which sends data
        to this computer
        """
        self.model = model
        self.trainer = trainer
        self.serverIP = '10.0.45.47'
        """
        gethostbyname() and gethostname() are from socket module
        """
        self.serverPort=1
        self.clientIp = gethostbyname(gethostname()) 
        self.clientPort = Client.client_dict[self.clientIp]+1


    def getEpochs(self):
        """
        returns the number of epochs
        it gets this from server computer.
        """
        return self.trainer.epochs


    def receiveTrainingData(self):
        """
        It receives [parameters,trainingdata] here.
        """
        print("Waiting for server.......",self.serverIP,self.serverPort)
        while True:
            try:
                sock = socket()
                sock.connect((self.serverIP,self.serverPort))
                with sock,sock.makefile('rb') as clientfile:
                    while True:

                        raw = clientfile.read()
                        if not raw: break # no more files, server closed connection.
                        data = pickle.loads(raw)
                        print("Received Training data")
                        if not data: break
                    else: # only runs if while doesn't break and length==0
                        print('Complete')
                sock.close()
                self.serverPort+=1
                return data
            except:
                """
                May be some TimeoutError is thrown.
                """
                pass

    def train(self,data):
        """
        Training is done here.
        1.Before training model parameters 
            values are reassigned with new values
            which are obtained from server computer.
        """
        i=0
        for p in self.model.params:
            p.weight=data[0][i]
            i+=1
        """
        Here we are changing parameters in optimizer
        without changing the state of optimizer.
        """
        self.trainer.optimizer.param_groups=[]
        param_groups = list(self.model.parameters())
        param_groups = [{'params': param_groups}]
        for param_group in param_groups:
            self.trainer.optimizer.add_param_group(param_group)
        self.printParameters()
        print("Started trainig...........")
        result=self.trainer.train(data[1])
        print("Completed training..........")
        self.printParameters()
    

    def getClientModelParams(self):
        """
        It rteturns parameters of the model
        that it is running.
        """
        params=[]
        for param in self.model.parameters():
            params.append(param)
        return params

    
    def printParameters(self):
        for i in self.model.parameters():
            print(list(i)[0])
            break


    def sendDatatoServer(self):
        """
        Here it sends model parameters to server computer.
        """
        print("Sending data to server computer..........")
        data = self.getClientModelParams()
        while True:
            try:
                sock=socket()
                sock.bind((self.clientIp,self.clientPort))
                sock.listen(1)
                print("waiting for a client")
                client,address=sock.accept()
                print(f"client joined from {address}")
                with client:
                    data=pickle.dumps(data)
                    client.sendall(data)
                print('DOne')
                sock.close()
                self.clientPort+=1
                break
            except:
                """
                Probably Address in use error might be raised
                """
                pass
        
    def run(self):
        """
        This is a sample function which demonstrates
        how to use these functions in training a model.
        """
        for epoch in range(self.getEpochs()):
            data = self.receiveTrainingData()
            self.train(data)
            self.sendDatatoServer()












"""
for i in self.trainer.model.parameters():
                print(list(i)[0])
                break
            """
