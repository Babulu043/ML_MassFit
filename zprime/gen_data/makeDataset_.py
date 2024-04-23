import ROOT
import pandas as pd
import numpy as np
import os
from sklearn.utils import shuffle


class makeDataset:
    def __init__(self,rootfile):
        tree_df = ROOT.RDataFrame('analysisTree',rootfile)
        self.train_df  = tree_df.Filter('gentau1_vis_px > -9999')
    def get_df(self,df):
        dataframe = pd.DataFrame(self.load_data(df),columns=self.getFeatures())
        return dataframe
        

    def setFeatures(self,*var):
        self.features = [v for v in var]
        return self.features

    def getFeatures(self):
        return self.features
    
    def load_data(self,df):
        feature_list = self.getFeatures()
        tree_ar = df.AsNumpy()
        feature_dict = self.get_Inputs(tree_ar,feature_list)
        data_ar = []
        for key in feature_dict.keys():
            data_ar.append(feature_dict[key])
        data = np.stack(tuple(data_ar),axis=1)
        return data

    def saveCSV(self,path,data,filename):
        feature_head = self.getFeatures()
        DataFrame = pd.DataFrame(data,columns=feature_head)
        DataFrame.to_csv(path+'/'+filename,index=False)
        
        
    def get_Inputs(self,df,col_list):
        input_dict = {}
        for col in col_list:
            item = df[col]
            input_dict[col] = item
        return input_dict


 
        


inputFile1 = "zprime_3750.root"
trainFile  = "3750.csv"

traindataset1 = makeDataset(inputFile1)
traindataset1.setFeatures(
    'gentau1_vis_px',
    'gentau1_vis_py',
    'gentau1_vis_pz',
    'gentau1_vis_e',
    'gentau1_vis_pt',
    'gentau1_vis_eta',
    'gentau1_vis_phi',
    'gentau1_vis_m',
    'gentau2_vis_px',
    'gentau2_vis_py',
    'gentau2_vis_pz',
    'gentau2_vis_e',
    'gentau2_vis_pt',
    'gentau2_vis_eta',
    'gentau2_vis_phi',
    'gentau2_vis_m',
    'genmet',
    'genmet_px',
    'genmet_py',
    'genmet_phi',
    'boson_mass',
    'event_weight',
    'class_id'
)

traincsvfile = traindataset1.get_df(traindataset1.train_df)
for _ in range(16):
    traincsvfile = shuffle(traincsvfile)



traincsvfile.to_csv(trainFile,index=False)







