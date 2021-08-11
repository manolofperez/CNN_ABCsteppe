Script and outputs for ABC cross-validation and empirical data
prediction for the species *Euphorbia segueriana* (scripts for the
remaining species are similar).
================

From the manuscript Kirschner & Perez et al. “Congruent evolutionary
responses of European steppe biota to late Quaternary climate change:
insights from convolutional neural network-based demographic modeling.”

### Load library and input files for model selection.
```{r}
# Load the ABC library.
library(abc)

# The list of the generating model for each simulation in the test set.
models<-scan("Esegueriana/models.txt")

# The predictions made by the trained CNN for each simulation, which will be used as SuSt.
sust<-read.table("Esegueriana/testSet_ModelPredictions.txt")

# The average value of CNN predictions fos the empirical data.
emp<-read.table("Esegueriana/Emp_ModelPredictions.txt")
emp<-apply(emp, 2, FUN = median)
```


### Perform cross validation using the test set and different thresholds 
to select the value with the highest accuracy.
```{r}
cv.modsel <- cv4postpr(models, sust, nval=10, tol =c(.05,.01,.005,.002,.001), method="rejection")
summary(cv.modsel)
```

> Confusion matrix based on 10 samples for each model.
> 
> $tol0.001
>    13 15  9
> 9   0  0 10
> 13 10  0  0h
> 15  0 10  0
> 
> $tol0.002
>    13 15  9
> 9   0  0 10
> 13 10  0  0
> 15  0 10  0
> 
> $tol0.005
>    13 15  9
> 9   0  0 10
> 13 10  0  0
> 15  0 10  0
> 
> $tol0.01
>    13 15  9
> 9   0  0 10
> 13 10  0  0
> 15  0 10  0
> 
> $tol0.05
>    13 15  9
> 9   0  0 10
> 13 10  0  0
> 15  0 10  0
> 
> 
> Mean model posterior probabilities (rejection)
> 
> $tol0.001
>         9     13     15
> 9  1.0000 0.0000 0.0000
> 13 0.0000 0.9733 0.0267
> 15 0.0033 0.0167 0.9800
> 
> $tol0.002
>         9     13     15
> 9  1.0000 0.0000 0.0000
> 13 0.0017 0.9783 0.0200
> 15 0.0033 0.0200 0.9767
> 
> $tol0.005
>         9     13     15
> 9  0.9993 0.0000 0.0007
> 13 0.0020 0.9787 0.0193
> 15 0.0027 0.0173 0.9800
> 
> $tol0.01
>         9     13     15
> 9  0.9997 0.0000 0.0003
> 13 0.0013 0.9813 0.0173
> 15 0.0017 0.0170 0.9813
> 
> $tol0.05
>         9     13     15
> 9  0.9998 0.0000 0.0002
> 13 0.0008 0.9927 0.0065
> 15 0.0005 0.0088 0.9907


### Perform rejection with the empirical data and the selected threshold.
```{r}
Rej.05<-postpr(emp, models, sust, tol = .05, method = "rejection")
summary(Rej.05)
```

> summary(NN.1)
> Call: 
> postpr(target = emp, index = models, sumstat = sust, tol = 0.05, 
>     method = "rejection")
> Data:
>  postpr.out$values (1500 posterior samples)
> Models a priori:
>  9, 13, 15
> Models a posteriori:
>  9, 13, 15
> 
> Proportion of accepted simulations (rejection):
>  9 13 15 
>  0  0  1 
> 
> Bayes factors:
>      9  13  15
> 9            0
> 13           0
> 15 Inf Inf   1

### Now we will use the CNN predictions from the selected model to estimate parameters.

Load files and name parameters correctly.
```{r}
parameters<-read.table("Esegueriana/parameters15.txt")
colnames(parameters)=c("Theta","T1","T2","T3","Ne","NeZ","NeZLGM","NeZPl","m12_LGM","m21_LGM","m12_Pl","m21_Pl")
parameters$NeZ=parameters$NeZ*parameters$Ne
parameters$NeZLGM=parameters$NeZLGM*parameters$Ne
parameters$NeZPl=parameters$NeZPl*parameters$Ne
parameters=within(parameters,rm(Theta))

sust<-read.table("Esegueriana/testSet_ParameterPredictions.txt")
emp<-read.table("Esegueriana/Emp_ParametersPredictions.txt")
emp<-apply(emp, 2, FUN = median)

cv.parest <- cv4abc(parameters, sust, nval=10, tol =c(.05,.01,.005,.002,.001), method = "rejection")

REJ.parest.001 <- abc(emp, parameters, sust, tol = .001,method = "rejection")

summary(cv.parest)

summary(REJ.parest.001)
```
