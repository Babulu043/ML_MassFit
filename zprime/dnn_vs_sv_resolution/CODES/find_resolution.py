import ROOT
import numpy as np
filename = 'dnn_svback.root'
treename = 'analysisTree'
df = ROOT.RDataFrame(treename,filename)



hist_dnn = df.Define('Mres_dnn',"(dnn_mass-boson_mass)/boson_mass").Histo1D(("Mres_dnn","",50,-2,2),"Mres_dnn")

hist_svfit = df.Define('Mres_svfit',"(m_sv-boson_mass)/boson_mass").Histo1D(("Mres_svfit","",50,-2,2),"Mres_svfit")

c1 = ROOT.TCanvas()
hist_dnn.SetStats(0)
hist_dnn.SetLineColor(2)
hist_dnn.SetLineWidth(4)
hist_svfit.SetLineWidth(4)

gauss_dnn = ROOT.TF1("gauss_dnn","gaus",-4,4)
gauss_svf = ROOT.TF1("gauss_svf","gaus",-4,4)

gauss_dnn.SetParameters(hist_dnn.GetMaximum(), hist_dnn.GetMean(), hist_dnn.GetRMS())
gauss_svf.SetParameters(hist_svfit.GetMaximum(), hist_svfit.GetMean(), hist_svfit.GetRMS())

gauss_dnn.SetLineColor(2)
gauss_svf.SetLineColor(4)
#hist_dnn.Fit("gauss_dnn")
#hist_svfit.Fit("gauss_svf")
hist_dnn.GetYaxis().SetRangeUser(0,120);
hist_dnn.GetXaxis().SetTitle("M_{reco} - M_{gen}/M_{gen}")
hist_dnn.Draw("histo")
hist_svfit.Draw("histosame")
#gauss_dnn.Draw("lsame")
#gauss_svf.Draw("lsame")





leg = ROOT.TLegend(0.13, 0.67, 0.45, 0.87)
leg.SetHeader("#bf{DNN vs SVfit} ","C");
leg.AddEntry(hist_dnn.GetPtr(),"dnn background")
leg.AddEntry(hist_svfit.GetPtr(),"SvFit background")

label = ROOT.TLatex()

label.SetTextSize(0.040)
label.DrawLatex(.70, 89.06, "#bf{DNN}")
rms_dnn = np.round(hist_dnn.GetRMS(),4)
mean_dnn = np.round(hist_dnn.GetMean(),4)
label.DrawLatex(.70, 79.0,f'rms : {rms_dnn}')
label.DrawLatex(.70, 69.0,f'mean: {mean_dnn}')
label.DrawLatex(.70, 50.06, "#bf{SvFit}")
rms_svf = np.round(hist_svfit.GetRMS(),4)
mean_svf = np.round(hist_svfit.GetMean(),4)
label.DrawLatex(.70, 40.06,f'rms : {rms_svf}')
label.DrawLatex(.70, 30.06,f'mean: {mean_svf}')

leg.Draw()
             
c1.SaveAs("root.png")
c1.SaveAs("root.C")   

#    dnn  sv
#3  1.30  1.215
#4  9.25  1.259
#5  2.262 1.192
#6  1.116 1.179





