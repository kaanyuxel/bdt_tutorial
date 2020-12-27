#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import ROOT
import array
import numpy

# Argument parser will let us the give input file
parser=argparse.ArgumentParser()
parser.add_argument("-i", "--input",  default="random_data.root", help="input file name")
args=parser.parse_args()


# Setup TMVA
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()
reader = ROOT.TMVA.Reader("Color:!Silent")
discriminatingvariables = ['x','y'] 
TreeName = 'ntuple'
vars = [] 
n=0
for var in discriminatingvariables:
    exec('var'+str(n)+' = array.array(\'f\',[0])')
    exec('reader.AddVariable("'+var+'",var'+str(n)+')')
    exec('vars.append(var'+str(n)+')')
    n += 1
 
reader.BookMVA("BDT", ROOT.TString('dataset/weights/TMVAClassification_BDT.weights.xml'))
FIn = ROOT.TFile.Open(args.input,"")
TIn= FIn.Get(TreeName)
MVAOutput = numpy.zeros(1, dtype=float) 
FOut = ROOT.TFile.Open(args.input.replace('.root','_updated.root'),"RECREATE")
TOut = TIn.CopyTree('0')
TOut.Branch('BDT_Classifier', MVAOutput,'BDT_Classifier/D') 
N = TIn.GetEntries()

for n in range(N):
    if n%500 == 1:
        print args.input+":   "+str(n) +' of '+str(N) +' events evaluated.'
    
    TIn.GetEntry(n)
    
    a = 0
    for var in discriminatingvariables:
        exec('var'+str(a)+'[0] = TOut.'+var)
        a += 1
    
    MVAOutput[0] = reader.EvaluateMVA('BDT')
    TOut.Fill(MVAOutput[0])
     
FOut.Write()
FOut.Close()