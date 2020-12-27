#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ROOT

# Create root file
myfile = ROOT.TFile('random_data.root', 'RECREATE')
# Define a ntuple with three variables x, y and signal inside of root file
ntuple = ROOT.TNtuple("ntuple", "ntuple", "x:y:signal")

# Generate 1500 'signal' events with gauss distribution center at 0.5 with 0.75 sigma
for i in range(1500):
    ntuple.Fill(ROOT.gRandom.Gaus(0.5, 0.75),  # x
                ROOT.gRandom.Gaus(0.5, 0.75),  # y
                1)  # signal code
# Generate 3000 'background' events with gauss distribution center at 2.45 with 0.75 sigma
for i in range(3000):    
    ntuple.Fill(ROOT.gRandom.Gaus(2.45, 0.75),  # x
                ROOT.gRandom.Gaus(2.45, 0.75),  # y
                0)  # background code
ntuple.Write() # Write the to file 
myfile.Write("",ROOT.TObject.kWriteDelete) # Close the file saving ntuple
# Messages to user !!
print(" Random data is generated with name : random_data.root")
print(" Leavingg, bye !!")