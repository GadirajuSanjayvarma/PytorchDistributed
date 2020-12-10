import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm
from model import Net1

class modelTraining:

  def __init__(self):
   
    if(torch.cuda.is_available()):
        self.device="cuda"
    else:
        self.device="cpu"
    self.epochs=10
    
    self.model=Net1().to(self.device)
    self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)    
    

    

  def train(self,train_loader):
        self.model.train()
        pbar = tqdm(train_loader)
        num=0
        params=[]
        total_loss=0
        num=0
        num_images=0
        correct=0
        optimizer=optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9)
        for (data, target) in pbar:
            #print(data.shape)
            data, target = data.to(self.device), target.to(self.device)
            self.optimizer.zero_grad()
            output = self.model(data)
            #loss = nn.CrossEntropyLoss()
            #print("**  ",output.shape,target.shape,"  **")
            loss = F.nll_loss(output, target)
            loss.backward()
            self.optimizer.step()
            total_loss+=loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()
            num+=1
            num_images+=len(pred)
            pbar.set_description(desc= f'loss={loss.item()} batch_id={num}')
        result=[total_loss/num,correct/num_images]
        return result


                        

     