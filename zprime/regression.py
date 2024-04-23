import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from keras.layers import LeakyReLU
import uproot3 as ROOT
import awkward as aw
from root_numpy import root2array, rec2array, array2root, tree2array
import argparse
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
parser = argparse.ArgumentParser()
parser.add_argument("-i1","--inputFile1",help="give the input root file to Train")

parser.add_argument("-i2","--inputFile2",help="give the input root file to Test")

parser.add_argument("-t","--train",help="to train the model",action="store_true")
parser.add_argument("-n","--nepoch",type=int,help="no. of epochs",default=100)
parser.add_argument("-m","--model",help="model name to save or load with .h5 format",default="regression_model.h5")
parser.add_argument("-p","--train_m",help="model name to save training",default="training.png")

parser.add_argument("-s","--isSignal",help="boolean for signal",action="store_true")

parser.add_argument("-nm","--name",help="give the name root file to save")
args = parser.parse_args()
    



def plot_loss(history):
    fig1,ax1 = plt.subplots()
    ax1.plot(history.history['loss'], label='loss')
    ax1.plot(history.history['val_loss'], label='val_loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Error [MPG]')
    ax1.legend()
    ax1.set_ylim(0,.1 )
    fig1.savefig('../plots/'+ args.train_m+'.png')
    ax1.grid(True)
    a= history.history['loss']
    b= history.history['val_loss']
    df = pd.DataFrame({"loss" : a, "vall_loss" : b})
    df.to_csv('../plots/'+ args.train_m+'.csv', index=False)

num_pipeline = Pipeline([('MinMaxScaler',MinMaxScaler(feature_range=(0,1))) ])


print(15*'==')

    
    

TrainDataSet = pd.read_csv(args.inputFile1,index_col=False)
TrainDataSet.fillna(value=TrainDataSet.mean(),inplace=True)
#TrainDataSet = TrainDataSet[(TrainDataSet.boson_mass >1000)]

TestDataSet = pd.read_csv(args.inputFile2,index_col=False) 
TestDataSet.fillna(value=TestDataSet.mean(),inplace=True)
TestDataSet = TestDataSet[(TestDataSet.boson_mass >2850)]
TestDataSet= TestDataSet[(TestDataSet.boson_mass < 6200)]


training_features = TrainDataSet.drop(columns=['boson_mass','event_weight','class_id']).to_numpy(dtype='float32')
training_labels  = TrainDataSet['boson_mass'].to_numpy(dtype='float32')
training_weight  = TrainDataSet['event_weight'].to_numpy(dtype='float32')

print(training_labels.shape[0])
#'gentau1_vis_pt','gentau2_vis_pt','gentau1_vis_m','gentau2_vis_m','gentau1_vis_eta','gentau1_vis_phi','gentau2_vis_eta','gentau2_vis_phi','genmet','genmet_phi','boson_mass','weight',

#xstar  = TestDataSet.drop(columns=['gentau1_vis_pt','gentau2_vis_pt','gentau1_vis_m','gentau2_vis_m','gentau1_vis_eta','gentau1_vis_phi','gentau2_vis_eta','gentau2_vis_phi','genmet','genmet_phi','boson_mass','event_weight','class_id']).to_numpy(dtype='float32')


xstar = TestDataSet.drop(columns=['boson_mass','event_weight','class_id']).to_numpy(dtype='float32')

ystar  = TestDataSet['boson_mass'].to_numpy(dtype='float32') 
xstarweight  = TestDataSet['event_weight'].to_numpy(dtype='float32')   

xtrain_star = np.concatenate((training_features,xstar),axis=0)
ytrain_star = np.concatenate((training_labels,ystar),axis=0)

xtrain_star_tr = num_pipeline.fit_transform(xtrain_star)  
ytrain_star_tr = num_pipeline.fit_transform(ytrain_star.reshape(-1,1))
weight_tr = training_weight.reshape(-1,1)

xtrain = xtrain_star_tr[:len(training_features)]
xstar_tr = xtrain_star_tr[len(training_features):]

