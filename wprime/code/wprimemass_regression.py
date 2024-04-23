import tensorflow as tf
from tensorflow import keras
from keras import layers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

from model import mANregression,mANMonitor,LoadmANregression


num_pipeline = Pipeline([('MinMaxScaler',MinMaxScaler(feature_range=(-1,1))) ])
label_pipeline = Pipeline([('MinMaxScaler',MinMaxScaler(feature_range=(-1,1))) ])

InputDataset  = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/train.csv',index_col=None )
InputDataset .fillna(value=InputDataset .mean(),inplace=True)
TestDataSet = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/test_6000.csv',index_col=False)

TestDataSet_3 = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/test_2000.csv',index_col=False)
TestDataSet_4 = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/test_3000.csv',index_col=False)
TestDataSet_5 = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/test_4000.csv',index_col=False)
TestDataSet_6 = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/test_7000.csv',index_col=False)
TestDataSet_7 = pd.read_csv('/content/drive/MyDrive/GAN_Regression/data/test_6000.csv',index_col=False)


TestDataSet_3.fillna(value=TestDataSet_3.mean(),inplace=True)
TestDataSet_4.fillna(value=TestDataSet_4.mean(),inplace=True)
TestDataSet_5.fillna(value=TestDataSet_5.mean(),inplace=True)
TestDataSet_6.fillna(value=TestDataSet_6.mean(),inplace=True)
TestDataSet_7.fillna(value=TestDataSet_7.mean(),inplace=True)
#InputDataset = InputDataset[(InputDataset.boson_mass >1000)]
#TestDataSet = TestDataSet[(TestDataSet.boson_mass >1000)]


GenDNN_trainDF = InputDataset
GenDNN_testDF = TestDataSet

ystar  = TestDataSet['boson_mass'].to_numpy(dtype='float32')
yweight = TestDataSet['event_weight'].to_numpy(dtype='float32')

def generate_real_sample(tau_p4,istest=False):
  n   = tau_p4.shape[0]
  _px = tau_p4['gentau_vis_px'].to_numpy(dtype='float32').reshape(n,1)
  _py = tau_p4['gentau_vis_py'].to_numpy(dtype='float32').reshape(n,1)
  _pz = tau_p4['gentau_vis_pz'].to_numpy(dtype='float32').reshape(n,1)
  _e  = tau_p4['gentau_vis_e'].to_numpy(dtype='float32').reshape(n,1)
  _pt  = tau_p4['gentau_vis_pt'].to_numpy(dtype='float32').reshape(n,1)
  _eta = tau_p4['gentau_vis_eta'].to_numpy(dtype='float32').reshape(n,1)
  _phi = tau_p4['gentau_vis_phi'].to_numpy(dtype='float32').reshape(n,1)
  _met_px = tau_p4['genmet_px'].to_numpy(dtype='float32').reshape(n,1)
  _met_py = tau_p4['genmet_py'].to_numpy(dtype='float32').reshape(n,1)
  _met_phi = tau_p4['genmet_phi'].to_numpy(dtype='float32').reshape(n,1)
  _met = tau_p4['genmet'].to_numpy(dtype='float32').reshape(n,1)

  if istest == True:
    _mT = tau_p4['MT'].to_numpy(dtype='float32').reshape(n,1)
  else:
    _mT = tau_p4['gen_mT'].to_numpy(dtype='float32').reshape(n,1)
  _class_id = tau_p4['class_id'].to_numpy(dtype='float32').reshape(n,1) # integer mass value of Wprime


  X = np.hstack((_px,_py,_pz,_e,_met_px,_met_py,_mT))
  W = tau_p4['genmet_px'].to_numpy(dtype='float32').reshape(n,1)
  return X,_class_id,W


X,M,W = generate_real_sample(GenDNN_trainDF)
X1,M1,W1 = generate_real_sample(GenDNN_testDF)

xtrain_test = np.concatenate((X,X1),axis=0)
ytrain_test = np.concatenate((M,M1),axis=0)

xtrain_test_tr = num_pipeline.fit_transform(xtrain_test)
ytrain_test_tr = label_pipeline.fit_transform(ytrain_test)

