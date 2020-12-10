import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm


class modelTraining:

  def __init__(self,epochs=10,loss=0.0,device="cpu",model=None,optimizer=None):
   
    self.epochs=epochs
    self.loss=loss
    if(torch.cuda.is_available()):
      self.device="cuda"
    else:
      self.device="cpu"  
    self.gradients_list=[]
    self.avg_gradients=0.0

    if(model==None):
        self.model=Net1().to(self.device)
    else:
        self.model=model
    self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)    
    

    for p in  self.model.parameters():
        #print("before changing grads")
        #print(p.grad[0])
        p.grad=torch.FloatTensor(p.shape).clone()
 
  def add_gradList(self,loss):
      self.gradients_list.append(loss) 


  def computeAvgGradients(self,para):
    print("computing avg gradient")
    avg_gradients=[]
    for i in range(0,len(para)):
      for index,j in enumerate(para[i]):
          if(i==0):
              avg_gradients.append(j)
          else:
              avg_gradients[index]=torch.add(avg_gradients[index],j)
            
        
    for i in range(0,len(avg_gradients)):
      divisor_list=torch.FloatTensor(avg_gradients[i].shape).fill_(len(para))
      
      avg_gradients[i]=torch.div(avg_gradients[i],divisor_list)
    
    

    self.avg_gradients= avg_gradients
    self.updateParams()

  def updateParams(self):
      
      i=0  
      for p in  self.model.params:
        
        p.weight=nn.Parameter(self.avg_gradients[i])
        i+=1  #  need to change based on gradients obtained
    
      
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


                        

     