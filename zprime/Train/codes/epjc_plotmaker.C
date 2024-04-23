vector <TH1F*> getHistograms(TString inputfile,int nbins,float xmin,float xmax){
  
  TFile* rootfile = new TFile(inputfile);
  TTree* tree = (TTree*)rootfile->Get("analysisTree");


  TString histDNNname = "h_dnn";
  TString histmANname = "h_mAn";
  TString histTruname = "h_true";

  TH1F* h_true = new TH1F(histTruname,"",nbins,xmin,xmax);
  TH1F* h_dnn = new TH1F(histDNNname,"",nbins,xmin,xmax);
  TH1F* h_mAn = new TH1F(histmANname,"",nbins,xmin,xmax);

  tree->Draw("dnn_mass >> "+histDNNname);// && gentau_vis_eta < 2.1 && gentau_vis_eta > -2.1");
  tree->Draw("m_sv >> "+histmANname);// && gentau_vis_eta < 2.1 && gentau_vis_eta > -2.1");
  //tree->Draw("boson_mass >>"+histTruname,"gentau_vis_pt > 10");// && gentau_vis_eta < 2.1 && gentau_vis_eta > -2.1");


  vector<TH1F*>vec_hist;
  h_dnn->Scale(1.0/h_dnn->Integral());
  h_mAn->Scale(1.0/h_mAn->Integral());
  //vec_hist.push_back(h_true);
  vec_hist.push_back(h_dnn);
  vec_hist.push_back(h_mAn);

  return vec_hist;


}
void epjc_plotmaker(){
  
  int nbins = 25;
  float xmin = 3500;
  float xmax = 5500;

  vector<TH1F*> histos3TeV;
  vector<TH1F*> histos4TeV;
  vector<TH1F*> histos5TeV;
  vector<TH1F*> histos6TeV;

  histos3TeV = getHistograms("./ZprimeM3000ToTauTau.root",nbins,xmin,xmax);
  histos4TeV = getHistograms("./ZprimeM4000ToTauTau.root",nbins,xmin,xmax);
  histos5TeV = getHistograms("./ZprimeM5000ToTauTau.root",nbins,xmin,xmax);
  histos6TeV = getHistograms("./ZprimeM6000ToTauTau.root",nbins,xmin,xmax);

  TH1F* href = new TH1F("href","",nbins,xmin,xmax);
  href->GetXaxis()->SetTitle("invariant mass of #tau#tau final state [GeV]");
  href->GetYaxis()->SetTitle("No. of occurance");
  href->GetYaxis()->SetRangeUser(0,0.8);
  href->SetStats(0);
  
  href->Draw("histo");
  TLegend* leg = new TLegend(0.641834,0.703158,0.873926,0.873684);
  leg->SetNColumns(2);
  for(int i=0; i < 2; i++){
    histos3TeV[i]->Draw("histosame");
    histos3TeV[i]->SetLineWidth(3);
    histos3TeV[i]->SetLineColor(8);
    if(i == 0){
      leg->AddEntry(histos3TeV[i],"DNN M_{Z'} = 3 TeV","l");
    }
    else{
      leg->AddEntry(histos3TeV[i],"SV fit M_{Z'} = 3 TeV","l");
      histos3TeV[i]->SetLineStyle(7);
    }
  }
  for(int i=0; i < 2; i++){
    histos4TeV[i]->Draw("histosame");
    histos4TeV[i]->SetLineWidth(3);
    histos4TeV[i]->SetLineColor(9);
    if(i == 0){
      leg->AddEntry(histos4TeV[i],"DNN M_{Z'} = 4 TeV","l");
    }
    else{
      leg->AddEntry(histos4TeV[i],"SV fit M_{Z'} = 4 TeV","l");
      histos4TeV[i]->SetLineStyle(7);
    }
  }
  for(int i=0; i < 2; i++){
    histos5TeV[i]->Draw("histosame");
    histos5TeV[i]->SetLineWidth(3);
    histos5TeV[i]->SetLineColor(46);
    if(i == 0){
      leg->AddEntry(histos5TeV[i],"DNN M_{Z'} = 5 TeV","l");
    }
    else{
      leg->AddEntry(histos5TeV[i],"SV fit M_{Z'} = 5 TeV","l");
      histos5TeV[i]->SetLineStyle(7);
    }
  }
  for(int i=0; i < 2; i++){
    histos6TeV[i]->Draw("histosame");
    histos6TeV[i]->SetLineWidth(3);
    histos6TeV[i]->SetLineColor(49);
    if(i == 0){
      leg->AddEntry(histos6TeV[i],"DNN M_{Z'} = 6 TeV","l");
    }
    else{
      leg->AddEntry(histos6TeV[i],"SV fit M_{Z'} = 6 TeV","l");
      histos6TeV[i]->SetLineStyle(7);
    }
  }
  leg->Draw();
}

