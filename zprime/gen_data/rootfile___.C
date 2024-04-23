#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>
 
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"
 
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
 
using namespace TMVA;

 vector<float>covm( vector<float>genmet_px_, vector <float> genmet_py_){ 


float avg_genmet_px_=   accumulate( genmet_px_.begin(), genmet_px_.end(), 0.0)/ genmet_px_.size();

float avg_genmet_py_=   accumulate( genmet_py_.begin(), genmet_py_.end(), 0.0)/ genmet_py_.size();

vector<float> gx;
vector<float> gy;
vector<float> gxy;
for(Int_t i = 0; i < genmet_px_.size(); i++){


    float gvar_x_ = (genmet_px_[i] - avg_genmet_px_)*(genmet_px_[i] - avg_genmet_px_);
    float gvar_y_ = (genmet_py_[i] - avg_genmet_py_)*(genmet_py_[i] - avg_genmet_py_);
    float gvar_xy_ = (genmet_px_[i] - avg_genmet_px_)*(genmet_py_[i] - avg_genmet_py_);
    gx.push_back(gvar_x_);
    gy.push_back(gvar_y_);
    gxy.push_back(gvar_xy_);
    
    }
   float gvar_x =  accumulate( gx.begin(), gx.end(), 0.0)/gx.size(); 
   float gvar_y =  accumulate( gy.begin(), gy.end(), 0.0)/gy.size();
   float gvar_xy = accumulate( gxy.begin(), gxy.end(), 0.0)/gxy.size();
    vector<float> covmx;
   covmx.push_back(gvar_x);
   covmx.push_back(gvar_y);
   covmx.push_back(gvar_xy);
  return  covmx ;
}



