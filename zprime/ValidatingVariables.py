import ROOT
import sys
import os 
VARIABLES = ["gentau1_vis_pt","gentau1_vis_eta","gentau1_vis_phi","gentau1_vis_e","gentau1_vis_m",
             "gentau2_vis_pt","gentau2_vis_eta","gentau2_vis_phi","gentau2_vis_e","gentau2_vis_m",
             "genmet","gen_mT","genmet_phi","gen_pTratio","gen_dtheta","covMet11","covMet12","covMet21","covMet22","boson_mass"]
rootfile_dir = './gen_data/root_files/'

list_of_files = os.listdir(rootfile_dir)


def collect_legend(listoffiles):
    leg = [filename.split('.root')[0] for filename in listoffiles]
    if len(leg) != len(list_of_files):
        raise Exception("The legend and files don't have same dimension")
    return leg
def create_histmodel(variable,xmin,xmax,nbins):
    if "pt" in variable:
        histmodel = ROOT.RDF.TH1DModel(variable, variable,xmin, xmax, nbins)
    else:
        histmodel = ROOT.RDF.TH1DModel(variable, variable,xmin, xmax, nbins)
    return histmodel
        
def collect_histo(filename,variable,condition):
    histmodel = create_histmodel(variable,0,2000,50)
    df = ROOT.RDataFrame("analysisTree",filename)
    hist = df.Filter(condition).Histo1D(histmodel,variable)
    return hist

collect_legend(list_of_files)

hist = collect_histo(rootfile_dir+list_of_files[0],"gentau1_vis_pt","gentau1_vis_pt > 0")

c = ROOT.TCanvas()
hist.Draw()
c.Draw()





