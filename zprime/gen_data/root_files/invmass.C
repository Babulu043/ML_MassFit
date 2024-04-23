float calc_vismass(float px,float py,float pz,float e){
  float vis_mass = TMath::Sqrt(e*e-px*px-py*py-pz*pz);
  return vis_mass;

  
}
vector<TH1F*> invmass_hist(TString inputfile,int nbins,float xmin,float xmax){
  float tau1_e,tau1_px,tau1_py,tau1_pz,tau1_pt;
  float tau2_e,tau2_px,tau2_py,tau2_pz,tau2_pt;
  float boson_mass = -9999;

  TFile* f = new TFile(inputfile);
  TTree* t = (TTree*)f->Get("analysisTree");

  TH1F* hb = new TH1F("hb","",nbins,xmin,xmax);
  TH1F* h = new TH1F("h","",nbins,xmin,xmax);

  t->SetBranchAddress("gentau1_vis_px",&tau1_px);
  t->SetBranchAddress("gentau1_vis_py",&tau1_py);
  t->SetBranchAddress("gentau1_vis_pz",&tau1_pz);
  t->SetBranchAddress("gentau1_vis_e",&tau1_e);
  t->SetBranchAddress("gentau1_vis_pt",&tau1_pt);

  t->SetBranchAddress("gentau2_vis_px",&tau2_px);
  t->SetBranchAddress("gentau2_vis_py",&tau2_py);
  t->SetBranchAddress("gentau2_vis_pz",&tau2_pz);
  t->SetBranchAddress("gentau2_vis_e",&tau2_e);
  t->SetBranchAddress("gentau2_vis_pt",&tau2_pt);

  t->SetBranchAddress("boson_mass",&boson_mass);

  for(int i=0;i < t->GetEntries();i++){
    t->GetEntry(i);
    float px_ = tau1_px+tau2_px;
    float py_ = tau1_py+tau2_py;
    float pz_ = tau1_pz+tau2_pz;
    float e_ = tau1_e+tau2_e;
    float vis_mass = -9999;
    if(tau1_pt > 0 && tau2_pt > 0){
      vis_mass = calc_vismass(px_,py_,pz_,e_);
      boson_mass = boson_mass;
    }
    h->Fill(vis_mass);
    hb->Fill(boson_mass);
  }
  vector<TH1F*> vec;
  vec.push_back(h);
  vec.push_back(hb);
  return vec;
  
}
void invmass(){
  TH1F* href = new TH1F("href","",50,0,7500); 
  /* TH1F* h4 = new TH1F("h4","",0,8000); */
  /* TH1F* h5 = new TH1F("h5","",0,8000); */
  /* TH1F* h6 = new TH1F("h6","",0,8000); */

  /* TH1F* h3_i = new TH1F("h3_i","",0,8000); */
  /* TH1F* h4_i = new TH1F("h4_i","",0,8000); */
  /* TH1F* h5_i = new TH1F("h5_i","",0,8000); */
  /* TH1F* h6_i = new TH1F("h6_i","",0,8000); */
  
  vector<TH1F*> h3;
  vector<TH1F*> h4;
  vector<TH1F*> h5;
  vector<TH1F*> h6;
  h3 = invmass_hist("zprime_3000.root",50,0,7500);
  h4 = invmass_hist("zprime_4000.root",50,0,7500);
  h5 = invmass_hist("zprime_5000.root",50,0,7500);
  h6 = invmass_hist("zprime_6000.root",50,0,7500);

  h3[0]->SetLineColor(28);
  h3[1]->SetLineColor(28);
  h3[0]->SetLineWidth(4);
  h3[1]->SetLineWidth(4);
  h3[0]->SetLineStyle(7);

  h4[0]->SetLineColor(2);
  h4[1]->SetLineColor(2);
  h4[0]->SetLineWidth(4);
  h4[1]->SetLineWidth(4);
  h4[0]->SetLineStyle(7);

  h5[0]->SetLineColor(4);
  h5[1]->SetLineColor(4);
  h5[0]->SetLineWidth(4);
  h5[1]->SetLineWidth(4);
  h5[0]->SetLineStyle(7);

  h5[0]->SetLineColor(8);
  h5[1]->SetLineColor(8);
  h5[0]->SetLineWidth(4);
  h5[1]->SetLineWidth(4);
  h5[0]->SetLineStyle(7);

  h6[0]->SetLineColor(4);
  h6[1]->SetLineColor(4);
  h6[0]->SetLineWidth(4);
  h6[1]->SetLineWidth(4);
  h6[0]->SetLineStyle(7);
  href->GetYaxis()->SetRangeUser(0,8000);
  href->SetStats(0);

  TLatex *t1 = new TLatex(0.33,0.823,"Number of occurance");
  TLatex *t2 = new TLatex(15,20,"m_{#tau^{+} #tau^{-}} [GeV]");

  
  /* href->GetYaxis()->SetTitle("Number of occurance");  */
  /* href->GetXaxis()->SetTitle("m_{#tau^{+} #tau^{-}} [GeV]");  */
    
  href->Draw("histo");
  h3[0]->Draw("histosame");
  h3[1]->Draw("histosame");

  h4[0]->Draw("histosame");
  h4[1]->Draw("histosame");

  h5[0]->Draw("histosame");
  h5[1]->Draw("histosame");

  h6[0]->Draw("histosame");
  h6[1]->Draw("histosame");

  TLegend* leg = new TLegend();
  leg->SetNColumns(2);
  leg->AddEntry(h3[1],"M_{true},M_{Z'} = 3 TeV","l");
  leg->AddEntry(h3[0],"M_{vis},M_{Z'} = 3 TeV","l");
  leg->AddEntry(h4[1],"M_{true},M_{Z'} = 4 TeV","l");
  leg->AddEntry(h4[0],"M_{vis},M_{Z'} = 4 TeV","l");
  leg->AddEntry(h5[1],"M_{true},M_{Z'} = 5 TeV","l");
  leg->AddEntry(h5[0],"M_{vis},M_{Z'} = 5 TeV","l");
  leg->AddEntry(h6[1],"M_{true},M_{Z'} = 6 TeV","l");
  leg->AddEntry(h6[0],"M_{vis},M_{Z'} = 6 TeV","l");

  leg->Draw();
    t1->Draw();
  t2->Draw();

}
