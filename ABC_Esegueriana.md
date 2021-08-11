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

> Carregando pacotes exigidos: abc.data  
> Carregando pacotes exigidos: nnet  
> Carregando pacotes exigidos: quantreg  
> Carregando pacotes exigidos: SparseM   