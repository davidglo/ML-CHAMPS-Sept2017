# Digit Classification 
## Using PCA and Logistic Regression

---?image=digitClassification/assets/classification.png&size=contain

---

## Data: 

* *Classes*: handwritten digits 1 - 10
* *Features*: integers 0 - 16 (BW intensity) - the pixels are the features. 
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

## Data splitting

* Split data up into *training* and *test* sets (60/40 split)
* Tune hyper-parameters of model on training set
* Test best estimator on test set
```python
>>> X_train, X_test, y_train, y_test = train_test_split(
>>>     X_digits,y_digits, test_size=0.4, random_state=0)
>>> print(X_train.shape, X_test.shape)
>>> print(y_train.shape, y_test.shape)
(1078, 64) (719, 64)
(1078,) (719,)
```
---
On training data: 

1. Scale features: $\mu(x_i) = 0, \sigma(x_i) = 1, i = 1 ... 64$
2. Dimensionality reduction with Principal Components Analysis ([PCA](https://en.wikipedia.org/wiki/Principal_component_analysis))
3. Fit [multinomial logisitic classifier](https://en.wikipedia.org/wiki/Multinomial_logistic_regression) with regularization $C \in (10^{-4}, 10^{4}) $
4. Use [cross-validation][1] to choose [regularization][2] and number of PCA components to retain based on accuracy
 
[1]: https://en.wikipedia.org/wiki/Cross-validation_(statistics)
[2]: https://en.wikipedia.org/wiki/Regularization_(mathematics)
---?image=digitClassification/assets/cv_results.png&size=contain

---

On test data, using optimal hyper-parameters:
```python
>>> test_score = estimator.score(X_test, y_test)
>>> print('Score on test data: {:4.2f}%'.format(test_score*100))
Score on test data: 95.69%
```


 







