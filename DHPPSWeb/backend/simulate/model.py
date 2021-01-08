import torch
import os
import csv
import numpy as np
from scipy.integrate import odeint
from functools  import reduce
import torch.nn as nn
from torch.autograd import Variable
import torch
import sys

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

class CLSTM_cell(nn.Module):
    def __init__(self, shape, input_chans, filter_size, num_features):
        super(CLSTM_cell, self).__init__()
        
        self.shape = shape#H,W
        self.input_chans=input_chans
        self.filter_size=filter_size
        self.num_features = num_features
        self.padding=(filter_size-1)/2
        self.conv = nn.Conv2d(self.input_chans + self.num_features, 4*self.num_features, self.filter_size, 1, (int(self.padding),int(self.padding)))

    
    def forward(self, input, hidden_state):
        hidden,c=hidden_state
        print('inputshape:',input.shape)
        print('hiddenshape:',hidden.shape)
        combined = torch.cat((input, hidden), 1)
        A=self.conv(combined)
        (ai,af,ao,ag)=torch.split(A,self.num_features,dim=1)
        i=torch.sigmoid(ai)
        f=torch.sigmoid(af)
        o=torch.sigmoid(ao)
        g=torch.tanh(ag)
        
        next_c=f*c+i*g
        next_h=o*torch.tanh(next_c)
        return next_h, next_c

    def init_hidden(self,batch_size):
        return (Variable(torch.zeros(batch_size,self.num_features,self.shape[0],self.shape[1])),Variable(torch.zeros(batch_size,self.num_features,self.shape[0],self.shape[1])))


class CLSTM(nn.Module):
    def __init__(self, shape, input_chans, filter_size, num_features,num_layers):
        super(CLSTM, self).__init__()
        
        self.shape = shape#H,W
        self.input_chans=input_chans
        self.filter_size=filter_size
        self.num_features = num_features
        self.num_layers=num_layers
        cell_list=[]
        cell_list.append(CLSTM_cell(self.shape, self.input_chans, self.filter_size, self.num_features))  
        for idcell in range(1,self.num_layers):
            cell_list.append(CLSTM_cell(self.shape, self.num_features, self.filter_size, self.num_features))
        self.cell_list=nn.ModuleList(cell_list)      
        self.Linear = nn.Linear(2700,30)
    def forward(self, input, hidden_state):

        current_input = input.transpose(0, 1)
        next_hidden=[]
        seq_len=current_input.size(0)

        
        for idlayer in range(self.num_layers):

            hidden_c=hidden_state[idlayer]
            all_output = []
            output_inner = []            
            for t in range(seq_len):#loop for every step
                hidden_c=self.cell_list[idlayer](current_input[t,...],hidden_c)

                output_inner.append(hidden_c[0])

            next_hidden.append(hidden_c)
            current_input = torch.cat(output_inner, 0).view(current_input.size(0), *output_inner[0].size())#seq_len,B,chans,H,W
            tempResult = current_input
            tempResult = tempResult.squeeze()
            tempResult = tempResult.view(1,-1)
            tempResult = tempResult
            

            result = self.Linear(tempResult)

        return result

    def init_hidden(self,batch_size):

        init_states=[]#this is a list of tuples
        for i in range(self.num_layers):
            init_states.append(self.cell_list[i].init_hidden(batch_size))
        return init_states

  
def train_model(model, train_data_list, train_labels_list, test_data=None, test_labels=None):
    loss_fn = torch.nn.MSELoss(reduction='sum').cuda()  
    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)
    num_epochs = 600    
    train_hist = np.zeros(num_epochs)
    test_hist = np.zeros(num_epochs)    
    for t in range(num_epochs):
      test_loss = loss_fn(train_labels_list[0],train_labels_list[0])
      for i in range(len(train_data_list)):
        train_data = train_data_list[i]

        train_data = processInput(train_data)
        train_labels = train_labels_list[i].cuda().float()
        hidden_state=model.init_hidden(batch_size)
        y_pred = model(train_data.float(),hidden_state)
        y_pred = y_pred.squeeze()
        loss = loss_fn(y_pred.float(), train_labels)    
        if test_data is not None:
          with torch.no_grad():
            y_test_pred = model(X_test)
            test_loss = loss_fn(y_test_pred.float(), y_test)
          test_hist[t] = test_loss.item()   
        optimiser.zero_grad()   
        loss.backward() 
        optimiser.step()
      if t % 10 == 0:  
        print(f'Epoch {t} train loss: {loss.item()} test loss: {test_loss.item()}')
      elif t % 10 == 0:
        print(f'Epoch {t} train loss: {loss.item()}')   
      train_hist[t] = loss.item()
    return model.eval(), train_hist, test_hist
