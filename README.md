# CHAMPS Machine Learning - Sept2017

Welcome to the Sept 2017 CHAMPS machine learning workshop, which has been co-created by Rob Arbon, Silvia Amabilino, Lars Bratholm, Mike O'Connor, and David Glowacki

This workshop is designed to help you gain familiarity with some of the machine learning learning tools available in Python, so that you can think about applying these tools to your own workflows.

## Timetable
* 10.00am - 10.30am Welcome Session, with coffee, tea, and biscuits!

* 10.30am - 12.30pm Morning Session
    * David Glowacki: a brief introduction to machine learning and the data science pipeline
    * Silvia Amabilino: [Neural networks to fit potential energy functions](https://github.com/davidglo/ML-CHAMPS-Sept2017/tree/master/pes)
      * Neural Networks
      * Regularisation
      * the Python data science pipeline 
      * Hyperparameter Optimization

* 12.30pm - 2.00pm Lunch (provided)

* 2.00pm – 5.00pm Afternoon Session: Time to explore some simple machine learning application examples
    * Rob Arbon: [Logistic regression for handwritten digits classification](https://gitpitch.com/davidglo/ML-CHAMPS-Sept2017#)
      * Python tricks for data normalization
      * dimensionality reduction using principle component analysis
      * visualization using Pandas
    * Lars Bratholm & Mike O’Connor: [Training a neural net to learn body coordinates in virtual reality](https://github.com/davidglo/ML-CHAMPS-Sept2017/tree/master/vr/)

This course is formulated as a set of Jupyter scripts that you can download onto your own machine and work through at your own pace. We will be around to answer questions.

It assumes that you have a working version of python3, preferably installed using [Anaconda](https://www.continuum.io/downloads)

## Short instructions on how to run jupyter notebooks

If you have installed Anaconda, you should already have jupyter notebooks (as explained [here](http://jupyter.readthedocs.io/en/latest/install.html)).

First, you should download a *.zip file of the entire git repo. you can do this by going to the [link](https://github.com/davidglo/ML-CHAMPS-Sept2017/tree/master/pes), clicking the green "Clone or Download button", and then choosing the "Download ZIP" option. You can put the *.zip file anywhere that you want on your computer.

To run notebooks, navigate to the directory that contains the notebook which you want to run (files with extension `.ipynb`). Then type the following command:

`jupyter notebook`

This will open a browser window where you can see all the files contained in the directory from which you typed the `jupyter notebook` command. Click on the notebook that you want to open. This will open it in a new tab. 

To run a cell in the notebook press `shift + enter`.

## Some useful Links

[Tensorflow playground lets you construct your own neural network for simple classification tasks](http://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.41885&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false)

[Kaggle - Data Science Competitions](https://www.kaggle.com/competitions)

[A neural algorithm of artistic style](https://arxiv.org/abs/1508.06576)

[Elements of statistical learning](https://web.stanford.edu/~hastie/ElemStatLearn/)

