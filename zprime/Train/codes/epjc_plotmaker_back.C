void epjc_plotmaker(){
  TFile* rootfile = new TFile("./DYJetsToTauTau_noSVFit.root");
  TTree* tree = (TTree*)rootfile->Get("t");

  TH1F* h_true = new TH1F("h_true","",40,0,200);
  TH1F* h_dnn = new TH1F("h_dnn","",40,0,200);
  TH1F* h_svf = new TH1F("h_svf","",30,0,200);

  tree->Draw("dnn_mass >> h_dnn","gentau1_vis_pt > 30 && gentau2_vis_pt > 30 ");
  tree->Draw("svfit_mass >> h_svf","gentau1_vis_pt > 30 && gentau2_vis_pt > 30 ");
 tree->Draw("boson_mass >> h_true","gentau1_vis_pt > 30 && gentau2_vis_pt > 30 "); 

  // histo styles
  h_dnn->SetLineColor(kRed);
  h_dnn->SetLineWidth(3);
  h_svf->SetLineColor(kGreen);
  h_svf->SetLineWidth(3);
  h_true->SetLineWidth(3);
  
  TH1F* href = new TH1F("href","",20,0,200);
  href->GetYaxis()->SetRangeUser(0,1200);

  TCanvas* c1 = new TCanvas("c1","c1",800,700);
  href->Draw("histo");
  h_true->Draw("histosame");
  h_dnn->Draw("histosame");
  h_svf->Draw("histosame");

  href->SetStats(0);
  href->GetXaxis()->SetTitle("invariant mass of #tau#tau final state [GeV]");
  href->GetYaxis()->SetTitle("No. of Occurance");

  //TLatex* label = new TLatex();
  //label->DrawLatex(11.0276,584.259, "#tau pT > 30 GeV");
  //legend
  TLegend* leg = new TLegend(0.641834,0.703158,0.873926,0.873684);
  leg->AddEntry("h_true","Z boson mass","l");
  leg->AddEntry("h_dnn","DNN M_{Z} = 90 GeV","l");
  leg->AddEntry("h_svf","SvFit M_{Z} = 90 GeV","l");
  leg->SetBorderSize(0);

  
  
  leg->Draw();

  
 

}
