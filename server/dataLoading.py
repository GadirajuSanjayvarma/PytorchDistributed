import torch
import torchvision
from torchvision import transforms


class pyDataLoader:
    def __init__(self,server_object,modelTrainer,device):
        self.server_object=server_object
        self.model_trainer=modelTrainer
        self.device=device

    def start_loading(self,train_loader,size=100):

        print("completed loading of train")  
        
        no_of_clients=self.server_object.get_no_clients()
        divisions=size//(no_of_clients)
        
        data=[] 
        i=0
    
        
        for batch_no,(images,targets) in enumerate(train_loader):
            data.append([images.to(self.device),targets.to(self.device)])
            if(len(data)>=divisions):  
                print("sending data ............................................")
                model_list=[]
                #for p in modelTrainer.model.parameters():
                #   print(p[0])
                #    break
                for p in self.model_trainer.model.parameters():
                    model_list.append(p)

                data=[model_list,data]
                self.server_object.send(self.server_object.client_list[i],data,i)
                data=[]
                i+=1
                
                if((i)==no_of_clients):
                    print("completed sending data to all clients")
                    #modelTrainer.startTraining(local_data)
                    #self.server_object.changeServer()
                    break




