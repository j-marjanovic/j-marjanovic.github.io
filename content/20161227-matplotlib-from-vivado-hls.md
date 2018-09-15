Title: Matplotlib from Vivado HLS
Date: 2016-12-27 22:00
Category: Misc
Tags: Xilinx, Vivado HLS, C++, Matplotlib
Status: Draft

Vivado HLS is a really convenient tool when when implementing Digital Signal
Processing algorithms in FPGA. The description of algorithm in C is much
closer to pseudo-code than a RTL state machine, which is responsible for
scheduling operations and keeping track of data in pipeline. This is
especially true when the algorithm is implemented in floating-point arithmetic
due to long pipelines to perform basic operations, such as addition and
multiplication.

Because of its usefulness in handling DSP algorithms an desirable feature
would be the possibility to draw plots directly from C++ code. Some examples
could be: plotting the frequency spectra of input and output signal from
filters, plotting the original and re-sampled signal for resampling filter
(each with different time step), plotting the input, internal signals and
output of a PID controller... Although the plots should not replace automated
test (e.g. by comparing the response to "golden" response), a visual
representation is really helpful during the development and debugging.

One way to obtain the plots from C++ code is to write the signals of interest
in a text file and then parse it with Python. Plots can then be plotted with
fantastic Matplotlib library. This approach gives the desired result, but
requires switching from Vivado HLS to some other IDE/shell and running the
Python script. When adding signals to plots the code must be changed in two
points, the code responsible for printing to file and the code responsible for
parsing the simulation output.

Because of this limitations I have started searching for other options. Not a
long time ago a curated list of C++ libraries was posted on Hacker News:
[Awesome C++](http://fffaraz.github.io/awesome-cpp/). Unfortunately as of
time of writing this blog post (December 2016) there were no appropriate
library on that list. Looking further I have managed to find [Matplotlib-cpp]()
which is a C++ wrapper for a Matplotlib Python library.

Simple example
--------------

To test 