void rootfile___( TString myMethodList = "" ){








TFile* input1 = new  TFile("test_5750.root");
TFile* F = new TFile("./sv/test_5750.root", "RECREATE");
TTree* tree1 = (TTree*)input1->Get("analysisTree");

Int_t kTr = 100;
Int_t kTr1 = tree1->GetEntries();
cout << kTr1 << endl;


  TBranch *b_tau1_vis_px;
  TBranch *b_tau1_vis_py;
  TBranch *b_tau1_vis_pz;
  TBranch *b_tau1_vis_e;
  TBranch *b_tau1_vis_pt;
  TBranch *b_tau1_vis_eta;
  TBranch *b_tau1_vis_phi;
  TBranch *b_tau1_vis_m;
  TBranch *b_tau2_vis_px;
  TBranch *b_tau2_vis_py;
  TBranch *b_tau2_vis_pz;
  TBranch *b_tau2_vis_e;
  TBranch *b_tau2_vis_pt;
  TBranch *b_tau2_vis_eta;
  TBranch *b_tau2_vis_phi;
  TBranch *b_tau2_vis_m;
  TBranch *b_met_px;
  TBranch *b_met_py;
  TBranch *b_met_phi;
  TBranch *b_met;
  TBranch *b_mT;
  TBranch *b_pTratio;
  TBranch *b_dtheta; 
  TBranch *b_covMet11;
  TBranch *b_covMet12;
  TBranch *b_covMet21;
  TBranch *b_covMet22; 
  TBranch *b_gentau1_vis_px;
  TBranch *b_gentau1_vis_py;
  TBranch *b_gentau1_vis_pz;
  TBranch *b_gentau1_vis_e;
  TBranch *b_gentau1_vis_pt;
  TBranch *b_gentau1_vis_eta;
  TBranch *b_gentau1_vis_phi;
  TBranch *b_gentau1_vis_m;
  TBranch *b_gentau2_vis_px;
  TBranch *b_gentau2_vis_py;
  TBranch *b_gentau2_vis_pz;
  TBranch *b_gentau2_vis_e;
  TBranch *b_gentau2_vis_pt;
  TBranch *b_gentau2_vis_eta;
  TBranch *b_gentau2_vis_phi;
  TBranch *b_gentau2_vis_m;
  TBranch *b_genmet_px;
  TBranch *b_genmet_py;
  TBranch *b_genmet_phi;
  TBranch *b_genmet;
  TBranch *b_gen_mT;
  TBranch *b_gen_pTratio;
  TBranch *b_gen_dtheta;
  TBranch *b_boson_mass;
  TBranch *b_boson_vis_mass;
  TBranch *b_gencovMet11;
  TBranch *b_gencovMet12;
  TBranch *b_gencovMet21;
  TBranch *b_gencovMet22;
  TBranch *b_event_weight;
  TBranch *b_class_id;



  Float_t tau1_vis_px[kTr];
  Float_t tau1_vis_py[kTr];
  Float_t tau1_vis_pz[kTr];
  Float_t tau1_vis_e[kTr];
  Float_t tau1_vis_pt[kTr];
  Float_t tau1_vis_eta[kTr];
  Float_t tau1_vis_phi[kTr];
  Float_t tau1_vis_m[kTr];
  Float_t tau2_vis_px[kTr];
  Float_t tau2_vis_py[kTr];
  Float_t tau2_vis_pz[kTr];
  Float_t tau2_vis_e[kTr];
  Float_t tau2_vis_pt[kTr];
  Float_t tau2_vis_eta[kTr];
  Float_t tau2_vis_phi[kTr];
  Float_t tau2_vis_m[kTr];
  Float_t met_px[kTr]; 
  Float_t met_py[kTr];
  Float_t met_phi[kTr];
  Float_t met[kTr];
  Float_t mT[kTr];
  Float_t pTratio[kTr];
  Float_t dtheta[kTr];
  Float_t covMet11[kTr];
  Float_t covMet12[kTr];
  Float_t covMet21[kTr];
  Float_t covMet22[kTr];
  Float_t gentau1_vis_px[kTr];
  Float_t gentau1_vis_py[kTr];
  Float_t gentau1_vis_pz[kTr];
  Float_t gentau1_vis_e[kTr];
  Float_t gentau1_vis_pt[kTr];
  Float_t gentau1_vis_eta[kTr];
  Float_t gentau1_vis_phi[kTr];
  Float_t gentau1_vis_m[kTr];
  Float_t gentau2_vis_px[kTr];
  Float_t gentau2_vis_py[kTr];
  Float_t gentau2_vis_pz[kTr];
  Float_t gentau2_vis_e[kTr];
  Float_t gentau2_vis_pt[kTr];
  Float_t gentau2_vis_eta[kTr];
  Float_t gentau2_vis_phi[kTr];
  Float_t gentau2_vis_m[kTr];
  Float_t genmet_px[kTr]; 
  Float_t genmet_py[kTr];
  Float_t genmet_phi[kTr];
  Float_t genmet[kTr];
  Float_t gen_mT[kTr];
  Float_t gen_pTratio[kTr];
  Float_t gen_dtheta[kTr];
  Float_t boson_mass[kTr];
  Float_t boson_vis_mass[kTr];
  Float_t gencovMet11[kTr];
  Float_t gencovMet12[kTr];
  Float_t gencovMet21[kTr];
  Float_t gencovMet22[kTr];
  Float_t event_weight[kTr];
  Float_t class_id[kTr];


  tree1->SetBranchAddress("gentau1_vis_px", gentau1_vis_px, &b_gentau1_vis_px);
  tree1->SetBranchAddress("gentau1_vis_py", gentau1_vis_py, &b_gentau1_vis_py);
  tree1->SetBranchAddress("gentau1_vis_pz", gentau1_vis_pz, &b_gentau1_vis_pz);
  tree1->SetBranchAddress("gentau1_vis_e", gentau1_vis_e, &b_gentau1_vis_e);
  tree1->SetBranchAddress("gentau1_vis_pt", gentau1_vis_pt, &b_gentau1_vis_pt);
  tree1->SetBranchAddress("gentau1_vis_eta", gentau1_vis_eta, &b_gentau1_vis_eta);
  tree1->SetBranchAddress("gentau1_vis_phi", gentau1_vis_phi, &b_gentau1_vis_phi);
  tree1->SetBranchAddress("gentau1_vis_m", gentau1_vis_m, &b_gentau1_vis_m);
  tree1->SetBranchAddress("gentau2_vis_px", gentau2_vis_px, &b_gentau2_vis_px);
  tree1->SetBranchAddress("gentau2_vis_py", gentau2_vis_py, &b_gentau2_vis_py);
  tree1->SetBranchAddress("gentau2_vis_pz", gentau2_vis_pz, &b_gentau2_vis_pz);
  tree1->SetBranchAddress("gentau2_vis_e", gentau2_vis_e, &b_gentau2_vis_e);
  tree1->SetBranchAddress("gentau2_vis_pt", gentau2_vis_pt, &b_gentau2_vis_pt);
  tree1->SetBranchAddress("gentau2_vis_eta", gentau2_vis_eta, &b_gentau2_vis_eta);
  tree1->SetBranchAddress("gentau2_vis_phi", gentau2_vis_phi, &b_gentau2_vis_phi);
  tree1->SetBranchAddress("gentau2_vis_m", gentau2_vis_m, &b_gentau2_vis_m);
  tree1->SetBranchAddress("genmet_px", genmet_px, &b_genmet_px);
  tree1->SetBranchAddress("genmet_py", genmet_py, &b_genmet_py);
  tree1->SetBranchAddress("genmet_phi", genmet_phi, &b_genmet_phi);
  tree1->SetBranchAddress("genmet", genmet, &b_genmet);
  tree1->SetBranchAddress("gen_mT", gen_mT, &b_gen_mT);
  tree1->SetBranchAddress("gen_pTratio", gen_pTratio, &b_gen_pTratio);
  tree1->SetBranchAddress("gen_dtheta", gen_dtheta, &b_gen_dtheta);
  tree1->SetBranchAddress("boson_mass", boson_mass, &b_boson_mass);
  tree1->SetBranchAddress("tau1_vis_px", tau1_vis_px, &b_tau1_vis_px);
  tree1->SetBranchAddress("tau1_vis_py", tau1_vis_py, &b_tau1_vis_py);
  tree1->SetBranchAddress("tau1_vis_pz", tau1_vis_pz, &b_tau1_vis_pz);
  tree1->SetBranchAddress("tau1_vis_e", tau1_vis_e, &b_tau1_vis_e);
  tree1->SetBranchAddress("tau1_vis_pt", tau1_vis_pt, &b_tau1_vis_pt);
  tree1->SetBranchAddress("tau1_vis_eta", tau1_vis_eta, &b_tau1_vis_eta);
  tree1->SetBranchAddress("tau1_vis_phi", tau1_vis_phi, &b_tau1_vis_phi);
  tree1->SetBranchAddress("tau1_vis_m", tau1_vis_m, &b_tau1_vis_m);
  tree1->SetBranchAddress("tau2_vis_px", tau2_vis_px, &b_tau2_vis_px);
  tree1->SetBranchAddress("tau2_vis_py", tau2_vis_py, &b_tau2_vis_py);
  tree1->SetBranchAddress("tau2_vis_pz", tau2_vis_pz, &b_tau2_vis_pz);
  tree1->SetBranchAddress("tau2_vis_e", tau2_vis_e, &b_tau2_vis_e);
  tree1->SetBranchAddress("tau2_vis_pt", tau2_vis_pt, &b_tau2_vis_pt);
  tree1->SetBranchAddress("tau2_vis_eta", tau2_vis_eta, &b_tau2_vis_eta);
  tree1->SetBranchAddress("tau2_vis_phi", tau2_vis_phi, &b_tau2_vis_phi);
  tree1->SetBranchAddress("tau2_vis_m", tau2_vis_m, &b_tau2_vis_m);
  tree1->SetBranchAddress("met_px", met_px, &b_met_px);
  tree1->SetBranchAddress("met_py", met_py, &b_met_py);
  tree1->SetBranchAddress("met_phi", met_phi, &b_met_phi);
  tree1->SetBranchAddress("met", met, &b_met);
  tree1->SetBranchAddress("event_weight", event_weight, &b_event_weight);
  tree1->SetBranchAddress("class_id", class_id, &b_class_id);






TTree *tree = new TTree("analysisTree", "analysisTree");
     
      tree->Branch("gentau1_vis_px",&gentau1_vis_px,"gentau1_vis_px/F");
      tree->Branch("gentau1_vis_py",&gentau1_vis_py,"gentau1_vis_py/F");
      tree->Branch("gentau1_vis_pz",&gentau1_vis_pz,"gentau1_vis_pz/F");
      tree->Branch("gentau1_vis_e",&gentau1_vis_e,"gentau1_vis_e/F");
      tree->Branch("gentau1_vis_m",&gentau1_vis_m,"gentau1_vis_m/F");
      tree->Branch("gentau1_vis_pt",&gentau1_vis_pt,"gentau1_vis_pt/F");
      tree->Branch("gentau1_vis_eta",&gentau1_vis_eta,"gentau1_vis_eta/F");
      tree->Branch("gentau1_vis_phi",&gentau1_vis_phi,"gentau1_vis_phi/F");

      tree->Branch("gentau2_vis_px",&gentau2_vis_px,"gentau2_vis_px/F");
      tree->Branch("gentau2_vis_py",&gentau2_vis_py,"gentau2_vis_py/F");
      tree->Branch("gentau2_vis_pz",&gentau2_vis_pz,"gentau2_vis_pz/F");
      tree->Branch("gentau2_vis_e",&gentau2_vis_e,"gentau2_vis_e/F");
      tree->Branch("gentau2_vis_m",&gentau2_vis_m,"gentau2_vis_m/F");
      tree->Branch("gentau2_vis_pt",&gentau2_vis_pt,"gentau2_vis_pt/F");
      tree->Branch("gentau2_vis_eta",&gentau2_vis_eta,"gentau2_vis_eta/F");
      tree->Branch("gentau2_vis_phi",&gentau2_vis_phi,"gentau2_vis_phi/F");

      tree->Branch("tau1_vis_px",&tau1_vis_px,"tau1_vis_px/F");
      tree->Branch("tau1_vis_py",&tau1_vis_py,"tau1_vis_py/F");
      tree->Branch("tau1_vis_pz",&tau1_vis_pz,"tau1_vis_pz/F");
      tree->Branch("tau1_vis_e",&tau1_vis_e,"tau1_vis_e/F");
      tree->Branch("tau1_vis_m",&tau1_vis_m,"tau1_vis_m/F");
      tree->Branch("tau1_vis_pt",&tau1_vis_pt,"tau1_vis_pt/F");
      tree->Branch("tau1_vis_eta",&tau1_vis_eta,"tau1_vis_eta/F");
      tree->Branch("tau1_vis_phi",&tau1_vis_phi,"tau1_vis_phi/F");
      
      tree->Branch("tau2_vis_px",&tau2_vis_px,"tau2_vis_px/F");
      tree->Branch("tau2_vis_py",&tau2_vis_py,"tau2_vis_py/F");
      tree->Branch("tau2_vis_pz",&tau2_vis_pz,"tau2_vis_pz/F");
      tree->Branch("tau2_vis_e",&tau2_vis_e,"tau2_vis_e/F");
      tree->Branch("tau2_vis_m",&tau2_vis_m,"tau2_vis_m/F");
      tree->Branch("tau2_vis_pt",&tau2_vis_pt,"tau2_vis_pt/F");
      tree->Branch("tau2_vis_eta",&tau2_vis_eta,"tau2_vis_eta/F");
      tree->Branch("tau2_vis_phi",&tau2_vis_phi,"tau2_vis_phi/F");
      
      tree->Branch("met_px",&met_px,"met_px/F");
      tree->Branch("met_py",&met_py,"met_py/F");
      tree->Branch("met_phi",&met_phi,"met_phi/F");
      tree->Branch("met",&met,"met/F");
      tree->Branch("genmet_px",&genmet_px,"genmet_px/F");
      tree->Branch("genmet_py",&genmet_py,"genmet_py/F");
      tree->Branch("genmet_phi",&genmet_phi,"genmet_phi/F");
      tree->Branch("genmet",&genmet,"genmet/F");
      tree->Branch("gen_mT",&gen_mT,"gen_mT/F");
      tree->Branch("gen_pTratio",&gen_pTratio,"gen_pTratio/F");
      tree->Branch("gen_dtheta",&gen_dtheta,"gen_dtheta/F");


      tree->Branch("boson_mass",&boson_mass,"boson_mass/F");
      tree->Branch("event_weight",&event_weight,"event_weight/F");
      tree->Branch("class_id",&class_id,"class_id/F");
      tree->Branch("covMet11",&covMet11,"covMet11/F");
      tree->Branch("covMet12",&covMet12,"covMet12/F");
      tree->Branch("covMet21",&covMet21,"covMet21/F");
      tree->Branch("covMet22",&covMet22,"covMet22/F");




vector < float > genmet_px_;
vector < float > genmet_py_;


for(Int_t i = 0; i < kTr1;i++){ tree1->GetEntry(i);

for(Int_t j = 0;j < 1; j++){ 

genmet_px_.push_back(genmet_px[j]);
genmet_py_.push_back(genmet_py[j]);

}}


vector < float >  c1 = covm(genmet_px_,genmet_py_);

cout <<"x : "<< c1[0] << endl;

cout <<"y : "<< c1[1] << endl;


cout <<"xy : " <<c1[2] << endl;


  int K=0;
  for(Int_t i = 0; i < kTr1;i++){ 
       tree1->GetEntry(i);
         for(Int_t j = 0;j < 1; j++){
 

 
           gentau1_vis_px[j]=gentau1_vis_px[j];
           gentau1_vis_py[j]=gentau1_vis_py[j];
           gentau1_vis_pz[j]=gentau1_vis_pz[j];
           gentau1_vis_e[j]=gentau1_vis_e[j];
           gentau1_vis_pt[j]=gentau1_vis_pt[j];
           gentau1_vis_eta[j]=gentau1_vis_eta[j];
           gentau1_vis_phi[j]=gentau1_vis_phi[j];
           gentau1_vis_m[j]=gentau1_vis_m[j];
           gentau2_vis_px[j]=gentau2_vis_px[j];
           gentau2_vis_py[j]=gentau2_vis_py[j];
           gentau2_vis_pz[j]=gentau2_vis_pz[j];
           gentau2_vis_e[j]=gentau2_vis_e[j];
           gentau2_vis_pt[j]=gentau2_vis_pt[j];
           gentau2_vis_eta[j]=gentau2_vis_eta[j];
           gentau2_vis_phi[j]=gentau2_vis_phi[j];
           gentau2_vis_m[j]=gentau2_vis_m[j];

           tau1_vis_px[j]=tau1_vis_px[j];
           tau1_vis_py[j]=tau1_vis_py[j];
           tau1_vis_pz[j]=tau1_vis_pz[j];
           tau1_vis_e[j]=tau1_vis_e[j];
           tau1_vis_pt[j]=tau1_vis_pt[j];
           tau1_vis_eta[j]=tau1_vis_eta[j];
           tau1_vis_phi[j]=tau1_vis_phi[j];
           tau1_vis_m[j]=tau1_vis_m[j];
           tau2_vis_px[j]=tau2_vis_px[j];
           tau2_vis_py[j]=tau2_vis_py[j];
           tau2_vis_pz[j]=tau2_vis_pz[j];
           tau2_vis_e[j]=tau2_vis_e[j];
           tau2_vis_pt[j]=tau2_vis_pt[j];
           tau2_vis_eta[j]=tau2_vis_eta[j];
           tau2_vis_phi[j]=tau2_vis_phi[j];
           tau2_vis_m[j]=tau2_vis_m[j];

           genmet_px[j]=genmet_px[j];
           genmet_py[j]=genmet_py[j];
           genmet_phi[j]=genmet_phi[j];
           genmet[j]=genmet[j];
           gen_mT[j]=gen_mT[j];
           gen_pTratio[j]=gen_pTratio[j];
           gen_dtheta[j]=gen_dtheta[j];
           met_px[j]=met_px[j];
           met_py[j]=met_py[j];
           met_phi[j]=met_phi[j];
           met[j]=met[j];
           event_weight[j] = event_weight[j];
           class_id[j] = class_id[j];
           covMet11[j]=c1[0];
           covMet12[j]=c1[2];
           covMet21[j]=c1[2];
           covMet22[j]=c1[1];

           boson_mass[j]=boson_mass[j];
//cout << K << endl;

//2298.6929 1758.5085
//2341.948 1785.6703

//-829764.25 -749562.0
//-1456113.8 -1386982.4
//-2378954.8 -2306832.0
//-3422345.5 -3346093.2
}tree->Fill();} 

tree->Write();
F->Close();

}
