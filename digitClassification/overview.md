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

## Pipeline 
1. Scale features so $\mu(X) = 0, \sigma(X) = 1$
2. Dimensionality reduction with Principal Components Analysis (PCA)
3. Estimate regression coefficients in multinomial logisitic classifier with regularization $C \in (10^{-4}, 10^{4}) $
4. Use cross-validation to choose regularization and number of PCA components to retain based on accuracy
 
---?image=digitClassification/assets/cv_results.png&size=contain



 