class LinearRegression1(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1,1000)
        self.hidden = torch.nn.Linear(1000,1)
        
    def forward(self,x):
        out = self.linear(x)
        out = self.hidden(out)
        return out
class LinearRegression(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1,200)
        self.hidden = torch.nn.Linear(200,1)
        
    def forward(self,x):
        out = self.linear(x)
        out = self.hidden(out)
        return out
def seir(y,t,b,a,g,p,u,N): 
    dy=[0,0,0,0,0,0]
    S=N-sum(y);
    dy[0]=np.dot(b[1:3],y[1:3])*S-a*y[0] # E
    dy[1]= a*y[0]-(g[1]+p[1])*y[1] #I1
    dy[2]= p[1]*y[1] -(g[2]+p[2])*y[2] #I2
    dy[3]= p[2]*y[2] -(g[3]+u)*y[3] #I3
    dy[4]= np.dot(g[1:3],y[1:3]) #R
    dy[5]=u*y[3] #D

    return dy
path=os.getcwd()
path = path+'/backend/simulate/'
rateModel = torch.load(path+'rate.pth')
daysModel = torch.load(path+'days.pth')
IncubPeriod=3.22 
DurMildInf=15.04 
FracMild=0.1  
FracSevere=0.95 
FracCritical=0.05 
CFR=0.97 
TimeICUDeath=1.072 
DurHosp=10.275 
N=1000
b=np.zeros(4) 
g=np.zeros(4) 
p=np.zeros(3)
a=1/IncubPeriod
u=(1/TimeICUDeath)*(CFR/FracCritical)
g[3]=(1/TimeICUDeath)-u
p[2]=(1/DurHosp)*(FracCritical/(FracCritical+FracSevere))
g[2]=(1/DurHosp)-p[2]
g[1]=(1/DurMildInf)*FracMild
p[1]=(1/DurMildInf)-g[1]
b=2.5e-4*np.array([1,1,1,1]) 
R0=N*((b[1]/(p[1]+g[1]))+(p[1]/(p[1]+g[1]))*(b[2]/(p[2]+g[2])+ (p[2]/(p[2]+g[2]))*(b[3]/(u+g[3]))))
tmax=160
tvec=np.arange(0,tmax,1)
ic=np.zeros(6)
ic[0]=1
soln=odeint(seir,ic,tvec,args=(b,a,g,p,u,N))
soln=np.hstack((N-np.sum(soln,axis=1,keepdims=True),soln))
casePer = [i[2]+i[3]+i[4] for i in soln]




def AcquireData(population,transport,infected):
  global daysModel
  global rateModel
  global casePer 
  scale = [float(population/1000)]
  transportList = [float(reduce(lambda x,y:x+y,transport))]
  transportList = [i/len(transportList) for i in transportList]
  scaledInfected = float(infected/scale[0])
  infectedList = [scaledInfected]
  daysResult = daysModel(torch.from_numpy(np.array(infectedList)))
  scaleResult = rateModel(torch.from_numpy(np.array(infectedList)))
  day = int(daysResult)+1
  scale = float(scale[0])
  returnListRaw = casePer[day:]
  returnList = []
  for i in returnListRaw:
    temp =0
    if i>0:
      returnList.append(i*scale*float(scaleResult))
    else:
      returnList.append(float(0.0))
  repairIndex=0
  flag = 0
  if returnList[0]<infected:
    flag = 1
    for i in range(len(returnList)):
      if returnList[i]>infected:
        repairIndex = i
        break
  if flag == 1:
    returnList = returnList[repairIndex:]

  return returnList

def AcquireAllData(popuList,transMatrix,infectedList):
  length = len(popuList)
  returnList = []
  for i in range(length):
    returnList.append(AcquireData(popuList[i],transMatrix[i],infectedList[i]))
  return returnList


def GetPredict(popuList,transMatrix,infectedList):
    return AcquireAllData(popuList,transMatrix,infectedList)
  
if __name__ == '__main__':
  #print(GetPredict([2000,4000],[[50,60],[120,40]],[100,256]))
  print(GetPredict(eval(sys.argv[1]),eval(sys.argv[2]),eval(sys.argv[3])))