ytrain = ytrain_star_tr[:len(training_features)]
ystar_tr = ytrain_star_tr[len(training_features):]




xtrain_tr,xtest_tr,ytrain_tr,ytest_tr = train_test_split(xtrain,ytrain, test_size=0.33, random_state=123)
x1,x2,wtrain,x3 = train_test_split(xtrain,weight_tr, test_size=0.33, random_state=123)


def peak_position_loss(y_true, y_pred):
    peak_distance = tf.abs(y_true - y_pred)
    base_loss = tf.reduce_mean(tf.square(y_true - y_pred))
    scaling_factor = tf.math.exp(-peak_distance)
    loss = scaling_factor * base_loss
    
    return loss

if(args.train == True):
    input_dim = xtrain.shape[1]
else:
    input_dim = xstar.shape[1]


#fig,ax = plt.subplots()
#ax.hist(TrainDataSet['boson_mass'] ,bins=100,log=False,label="true mass",range=(2500,6500))
#plt.show()

def build_model(layer_geom,learning_rate=1e-5,input_shapes=[20]):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=input_shapes))
    for layer in layer_geom:
        model.add(keras.layers.Dense(layer_geom[layer],activation='relu'))
        model.add(LeakyReLU(alpha=0.5))
        #model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dropout(0.1))

    model.add(keras.layers.Dense(1,activation='linear',kernel_initializer='normal'))
    model.compile(loss='mean_absolute_error',optimizer='adam')
    return model
    
#hlayer_outline = {'hlayer1':1000,'hlayer2':1000,'hlayer4':1000,'hlayer5':1000}
#hlayer_outline = {'hlayer1':128,'hlayer2':128,'hlayer3':128,'hlayer4':128}
hlayer_outline = {'hlayer1':64,'hlayer2':128,'hlayer3':128,'hlayer4':64}
model = build_model(hlayer_outline,input_shapes=[input_dim])
model.summary()
if args.train:
    early_stopping_cb = keras.callbacks.EarlyStopping(patience=50,restore_best_weights=True)
    checkpoint_cb = keras.callbacks.ModelCheckpoint("../models/"+args.model,save_best_only=True)
    history = model.fit(xtrain_tr,ytrain_tr, epochs=args.nepoch,batch_size =1024,validation_data=(xtest_tr,ytest_tr),callbacks=[checkpoint_cb])#,early_stopping_cb])
    #history = model.fit(xtrain_tr,ytrain_tr, epochs=args.nepoch,batch_size =64,validation_data=(xtest_tr,ytest_tr),callbacks=[checkpoint_cb])#,early_stopping_cb])
    plot_loss(history)
else:
    model = keras.models.load_model("../models/"+args.model)

    #model = keras.models.load_model("../models/"+args.model, custom_objects={"peak_position_loss": peak_position_loss})

filename = 'background.root' #'invariant_mass_5TEV_tr100_background.root'
if args.isSignal:
    filename = 'signal.root'
range1=(0,6500)
if args.isSignal:
    range1=(0,6300)
if(args.train == False):

    y_pred_tr = model.predict(xstar_tr)
    y_pred = num_pipeline.inverse_transform(y_pred_tr.reshape(-1,1))
    fig2,ax2 = plt.subplots()
    branch1 = np.array(y_pred,dtype=[("dnn_mass",'float32')])
    branch2 = np.array(ystar,dtype=[("boson_mass",'float32')])
    branch3 = np.array(xstarweight,dtype=[("event_weight",'float32')])               
    array2root(branch1,filename,'tree',mode='recreate')
    array2root(branch2,filename,'tree',mode='update')
    array2root(branch3,filename,'tree',mode='update')
    
    
    ax2.hist(ystar ,bins=50,log=True,label="true mass",range=range1)
    ax2.hist(y_pred,bins=50,log=True,label="regression mass",range=range1)

    ax2.set_xlabel('invariant mass')
    ax2.set_ylabel('Events [a.u]')
    #print(y_pred)
    plt.legend()
    plt.show()
    #fig2.savefig('../plots/invariant_mass_5TEV_tr100.png')
    

