#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import ROOT

# Argument parser will let us the give input and output file
parser=argparse.ArgumentParser()
parser.add_argument("-i", "--input",  default="random_data.root", help="input file name")
parser.add_argument("-o", "--output", default="bdt_test.root",    help="output file name")
args=parser.parse_args()


ROOT.TMVA.Tools.Instance() # Get Existing TMVA from root
fout = ROOT.TFile(args.output,"RECREATE") # Define a output file which will covers all BDT info
# Open a BDT Factory which will give some informations to user progress about BDT
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([
                                		"!V",
                                		"!Silent",
                                		"Color",
                                		"DrawProgressBar",
                                		"Transformations=I;D;P;G,D",
                                		"AnalysisType=Classification"
                                	]))
# Add data to 'DataLoader' that will be used in BDT analysis 
dataloader = ROOT.TMVA.DataLoader("dataset")
dataloader.AddVariable("x","F")
dataloader.AddVariable("y","F") 

# Access the data file and ntuple inside of it  
FIn = ROOT.TFile.Open(args.input)
TIn= FIn.Get("ntuple")
# 'DataLoader' need to learn the which tree will be used in BDT analysis 
dataloader.AddSignalTree(TIn)
dataloader.AddBackgroundTree(TIn)
 
# In our case, we have only one ntuple but it has identifier for signal and background events.
# To give signal and background events to 'DataLoader', we can use cuts, separetely. 
sigCut = ROOT.TCut("signal > 0.5")
bgCut  = ROOT.TCut("signal <= 0.5")

#Give them to 'DataLoader' by specifiying some informations (Check the TMVA manuel)
dataloader.PrepareTrainingAndTestTree(sigCut,   # signal events
                                      bgCut,    # background events
                                      ":".join([
                                        			"nTrain_Signal=0",
                                        			"nTrain_Background=0",
                                        			"SplitMode=Random",
                                        			"NormMode=NumEvents",
                                        			"!V"
                                       		  	]))
#Give 'DataLoader' to Factory specifiying some informations (Check the TMVA manuel)
factory.BookMethod(dataloader, 
				   ROOT.TMVA.Types.kBDT, 
				   "BDT", 
				   ":".join([
                           		"!H",
                           		"!V",
                           		"NTrees=850",
                           		"MinNodeSize=2.5%",
                           		"MaxDepth=3",
                           		"BoostType=AdaBoost",
                           		"AdaBoostBeta=0.5",
                           		"UseBaggedBoost",
                           		"BaggedSampleFraction=0.5",
                           		"SeparationType=GiniIndex",
                           		"nCuts=20",
                            ]))	
#Factory will analyze them with respect to the definitions!!
factory.TrainAllMethods() #With the half of data, it will learn 
factory.TestAllMethods() #With the other half, it will test
factory.EvaluateAllMethods() # BDT Analysis !!!
fout.Close() # Output for user !!!

ROOT.TMVA.TMVAGui(args.output) # Gui for user to see what is happened in the analysis!!

input("Press any key to exit!")
