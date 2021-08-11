Script and outputs for ABC cross-validation and empirical data
prediction for the species *Euphorbia segueriana* (scripts for the
remaining species are similar).
================

From the manuscript Kirschner & Perez et al. “Congruent evolutionary
responses of European steppe biota to late Quaternary climate change:
insights from convolutional neural network-based demographic modeling.”

### Model selection
Load library and input files.
```{r}
# Load the ABC library.
library(abc)

# The list of the generating model for each simulation in the test set.
models<-scan("models.txt")

# The predictions made by the trained CNN for each simulation, which will be used as SuSt.
sust<-read.table("testSet_ModelPredictions.txt")

# The average value of CNN predictions for the empirical data.
emp<-read.table("Emp_ModelPredictions.txt")
emp<-apply(emp, 2, FUN = median)
```

Perform cross validation using the test set and different thresholds to select the value with the highest accuracy.
```{r}
cv.modsel <- cv4postpr(models, sust, nval=10, tol =c(.05,.01,.005,.002,.001), method="rejection")
summary(cv.modsel)
```

> Output:
> ```
> Confusion matrix based on 10 samples for each model.
> 
> $tol0.001
>    13 15  9
> 9   0  0 10
> 13 10  0  0
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
> ```

Perform rejection with the empirical data and the selected threshold.
```{r}
Rej.05<-postpr(emp, models, sust, tol = .05, method = "rejection")
summary(Rej.05)
```

> Output:
> ```
> summary(Rej.05)
> Call: 
> postpr(target = emp, index = models, sumstat = sust, tol = 0.05, method = "rejection")
> 
> Data:
>  postpr.out$values (1500 posterior samples)
> 
> Models a priori:
>  9, 13, 15
> 
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
> ```

### Now we will use the CNN predictions from the selected model to estimate parameters.

Load files and name parameters.
```{r}
# Parameters for the selected model.
parameters<-read.table("parameters3.txt")

# Name columns.
colnames(parameters)=c("Theta","T1","T2","T3","Ne","NeZ","NeZLGM","NeZPl","m12_LGM","m21_LGM","m12_Pl","m21_Pl")

# Transform parameter values, when necessary.
parameters$NeZ=parameters$NeZ*parameters$Ne
parameters$NeZLGM=parameters$NeZLGM*parameters$Ne
parameters$NeZPl=parameters$NeZPl*parameters$Ne
parameters=within(parameters,rm(Theta))

# The parameter predictions made by the trained CNN for simulations from the selcted model, which will be used as SuSt.
sust<-read.table("testSet_ParameterPredictions.txt")

# The average value of CNN predictions for the empirical data.
emp<-read.table("Esegueriana/Emp_ParametersPredictions.txt")
emp<-apply(emp, 2, FUN = median)
```

Perform cross validation using the test set and different thresholds to select the value with the highest accuracy.
```{r}
cv.parest <- cv4abc(parameters, sust, nval=10, tol =c(.05,.01,.005,.002,.001), method = "rejection")
summary(cv.parest)
```

> Output:
> ```
> Prediction error based on a cross-validation sample of 10
> 
>              T1        T2        T3        Ne       NeZ    NeZLGM     NeZPl   m12_LGM   m21_LGM    m12_Pl    m21_Pl
> 0.001 1.2480373 2.5487941 0.9503033 1.1513134 0.8268913 1.1955350 1.0839741 0.7810868 0.8698749 0.9455978 0.9629271
> 0.002 1.0783402 2.7780802 1.0639218 1.0047776 1.0487878 1.2421166 0.9791096 0.9327081 1.0196879 1.1034843 0.7881159
> 0.005 1.2833362 2.4784407 1.2807658 1.0465434 0.9855177 0.9282621 1.0509444 0.7016709 0.9663778 1.1414797 0.8770493
> 0.01  1.1328156 2.1323440 1.1702100 1.1398613 0.8570619 0.9682446 1.0811069 0.8747661 1.0007252 1.1457145 0.8504343
> 0.05  1.0124374 2.1642556 0.9717194 0.9447449 0.8697100 0.9983704 0.8934766 0.9420805 1.0864375 1.0111190 0.9339603
> ```


Perform rejection with the empirical data and the selected threshold.
```{r}
REJ.parest.001 <- abc(emp, parameters, sust, tol = .001,method = "rejection")
summary(REJ.parest.001)
```

> Output:
> ```
> Call: 
> abc(target = emp, param = parameters, sumstat = sust, tol = 0.001, 
>     method = "rejection")
> Data:
>  abc.out$unadj.values (10 posterior samples)
> 
>                        T1           T2           T3           Ne          NeZ       NeZLGM        NeZPl      m12_LGM      m21_LGM       m12_Pl       m21_Pl
> Min.:        2.776931e+05 1.483476e+04 3.151422e+03 6.022209e+04 4.771559e+04 9.824978e+05 4.489653e+04 1.326000e+00 1.580000e-01 4.210000e-02 1.855000e-01
> 2.5% Perc.:  3.183399e+05 1.564209e+04 3.177439e+03 7.237111e+04 5.362408e+04 1.649852e+06 4.820020e+04 1.329900e+00 2.595000e-01 1.642000e-01 2.178000e-01
> Median:      9.127072e+05 8.193527e+04 6.121522e+03 1.267838e+05 2.741118e+05 8.280722e+06 1.061566e+05 3.443400e+00 2.163800e+00 2.296900e+00 2.633200e+00
> Mean:        1.122354e+06 6.948541e+04 6.781768e+03 1.407405e+05 2.799396e+05 8.888713e+06 1.004108e+05 3.155500e+00 2.380200e+00 2.130900e+00 2.643600e+00
> Mode:        6.011737e+05 8.924212e+04 4.770534e+03 1.214761e+05 2.433353e+05 8.314041e+06 1.182793e+05 3.815900e+00 1.571700e+00 2.203100e+00 2.624600e+00
> 97.5% Perc.: 2.246361e+06 1.008304e+05 1.081817e+04 1.921998e+05 5.659620e+05 1.731233e+07 1.308582e+05 4.455600e+00 4.609300e+00 4.576500e+00 4.506200e+00
> Max.:        2.254835e+06 1.014015e+05 1.119312e+04 1.932194e+05 5.721649e+05 1.757552e+07 1.315341e+05 4.565500e+00 4.653100e+00 4.615400e+00 4.528800e+00
> ```
