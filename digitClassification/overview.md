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

$$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$$

1. Scale features 







