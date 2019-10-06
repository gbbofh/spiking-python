# Spiking Python

## What it is
This is an implementation of the model described by Eugene Izhikevich in the
2003 paper 'Simple Model of Spiking Neurons'. It is implemented here in Python.


## Requirements

 * SciPy
 * NumPy
 * Matplotlib

SciPy and NumPy are required, as the libraries provide extremely fast support
for array/matrix calculations, and generating random numbers according to a wide
variety of distributions. After the switch was made from raw Python lists to
NumPy arrays, speed increased by ~99.8% for the 1,000 neuron model presented in
the original paper.

Matplotlib is used to facilitate plotting, as opposed to dumping the output for
plotting/analysis by another program -- however in the future this will likely
be added as an option when I get around to adding command-line arguments.

## To Do

Currently I am adding support for live-updating graphs through the use of
matplotlib.animation. After the initial prototype is complete, the code will be
refactored into a more reasonable and extensible format that will allow for
extensibility/maintainability before it is merged into the master branch.
Ideally, a command-line flag will be added that will toggle the live-updating
functionality.

