import ROOT
import numpy as np
dnnfilename = '../samples/predicted_samples/dnn_sv3000.root'#'ZprimeM6000ToTauTau.root'
svffilename = '../samples/predicted_samples/ZprimeM3000ToTauTau.root'
dnntreename = 'analysisTree'
svftreename = 'analysisTree'
df_dnn = ROOT.RDataFrame(dnntreename,dnnfilename)
df_svf = ROOT.RDataFrame(svftreename,svffilename)



hist_dnn = df_dnn.Define('Mres_dnn',"(dnn_mass-boson_mass)/boson_mass").Histo1D(("Mres_dnn","",40,-2,2),"Mres_dnn")

hist_svfit = df_svf.Define('Mres_mAN',"(dnn_mass-boson_mass)/boson_mass").Histo1D(("Mres_mAN","",40,-2,2),"Mres_mAN")

c1 = ROOT.TCanvas("c1","",800,800)

hist_dnn.SetStats(0)
hist_dnn.SetLineColor(4)
hist_svfit.SetLineColor(2)
hist_dnn.SetLineWidth(5)
hist_svfit.SetLineWidth(5)

gauss_dnn = ROOT.TF1("gauss_dnn","gaus",-4,4)
gauss_svf = ROOT.TF1("gauss_svf","gaus",-4,4)

gauss_dnn.SetParameters(hist_dnn.GetMaximum(), hist_dnn.GetMean(), hist_dnn.GetRMS())
gauss_svf.SetParameters(hist_svfit.GetMaximum(), hist_svfit.GetMean(), hist_svfit.GetRMS())

gauss_dnn.SetLineColor(2)
gauss_svf.SetLineColor(4)
#hist_dnn.Fit("gauss_dnn")
#hist_svfit.Fit("gauss_svf")
hist_dnn.GetYaxis().SetRangeUser(0,180);
hist_dnn.GetXaxis().SetTitle("(M_{reco} - M_{gen})/M_{gen}")
hist_dnn.Draw("histo")
hist_svfit.Draw("histosame")

#gauss_dnn.Draw("lsame")
#gauss_svf.Draw("lsame")





leg = ROOT.TLegend(0.13, 0.67, 0.45, 0.87)
leg.SetBorderSize(0);
leg.SetHeader("#bf{DNN vs mAN} ","C");
leg.AddEntry(hist_dnn.GetPtr(),"dnn 3TeV")
leg.AddEntry(hist_svfit.GetPtr(),"mAN 3TeV")

label = ROOT.TLatex()

label.SetTextSize(0.040)


if 'WJets' in dnnfilename:
    rms_dnn = np.round(hist_dnn.GetRMS(),4)
    mean_dnn = np.round(hist_dnn.GetMean(),4)
    rms_svf = np.round(hist_svfit.GetRMS(),4)
    mean_svf = np.round(hist_svfit.GetMean(),4)
    label.DrawLatex(0.931232,205.04, "#bf{DNN}")
    label.DrawLatex(0.931232, 188.911,f'rms : {rms_dnn}')
    label.DrawLatex(0.931232, 160.313,f'mean: {mean_dnn}')
    label.DrawLatex(0.931232, 120.767, "#bf{mAN}")
    
    label.DrawLatex(0.931232, 90.076,f'rms : {rms_svf}')
    label.DrawLatex(0.931232, 70.379,f'mean: {mean_svf}')

else:
    rms_dnn = np.round(hist_dnn.GetRMS(),4)
    mean_dnn = np.round(hist_dnn.GetMean(),4)
    label.DrawLatex(0.808271,122.76, "#bf{DNN}")
    label.DrawLatex(0.808271, 114.395,f'rms : 0.18')
    label.DrawLatex(0.808271, 107,f'mean: 0.065')
    label.DrawLatex(0.808271, 97.8629, "#bf{mAN}")
    rms_svf = np.round(hist_svfit.GetRMS(),4)
    mean_svf = np.round(hist_svfit.GetMean(),4)
    label.DrawLatex(0.808271, 89.879,f'rms : {rms_svf}')
    label.DrawLatex(0.808271, 81.8952,f'mean: {mean_svf}')
leg.Draw()
c1.Draw()
c1.SaveAs("../plots/Mres_zp_mAN_3TeV.png")
c1.SaveAs("./Mres_zp.C")   

#    dnn_mean  dnn_rms  sv_mean sv_rms
#3   0.065     0.18
#4   0.035     0.106
#5   -0.069    0.109   
#6   -0.105     0.1246





