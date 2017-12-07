{
   // user-defined style for high-quality plots

   // histograms lines
   gStyle->SetHistFillColor(0) ;
   gStyle->SetHistFillStyle(0) ;

   gStyle->SetHistLineColor(1) ;
   gStyle->SetHistLineStyle(0) ;
   gStyle->SetHistLineWidth(1) ;

   // suppress titles, stats box ans fit box
   gStyle->SetOptTitle(0) ;
   //gStyle->SetOptFit(0) ;



   // axis settings
   gStyle->SetLabelFont(142, "xyz") ;
   gStyle->SetLabelSize(0.04, "xyz") ;

   gStyle->SetTitleFont(142, "xyz") ;
   gStyle->SetTitleOffset(1.2, "xyz") ;
   gStyle->SetTitleSize(0.05, "xyz") ;


   // stat box
   gStyle->SetOptStat(0) ;
   //gStyle->SetOptStat("emr") ;   // display Entries, Mean and RMS
   //gStyle->SetStatFont(142) ;
   //gStyle->SetStatFontSize(0.05) ;
   //gStyle->SetStatBorderSize(0) ;


   // test
   TH1F *h = new TH1F("h", "hTest", 100, -5, 5) ;
   h->FillRandom("gaus", 10000) ;
   h->Draw() ;
   h->GetXaxis()->SetTitle("x-axis") ;
   h->GetYaxis()->SetTitle("y-axis") ;

   gPad->Modified() ;
   gPad->Update() ;

}
