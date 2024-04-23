vector <TH1F*> getHistograms(TString inputfile,int nbins,float xmin,float xmax){
  
  TFile* rootfile = new TFile(inputfile);
  TTree* tree = (TTree*)rootfile->Get("analysisTree");


  TString histDNNname = "h_dnn";
  TString histmANname = "h_mAn";
  TString histTruname = "h_true";

  TH1F* h_true = new TH1F(histTruname,"",25,xmin,xmax);
  TH1F* h_dnn = new TH1F(histDNNname,"",nbins,xmin,xmax);
  TH1F* h_mAn = new TH1F(histmANname,"",nbins,xmin,xmax);

  tree->Draw("dnn_mass >> "+histDNNname);// && gentau_vis_eta < 2.1 && gentau_vis_eta > -2.1");
  //tree->Draw("mAn_mass >> "+histmANname,"gentau_vis_pt > 10");// && gentau_vis_eta < 2.1 && gentau_vis_eta > -2.1");
  tree->Draw("boson_mass >>"+histTruname);// && gentau_vis_eta < 2.1 && gentau_vis_eta > -2.1");


  vector<TH1F*>vec_hist;

  
  
  //vec_hist.push_back(h_mAn);
  vec_hist.push_back(h_true);
  vec_hist.push_back(h_dnn);
  
  return vec_hist;


}
void epjc_plotmaker_intra(){
  
  int nbins = 30;
  float xmin = 500;
  float xmax = 7000;

  vector<TH1F*> histosBkg;
  vector<TH1F*> histos3TeV;
  vector<TH1F*> histos4TeV;
  vector<TH1F*> histos5TeV;
  vector<TH1F*> histos6TeV;


  histos3TeV = getHistograms("../samples/predicted_samples/dnn_sv3000.root",nbins,xmin,xmax);
  histos4TeV = getHistograms("./ZprimeM4100ToTauTau.root",nbins,xmin,xmax);
  histos5TeV = getHistograms("./ZprimeM4500ToTauTau.root",nbins,xmin,xmax);
  histos6TeV = getHistograms("./ZprimeM4900ToTauTau.root",nbins,xmin,xmax);
  histosBkg  = getHistograms("../samples/predicted_samples/dnn_sv6000.root",nbins,xmin,xmax);
    
  TH1F* href = new TH1F("href","",nbins,xmin,xmax);
  href->GetXaxis()->SetTitle("invariant mass of #tau#tau final state [GeV]");
  href->GetYaxis()->SetTitle("a.u.");
  href->GetYaxis()->SetRangeUser(0,0.4);
  href->SetStats(0);
  
  href->Draw("histo");
  TLegend* leg = new TLegend(0.641834,0.703158,0.873926,0.873684);
  leg->SetNColumns(1); 
  
  //for(int i=0; i < 3; i++){
  double s1 = 1.0/histos3TeV[1]->Integral();
  histos3TeV[1]->Scale(s1);//
  histos4TeV[1]->Scale(1.0/histos4TeV[1]->Integral());
  histos5TeV[1]->Scale(1.0/histos5TeV[1]->Integral());
  histos6TeV[1]->Scale(1.0/histos6TeV[1]->Integral());
  histosBkg[1]->Scale(1.0/histosBkg[1]->Integral());
    
  histos3TeV[1]->Draw("histosame");
  histos3TeV[1]->SetLineWidth(4);
  histos3TeV[1]->SetLineColor(2);
    
  leg->AddEntry(histos3TeV[1],"DNN M_{W'} = 4 TeV","l");
  //}
  //for(int i=0; i < 3; i++){
  histos4TeV[1]->Draw("histosame");
  histos4TeV[1]->SetLineWidth(5);
  histos4TeV[1]->SetLineColor(6);
  histos4TeV[1]->SetLineStyle(7);
  leg->AddEntry(histos4TeV[1],"DNN interpolation at M_{W'} = 4.1 TeV","l");
  //}
  //for(int i=0; i < 3; i++){
  histos5TeV[1]->Draw("histosame");
  histos5TeV[1]->SetLineWidth(4);
  histos5TeV[1]->SetLineColor(46);
  leg->AddEntry(histos5TeV[1],"DNN M_{W'} = 4.5 TeV","l");
  //}
  //for(int i=0; i < 3; i++){
  histos6TeV[1]->Draw("histosame");
  histos6TeV[1]->SetLineWidth(5);
  histos6TeV[1]->SetLineColor(9);
  histos6TeV[1]->SetLineStyle(7);
  leg->AddEntry(histos6TeV[1],"DNN interpolation at M_{W'} = 4.9 TeV","l");
  //}
  //for(int i=0; i < 3; i++){
  histosBkg[1]->Draw("histosame");
  histosBkg[1]->SetLineWidth(4);
  histosBkg[1]->SetLineColor(48);
  leg->AddEntry(histosBkg[1],"DNN M_{W'} = 6 TeV","l");
  //}
  leg->Draw();
}

