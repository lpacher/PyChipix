
{

   gStyle->SetCanvasPreferGL(0) ;

   gStyle->SetAxisColor(kWhite, "X") ;
   gStyle->SetAxisColor(kWhite, "Y") ;

   gStyle->SetLabelColor(kWhite, "X") ;
   gStyle->SetLabelColor(kWhite, "Y") ;

   gStyle->SetLabelSize(0.05, "X") ;
   gStyle->SetLabelSize(0.05, "Y") ;

   gStyle->SetTextColor(kWhite) ;

   gStyle->SetCanvasColor(kBlack) ;
   gStyle->SetPadColor(kBlack) ;

   gStyle->SetGridColor(kWhite) ; 
   gStyle->SetPadGridX(1) ;
   gStyle->SetPadGridY(1) ;
 
   gStyle->SetFrameFillColor(kBlack) ;
   gStyle->SetFrameLineColor(kWhite) ;

   gStyle->SetTextColor(kWhite) ;

   gStyle->SetHistFillStyle(1001) ;
   gStyle->SetHistFillColor(kRed) ;
   gStyle->SetHistLineColor(kRed) ;

   gStyle->SetOptStat(0) ;

   printf("Black-style set!\n") ;

}