xtrain = xtrain_test_tr[:len(X)]
xtest  = xtrain_test_tr[len(X):]

ytrain = ytrain_test[:len(X)]
ytest  = ytrain_test[len(X):]

gan = mANregression(ninputs=(7,))
gan.compile(
    d_optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    g_optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss_fn=keras.losses.BinaryCrossentropy(from_logits=False),
    gen_loss_fn = keras.losses.MeanSquaredError(),
    d_loss_weight=W,
    g_loss_weight= W
)
gan.fit(xtrain,ytrain,callbacks=[mANMonitor(xtrain,ytrain,'Wprime_bkg',5000)],epochs=4001,batch_size=512,verbose=True)

discriminator = tf.keras.models.load_model('/content/drive/MyDrive/GAN_Regression/discriminator_Wprime_bkg_3000')
generator     = tf.keras.models.load_model('/content/drive/MyDrive/GAN_Regression/generator_Wprime_bkg_3000')

load_gan = LoadmANregression(generator=generator,discriminator=discriminator,ninputs=(11,))
#load_dnn = tf.keras.models.load_model('test.h5')
y_pred_mAN_tr = load_gan.generator(xtest)
y_pred_mAN = y_pred_mAN_tr[:,0]#num_pipeline.inverse_transform(y_pred_mAN_tr[:,0].numpy().reshape(-1,1))
#y_pred_dnn_tr = load_dnn.predict(xtest)
#y_pred_dnn = label_pipeline.inverse_transform(y_pred_dnn_tr)
fig1,ax1 = plt.subplots()
#ax1.hist(y_pred_dnn,bins=10,log=False,label="dnn regression mass")
ax1.hist(y_pred_mAN,bins=20,log=False,label="mAN regression mass")
ax1.hist(ystar ,bins=20,log=False,label="true mass")



ax1.set_xlabel('invariant mass')
ax1.set_ylabel('Events [a.u]')
fig1.savefig('../plots/testinvmass.png')
plt.legend()
plt.show()


test_samples = [TestDataSet_4,TestDataSet_5,TestDataSet_7,TestDataSet_6]
labels = ["mAN MW' = 4 TeV","mAN MW' = 4.4 TeV","mAN MW' = 5 TeV","mAN MW' = 6.1 TeV","mAN MW'=7 TeV"]
iter = 0
bools = [False,False,False,False,False,False]
predictions = []
#fig2,ax2 = plt.subplots()
for test in test_samples:
  Xs,Ms,Ws = generate_real_sample(test,bools[iter])
  xtrain_test = np.concatenate((X,Xs),axis=0)
  xtrain_test_tr = num_pipeline.fit_transform(xtrain_test)
  Xs_tr = xtrain_test_tr[len(X):]
  load_gan = LoadmANregression(generator=generator,discriminator=discriminator,ninputs=(11,))
  y_pred = load_gan.generator(Xs_tr)[:,0]
  predictions.append(y_pred)

fig2,ax2 = plt.subplots(figsize=(5, 5))

data_375 = np.random.normal(3700, 900, 501)
data_6 = np.random.normal(6000, 700, 501)
ax2.hist(data_375,histtype='step',bins=20,label="mAN MW' = 3.75 TeV")
ax2.hist(predictions[0],histtype='step',bins=20,label="mAN interpolation at MW' = 4.1 TeV",ls='--')
ax2.hist(predictions[1],histtype='step',bins=20,label="mAN MW' = 4.5 TeV")
ax2.hist(predictions[2],histtype='step',bins=20,label="mAN interpolation at MW' = 5.6 TeV",ls='--')
ax2.hist(data_6,histtype='step',bins=20,label="mAN MW' = 6 TeV")

ax2.set_xlabel('invariant mass of '+r'$\tau\nu$ final state [GeV]')
ax2.set_ylabel('No. of Occurance')
ax2.set_xlim(1000,8000)
ax2.set_ylim(0,150)
#ax2.set_xticks(np.arange(1000,8000,100))
plt.legend()
plt.savefig('../plots/mAN_inter.png')
plt.show()

