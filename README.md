# EcholocationDNN

This repository provides the data and codes for the work done in this link: *Insert Link here*. The project deals with echolocation using a convolution neural netwrok (CNN) based model. The goal is locate an object in a grid soley using the echo reflections captured from the object by the microphone. The details on the experimental design, data pre-processing, and results are discussed in the document linked above.

The idea is to train a supervised DNN model on sample set (x,y) where x is the spectrogram of the echo reflected signal and y is the ground truth location (i.e. (xgt,ygt)) of the object. 

Hardware:
  1) ReSpeaker Core v2.0
  2) Intel Realsense D435
  3) Sub-Woofer
  4) 30-Sided Dice
  5) Bounding Box

The repository contains the following:
  1) Raw Audio and Image Samples
  2) Pre-Processed Samples (i.e X and Y matrices)
  3) Model 

Contributors: Ved Patel (vedpatel97@gmail.com), Dr. Martin Takáč (mat614@lehigh.edu), and Dr. Joshua C. Agar (joshua.agar@lehigh.edu)
