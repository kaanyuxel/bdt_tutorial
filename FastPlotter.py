#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import ROOT

# Argument parser will let us the give input file and cut options
parser=argparse.ArgumentParser()
parser.add_argument("-f","--file",help="input file")
parser.add_argument("-c","--signal_cut",default="1", help="cut")
args=parser.parse_args()

# Access the data file and ntuple inside of it  
FIn = ROOT.TFile.Open(args.file)
TIn= FIn.Get("ntuple")

# Create a empty 2D histogram to draw signal and background events
hist_1 = ROOT.TH2F("hist_1", "Signal and Background Distributions;X [m];Y [m]", 100, -3, 5, 100, -3, 5)
hist_2 = ROOT.TH2F("hist_2", "Signal and Background Distributions;X [m];Y [m]", 100, -3, 5, 100, -3, 5)


# Fill the signal events
TIn.Draw("y:x>>hist_1", "signal > 0.5 &&" + args.signal_cut, "same")
# Fill the background events
TIn.Draw("y:x>>hist_2", "signal <= 0.5 &&" + args.signal_cut, "same")

# create a new TCanvas
ROOT.TCanvas()
#Define marker style, color and size for signal, respectively. 
hist_1.SetMarkerStyle(8)
hist_1.SetMarkerColor(ROOT.kRed)
hist_1.SetMarkerSize(0.5)
hist_1.SetStats(0) # Close info box of plot
hist_1.Draw(); # Draw signal distribution to canvas
#Define marker style, color and size for signal, respectively. 
hist_2.SetMarkerStyle(8)
hist_2.SetMarkerColor(ROOT.kBlue)
hist_2.SetMarkerSize(0.5) 
hist_2.SetStats(0) # Close info box of plot
hist_2.Draw("same");  # Draw background distribution to canvas

# Legend box definition which helps us to know which is which
legend = ROOT.TLegend(0.1232092,0.7705263,0.3180516,0.8926316)
legend.AddEntry(hist_1, " Signal ", "p") #Introduce the signal histogram to legend as a point
legend.AddEntry(hist_2, " Background", "p") #Introduce the background histogram to legend as a point
legend.Draw("sames") #Draw to well defined legend to canvas

raw_input("Press any key to exit!")