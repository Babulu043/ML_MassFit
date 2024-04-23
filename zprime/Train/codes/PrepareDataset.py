import ROOT
import sys
import pandas as pd
import numpy as np

train_variables = ["gentau1_vis_px","gentau1_vis_py","gentau1_vis_pz","gentau1_vis_e","gentau1_vis_pt","gentau1_vis_eta","gentau1_vis_phi","gentau1_vis_m",
                   "gentau2_vis_px","gentau2_vis_py","gentau2_vis_pz","gentau2_vis_e","gentau2_vis_pt","gentau2_vis_eta","gentau2_vis_phi","gentau2_vis_m","genmet",
                   "genmet_px","genmet_py","genmet_phi","boson_mass","event_weight","class_id"]

class PrepareDatasetForSVFit:
    def __init__(self,file_input,file_output):
        rdf = ROOT.RDataFrame("analysisTree",file_input)
        rdf = rdf.Filter("gentau1_vis_pt > 0 && gentau2_vis_pt > 0")

        px_mean = rdf.Define("mean_px","genmet_px").Mean("mean_px").GetValue()
        py_mean = rdf.Define("mean_py","genmet_py").Mean("mean_py").GetValue()


        rdf = rdf.Define("metpx_mean",str(px_mean))
        rdf = rdf.Define("metpy_mean",str(py_mean))

        sum_Xavg_squre = rdf.Define("Xavg_square","(genmet_px - metpx_mean)*(genmet_px - metpx_mean)").Sum("Xavg_square").GetValue()
        sum_Yavg_squre = rdf.Define("Yavg_square","(genmet_py - metpy_mean)*(genmet_py - metpy_mean)").Sum("Yavg_square").GetValue()
        sum_XYavg_squre = rdf.Define("XYavg_square","(genmet_px - metpx_mean)*(genmet_py - metpy_mean)").Sum("XYavg_square").GetValue()

        covMet_XX = sum_Xavg_squre/rdf.Count().GetValue()
        covMet_YY = sum_Yavg_squre/rdf.Count().GetValue()
        covMet_XY = sum_XYavg_squre/rdf.Count().GetValue()

        rdf = rdf.Define("covMet11",str(covMet_XX))
        rdf = rdf.Define("covMet12",str(covMet_XY))
        rdf = rdf.Define("covMet21",str(covMet_XY))
        rdf = rdf.Define("covMet22",str(covMet_YY))

        branchs = train_variables+["covMet11","covMet12","covMet21","covMet22"]

        branch_list = ROOT.vector('string')()
        for branchname in branchs:
            branch_list.push_back(branchname)

        rdf.Snapshot("analysisTree",str(sys.argv[2]),branch_list)



import os
from sklearn.utils import shuffle


class makeDataset:
    def __init__(self,rootfile):
        tree_df = ROOT.RDataFrame('analysisTree',rootfile)
        self.train_df  = tree_df.Filter('gentau1_vis_px > -9999')
    def get_df(self,df):
        dataframe = pd.DataFrame(self.load_data(df),columns=self.getFeatures())
        return dataframe
        

    def setFeatures(self,vars):
        self.features = vars#[v for v in var]

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


 
        


inputFile = sys.argv[1]
outputFile  = sys.argv[2]
if '.csv' in outputFile:
    print("Producing CSV file for DNN training")
    trainDataset = makeDataset(inputFile)
    train_variables = train_variables + ['m_sv']
    trainDataset.setFeatures(train_variables)
    traincsvfile = trainDataset.get_df(trainDataset.train_df)
    for _ in range(16):
        traincsvfile = shuffle(traincsvfile)
    traincsvfile.to_csv(outputFile,index=False)
elif '.root' in outputFile:
    PrepareDatasetForSVFit(inputFile,outputFile)
else:
    print("provide right dataformat")







