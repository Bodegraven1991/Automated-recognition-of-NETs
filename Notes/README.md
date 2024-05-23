This is a space to add your notes
[![Shipping files](https://github.com/neuefische/ds-artificial-neural-networks/actions/workflows/workflow-04.yml/badge.svg?branch=main&event=workflow_dispatch)](https://github.com/neuefische/ds-artificial-neural-networks/actions/workflows/workflow-04.yml)

# Artificial Neural Networks

In this repo we will have a look at artificial neural networks.

## Task

Please work in pairs through all the notebooks in this particular order:

### Day 1

Typical libraries are pytorch, TensorFlow & Keras. We will use TensorFlow & Keras in this course. The following notebooks will show you how to implement DNN for regression and classification problems. Additionally, you can find the notebooks for dealing with over- and underfitting. And you will find a notebook on how to save and load models.

1. [Regression with TensorFlow & Keras](day_1/01_Regression_TensorFlow_Keras.ipynb)
2. [Classification with TensorFlow & Keras](day_1/02_Classification_TensorFlow_Keras.ipynb)
3. [Over- and Underfitting](day_1/03_Overfit_Underfit.ipynb)
4. [Load Models](day_1/04_Load_saved_Models.ipynb) (optional)

### Day 2

On day 2 you have the possibility to implement a Neural Network for your second project.

5. [DNN Assignment](day_2/05_DNN_Assignment.ipynb)

### Bonus

No one is normally creating their own DNN from scratch in python. But it could be a useful exercise for some. In this exercise you will build your own deep neural network with some assistance. This should help you to get a better understanding what is going on when "training" a NN.
Therefore, you will even compute your own back-propagation algorithm. You start this if you finish early on one of the other days, else save it for later review if you are interested.

6. [DNN from scratch](bonus/00_DNN_from_scratch.ipynb) 

## Environment

We have to install hdf5:

```BASH
 brew install hdf5
 brew install graphviz
```
With the system setup like that, we can go and create our environment and install tensorflow on M1

```BASH
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements_M1.txt
```

For Unix users

```BASH
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```
For Windows users

For `PowerShell` CLI :

 ```PowerShell
 pyenv local 3.11.3
 python -m venv .venv
 .venv\Scripts\Activate.ps1
 pip install --upgrade pip
 pip install -r requirements.txt
 ```

 For `Git-Bash` CLI :
 ```
 pyenv local 3.11.3
 python -m venv .venv
 source .venv/Scripts/activate
 pip install --upgrade pip
 pip install -r requirements.txt
 ```
