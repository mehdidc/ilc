#define MAXN  1000
#include <iostream>
#include <vector>
// Execute with:
// .x TPlot.C("ECalReconstruction.root","Secondaries.root",0) 
// 0 - number of event
void TPlot(string ECalEventfile, string MCEventfile,int number){
	
	float m_e = 0.000510999;
	float m_p = 0.938272;
	float m_k = 0.4937;
	float m_pi = 0.13957;
	float m_mu = 0.105658;

	
	int _posx[MAXN];
	int _posy[MAXN];
	int _posz[MAXN];
	
	float _mass[MAXN];

	float _startX[MAXN];
	float _startY[MAXN];
	float _startZ[MAXN];

	float _endX[MAXN];
	float _endY[MAXN];
	float _endZ[MAXN];

	float energyDep[30];
	int nhits;
	int nMC;
	int nMCn;
	int _cluster = 0;
	int _tracks = 0;
	int _showerCount = 0;
	gStyle->SetCanvasPreferGL(kTRUE);
	TCanvas * c1 = new TCanvas("c1", "The 3d view",0,0,1000,500);
	TPad *boxPad  = new TPad("box", "box", 0.02, 0.02, 0.48, 0.92);
	TPad *box1Pad = new TPad("box1", "box1", 0.52, 0.02, 0.98, 0.92);
	boxPad->Draw();
	box1Pad->Draw();
	
	TH3I * h3_Energy= new TH3I("h3Energy","",30,0,30,  18,0,18, 18,0,18 );
	//TH1F * h3 = new TH1F("h3","",30,0,30  );
	TChain* T = new TChain("TestTree");
	TChain* T1 = new TChain("MCParticles");
	T->Add(ECalEventfile.c_str());
	T1->Add(MCEventfile.c_str());
	int mTotalNumberOfEvents = T->GetEntries();
	T1->SetBranchAddress("nMCparticles_corrected", &nMC);
	T1->SetBranchAddress("nMCparticles", &nMCn);
	T1->SetBranchAddress("startX", _startX);
	T1->SetBranchAddress("startY", _startY);
	T1->SetBranchAddress("startZ", _startZ);

	T1->SetBranchAddress("mass", _mass);

	T1->SetBranchAddress("endX", _endX);
	T1->SetBranchAddress("endY", _endY);
	T1->SetBranchAddress("endZ", _endZ);


	T->SetBranchAddress("nhits", &nhits);
	T->SetBranchAddress("posx", _posx);
	T->SetBranchAddress("posy", _posy);
	T->SetBranchAddress("posz", _posz);
	T->SetBranchAddress("energyDep", energyDep);
	T->SetBranchAddress("clusterTotal", &_cluster);
	T->SetBranchAddress("tracksCount", &_tracks);
	T->SetBranchAddress("showerCount", &_showerCount);
	cout << "mTotalNumberOfEvents: " << mTotalNumberOfEvents << '\n';
	T->GetEntry(number);
	
	T1->GetEntry(number);
	cout << "Total number of MC particles: " << nMC <<" (" << nMCn << ')'<< '\n'<< '\n';
	cout << "Total number of clusters: " << _cluster << '\n';
	cout << "Total number of tracks: " << _tracks << '\n';
	cout << "Total number of showers: " << _showerCount << '\n';
	cout << "Hits: " << nhits << '\n';	

	for (unsigned int i = 0; i < nhits; i += 1)
	{
	        h3_Energy->Fill(_posz[i],_posx[i],_posy[i], 1.0);
	        //cout << "_posz[i]: " << _posz[i] << " _posx[i]: " << _posx[i] <<  " _posy[i]: " << _posy[i] << '\n';
	        //printf(_posx[i]);
	}
	boxPad->cd();
	h3_Energy->Draw("glbox");
	box1Pad->cd();
	gROOT->Reset();
	view = TView::CreateView(1);
	view->SetRange(1300,-90,-90,1500,90,90);
	view->ShowAxis();
	float epsilon = 0.0001;
	for (int j = 0; j < nMC; j++) 
	{
		TPolyLine3D * pl3d1 = new TPolyLine3D();
		//cout << "Added line!" << '\n';
		pl3d1->SetLineWidth(3);
		if (_mass[j] > m_k - epsilon && _mass[j] <m_k+epsilon) 
		{
			pl3d1->SetLineColor(kRed);
		}
		if (_mass[j] > m_e - epsilon && _mass[j] <m_e+epsilon)
		{
		        pl3d1->SetLineColor(kBlue);
		}
		if (_mass[j] > m_p - epsilon && _mass[j] <m_p+epsilon)
		{
		        pl3d1->SetLineColor(kYellow);
		}
		if (_mass[j] > m_pi - epsilon && _mass[j] <m_pi+epsilon)
		{
		        pl3d1->SetLineColor(kGreen);
		}

		pl3d1->SetPoint(0,_startZ[j],_startX[j],_startY[j]);
		 //cout << "Start z: " << _startZ[j]<< '\n';
		pl3d1->SetPoint(1,_endZ[j],_endX[j],_endY[j]);
		 //cout << "End z: " << _endZ[j]<< '\n';
		pl3d1->Draw();
	}
	TPolyLine3D *axis = new TPolyLine3D(6);
	axis->SetPoint(0,1300,-90,-90);
	axis->SetPoint(1,1300,-90,90);
	axis->SetPoint(2,1300,90,90);
	axis->SetPoint(3,1500,90,90);
	axis->SetPoint(4,1500,-90,90);
	axis->SetPoint(5,1300,-90,90);
	axis->Draw();
	TPolyLine3D *axis2 = new TPolyLine3D(4);
	axis2->SetPoint(0,1300,90,-90);
	axis2->SetPoint(1,1500,90,-90);
	axis2->SetPoint(2,1500,-90,-90);
	axis2->SetPoint(3,1500,-90,90);
	axis2->Draw();
	TPolyLine3D *axis3 = new TPolyLine3D();
	axis3->SetPoint(0,1500,90,-90);
	axis3->SetPoint(1,1500,90,90);
	axis3->Draw();
}
