import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler,QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

class prepare_dataset:
    def __init__(self,train_df,test_df):
        #self.num_pipeline = Pipeline([('MinMaxScaler',MinMaxScaler(feature_range=(0,1))) ])
        self.num_pipeline = Pipeline([('QuantileTransformer',QuantileTransformer(random_state=0))])
        train_df = self.preselection(train_df)
        test_df  = self.preselection(test_df)
        # self.m_sv = test_df['m_sv'].to_numpy(dtype='float32')
        # test_df = test_df.drop(columns=['m_sv'])
        self.L1pT = test_df['gentau1_vis_pt'].to_numpy(dtype='float32')
        self.L2pT = test_df['gentau2_vis_pt'].to_numpy(dtype='float32')
        self.L1Eta = test_df['gentau1_vis_eta'].to_numpy(dtype='float32')
        self.L2Eta = test_df['gentau2_vis_eta'].to_numpy(dtype='float32')
        self.mET  = test_df['genmet'].to_numpy(dtype='float32')
        train_df.fillna(value=train_df.mean(),inplace=True)
        test_df.fillna(value=test_df.mean(),inplace=True)
        self.joint_array(train_df,test_df)
        
    def preselection(self,df):
        df = df[df['gentau1_vis_pt'] > 0]
        df = df[df['gentau2_vis_pt'] > 0]
        return df 
    
    def getfeaturesAndLables(self,df):
        features = df.drop(columns=['boson_mass','event_weight','class_id']).to_numpy(dtype='float32')
        labels  = df['boson_mass'].to_numpy(dtype='float32')
        return features,labels
    
    def joint_array(self,df1,df2):
        x1,y1 = self.getfeaturesAndLables(df1)
        x2,y2 = self.getfeaturesAndLables(df2)

        xjoint = np.concatenate((x1,x2),axis=0)
        yjoint = np.concatenate((y1,y2),axis=0)
        xjoint_tr = self.num_pipeline.fit_transform(xjoint)
        yjoint_tr = self.num_pipeline.fit_transform(yjoint.reshape(-1,1))

        self.xtrain = xjoint_tr[:len(x1)]
        self.ytrain = yjoint_tr[:len(y1)]

        self.xtest  = xjoint_tr[len(x1):]
        self.ytest  = yjoint_tr[len(y1):]

    def prepareTrain(self):
        feature,val_feature,label,val_label = train_test_split(self.xtrain,self.ytrain,test_size=0.33, random_state=123)
        return feature,val_feature,label,val_label
    def prepareTest(self):
        return self.xtest,self.ytest