# CNN_ABCsteppe

scripts from Kirschner et al. "Congruent evolutionary responses of European steppe biota to late Quaternary climate change: insights from convolutional neural network based demographic modeling" (https://www.researchsquare.com/article/rs-534143/latest ), to simulate and compare genetic datasets from five steppe species under three different demographic models. Data under the selected model for each species was also used to perform parameter estimation. Both model comparison and parameter estimation were achieved by training a CNN, form which prediction were then used as Summary Statistics (SuSt) for ABC.

simulate_Esegueriana.py - python script to simulate segregating sites and save them as NumPy arrays for *Euphorbia segueriana*. Simulations for the other species use a similar script, modified to reflect differences in the sample sizes and priors.

TrainCNN_Models_Esegueriana.ipynb - python notebook containing code and outputs for training and calibrating a CNN for model selection, perform cross-validation and predict the most likely model from empirical data in the species *E. segueriana* (scripts for the remaining species are similar).

TrainCNN_Parameters_Esegueriana.ipynb - python notebook containing code and outputs for training a CNN to peform parameter estimation in the species *Euphorbia segueriana* (scripts for the remaining species are similar).

ABC_Esegueriana.md - Code and outputs for ABC cross-validation and empirical data prediction for model selection and parameter estimation in the species *Euphorbia segueriana* (scripts for the remaining species are similar).

EmpiricalData - Folder containing the empirical data from the five steppe species analyzed.
