# EcholocationDNN

This repository provides the data and codes for the work done in this link: *Insert Link here*. The project deals with echolocation using a convolution neural netwrok (CNN) based model. The goal is locate an object in a grid soley using the echo reflections captured from the object by the microphone. The details on the experimental design, data pre-processing, and results are discussed in the document linked above.

The idea is to train a supervised DNN model on sample set (x,y) where x is the spectrogram of the echo reflected signal and y is the ground truth location (i.e. (x_gt, y_gt)) of the object. The model is proposed for both single object detection and multi object (i.e 2 objects) detection problem. The ground truth location for two object case would be { (x_1_gt, y_1_gt), (x_2_gt, y_2_gt) }.

## Hardware:
  1) [ReSpeaker Core v2.0](https://wiki.seeedstudio.com/ReSpeaker_Core_v2.0/)
  2) [Intel Realsense D435](https://www.intelrealsense.com/depth-camera-d435/)
  3) [30-Sided Dice](https://tinyurl.com/30-sided-dice)
  4) Sub-Woofer

## Dependencies:
  1) Numpy >= 1.17.0
  2) OpenCV-Python >= 4.4.0.42
  3) PyTorch >= 1.5.1
  4) SciPy >= 1.5.0
  5) PyAudio >= 0.2.11
  6) pygame >= 2.0.1

## Data Collection Methodology:
Respeaker Core v2.0 is used to collect the audio samples and the Realsense camera to capture the ground truth location. The Respeaker is accessed via a client server HTTPS protocol. The speaker is pinged on the server at the time of recording and a compressed recording file is sent back to the client. The file is decompressed on the client end and saved as a .npy file. The Reaslsense casmera returns both RGD and depth images. For this experiment, we only consider the RGB output to get the ground truth location. The data collection module saves the recorded sample(.npy) and RGB output into folders Recording and Images respectively. Both server and data collection files are attached in the repository.
  
The data collection process can be broken down into following sequence of operations:
  1) Play a high bass sound on the sub-wwofer to move the dice randomly in the box
  2) Capture an image to get the present location of the dice
  3) Start Recording and the emit the sound (done concurrently using threading)
  4) ReSpeaker returns the recorded sample to the client
  5) Repeat 
    
## Files:
  1) Raw Audio and Image Samples
  2) Pre-Processed Samples (i.e X and Y matrices)
  3) Model 

The raw audio samples and ground truth images for both single and multi object problems are provided [here](). The pre-processed X and Y matrices can be found [here](https://drive.google.com/drive/folders/1tWZZ7TY5ViGDtpf1EldzXDdm7Hi6CRWQ?usp=sharing). 

The data pre-processing notebook takes the raw audio and image files as an input. The input files are expected to come from a directory with two sub folder named Recording and Images for audio and image files respectively. 

The raw audio samples is transformed into a spectrogram of size (129,6) and this is done for all 6 channels of the microphone resulting into an array of shape (6,129,6). The spectrogram time and frequency precision can be controlled using the *nperseg* (window size) argument. Spectrograms are created using the [signal processing](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html) module of SciPy package. 

The pre-processing on ground truth images is done specific to our experimental setup. [Corner Detection](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html) algorithms from OpenCV are used to slice the image and detect the ground truth location for our object. The slicing parameters in the pre-processing notebook are specific to our setup but the process can be adapted to other settings.

The CNN model is forumlated in PyTorch and trained on a NVIDIA Tesla K80 GPU. The model was trained using Adam with a constant learning rate of 0.001 with regularization acting as an hyperparamter. The model architecture and training procedure are discussed in the document linked above.


Contributors: Ved Patel (vedpatel97@gmail.com), Dr. Martin Takáč (mat614@lehigh.edu), and Dr. Joshua C. Agar (joshua.agar@lehigh.edu)
