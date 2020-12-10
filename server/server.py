from socket import *
import os
import pickle
import torch
import torchvision
import _thread

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim




class server:

  def __init__(self,host,port,target_clients,mode):
    self.host=host
    self.port=1
    self.valid=True
    self.target_clients=target_clients
    self.mode=mode
    self.client_list=[]
    self.params_list=[]
    
  

  def startServer(self):
    if(self.mode=="server"):
      
      sock=socket()
      sock.bind((self.host,self.port))
      print("hosting on",self.host,self.port)
      sock.listen(1)
      self.port+=1
      no_of_clients=0
      
      while(True):
          
          print("waiting for a client")
          client,address=sock.accept()
          self.client_list.append(client)
          no_of_clients+=1
         
          print("client joined from ",address)
          #print("total clients are",len(self.client_list))
          
          if(no_of_clients==len(self.target_clients)):
            print("target clients reached")
            print("all clinets connected")
            #dataLoading.start_loading(self,self.modelTrainer)
            sock.close()
            break
            

    if(self.mode=="client"):
      

      for i in range(0,len(self.target_clients)):
          self.target_clients[i]=(self.target_clients[i][0],self.target_clients[i][1]+1)
      try: 
        
        dummy_list=[]
        for address in  self.target_clients:
            dummy_list.append(address)
        i=0
        while(len(dummy_list)>0):
            print(dummy_list)
            if(i>=len(dummy_list)):
                i=0
            try:
              print("checking with address",i) 
              #print(dummy_list[i])
              sock1=socket()
              sock1.connect(dummy_list[i])
              with sock1,sock1.makefile('rb') as clientfile:     
                  raw = clientfile.read()     
                  data = pickle.loads(raw)
                  print(data)
                  #self.addToTextFile(data[1])
                  #self.modelTrainer.add_gradList(data[0])
                  self.params_list.append(data)
                  
                  dummy_list.pop(i)
                  print(i,"address is removed")
                  sock1.close() 
             
              
              i+=1  
              
              
            except Exception as e:
              print("got exception with address",dummy_list[i],e)
              sock1.close() 
              #break
                      
      except Exception as e:
        #print(e)  
        print("obtained all gradients")    
      #self.modelTrainer.computeAvgGradients()

      #self.changeServerMod()
      

                     


  
  def changeServerMode(self):
    if(self.mode=="client"):
      self.client_list=[]
      self.params_list=[]
      self.mode="server"
    else:
      
      self.mode="client"  
    
    print("changed server mode")
    #self.startServer()


  def addToTextFile(self,data):
    with open("loss.txt", 'a') as file1: 
       file1.write("{} {}\n".format(data[0],data[1])) 


  def send(self,client, data,index):
    with client:
        #print(data)
        data=pickle.dumps(data)
        #s.send(data)
        print(client)
        client.sendall(data)

        #print('completed sending data for client',client)

    #self.client_list.pop(index) 


  def get_no_clients(self):
    return len(self.target_clients)  




