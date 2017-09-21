# Digit Classification 
## Using PCA and Logistic Regression

---?image=digitClassification/assets/classification.png&size=contain

---

## Data: 

* *Classes*: handwritten digits 1 - 10
* *Features*: integers 0 - 16 (BW intensity)
* *Dimensionality*: 64 (8 x 8 pixels)
* ~180 examples per class
* Total samples: 1797

```python
>>> from sklearn.datasets import load_digits
>>> digits = load_digits()
>>> print(digits.data.shape)
(1797, 64)
```

---

## Pipeline part 1
1. Scale features so $\mu(X) = 0, \sigma(X) = 1$
2. Dimensionality reduction with Principal Components Analysis (PCA)
```python
>>> X.shape
(1797,64)
## Do PCA - retain 20 components
>>> X_pca.shape
(1797, 20)
``` 
---
## Pipeline part 2

3. Estimate regression coefficients in multinomial logisitic classifier with regularization $C = ...$
4. Use cross-validation to choose regularization and number of PCA components to retain based on accuracy
  







