from server import server
from dataLoading import pyDataLoader
from modelTrainer import modelTraining
import torch
import torchvision
from torchvision import transforms

if(torch.cuda.is_available()):
    device="cuda"
else:
    device="cpu"        
from model import Net1

model=Net1().to(device)

target_clients=[("192.168.7.12",4999),("10.0.44.240",5999),("10.0.44.169",6999),("192.168.7.13",7999),("10.0.47.208",8999),("10.0.27.111",9999)]
target_clients_choice=[target_clients[0]]
#target_clients_self=[('192.168.7.19',5000)]

server1=server("192.168.7.19",1,target_clients_choice,"server")

optimizer = None
modelTrainer=modelTraining(epochs=10,loss=0.0,device="cpu",model=model,optimizer=None)
dataLoader=pyDataLoader(server1,modelTrainer,device)
trans= [transforms.RandomHorizontalFlip(),
                        transforms.RandomCrop(32, padding=4),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[n/255.
                            for n in [129.3, 124.1, 112.4]], std=[n/255. for n in [68.2,  65.4,  70.4]])]

trans = transforms.Compose(trans)
train_loader = torch.utils.data.DataLoader(
    torchvision.datasets.CIFAR100('/files/', train=True, download=True,
                                transform=trans),batch_size=32, shuffle=True)
epochs=10
for i in range(epochs):
        print("epoch is",i)
        server1.startServer()
        # wait for all clients to be connected
        

        dataLoader.start_loading(train_loader,size=len(train_loader))

        server1.changeServerMode()
        server1.startServer()

        #now we have obtained gradients form all clients in self.paramslist
        modelTrainer.computeAvgGradients(server1.params_list)
        modelTrainer.updateParams()
        server1.changeServerMode()









