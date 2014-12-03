
#define MAXN  1000
#include <iostream>
#include <vector>
// Execute with:
// .x TPlot.C("ECalReconstruction.root","Secondaries.root",0) 
// 0 - number of event
void to_csv(string ECalEventfile, string MCEventfile){
	
	int _posx[MAXN];
	int _posy[MAXN];
	int _posz[MAXN];
	
	float _mass[MAXN];

	float _startX[MAXN];
	float _startY[MAXN];
	float _startZ[MAXN];
        float _energy[MAXN];

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
	
	TChain* T = new TChain("TestTree");
	TChain* T1 = new TChain("MCParticles");
	T->Add(ECalEventfile.c_str());
	T1->Add(MCEventfile.c_str());
        T->SetBranchAddress("energy", _energy);
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

	int number = 1;
	cout << "mTotalNumberOfEvents: " << mTotalNumberOfEvents << '\n';
	T->GetEntry(number);
	T1->GetEntry(number);
	cout << "Total number of MC particles: " << nMC <<" (" << nMCn << ')'<< '\n'<< '\n';
	cout << "Total number of clusters: " << _cluster << '\n';
	cout << "Total number of tracks: " << _tracks << '\n';
	cout << "Total number of showers: " << _showerCount << '\n';
	cout << "Hits: " << nhits << '\n';	


       cout << "tracks:"<<_tracks << " shower:" << _showerCount<<'\n';

	for (unsigned int i = 0; i < nMCn; i += 1)
	{
	       cout << _startX[i] << " " << _startY[i] << " " << _startZ[i] << " " << _mass[i] << '\n';
	}
	for (unsigned int i = 0; i < nhits; i += 1)
	{
	//        h3_Energy->Fill(_posz[i],_posx[i],_posy[i], 1.0);
	        cout << _posz[i] << " " << _posx[i] <<  " " << _posy[i] << " " << _energy[i] << '\n';
	        //printf(_posx[i]);
	}
}
