Title: Comparison of Place&Route algorithms in Quartus 14.0 and Quartus 15.1
Date: 2016-02-08 21:00
Category: Projects
Tags: Altera, FPGA, HDL
Status: draft

It is actually along story before I got to write this blog post and although it
is not really important how I got here, I would like to share a bit of context.
I have started writing an implementation of MD5 hash function in Chisel, a
Scala-based Hardware Description Language. For quite some time I am getting
tired of SystemVerilog's "always_ff @(posedge clk) begin if reset q <= 0 ..."
and while the Vivado HLS gives great results I still wanted to see what is there
in the middle. I also dream of HLS language based on a functional programing
language, such as Haskell or Scala.

The MD5 function requires some padding of the input message, and I wanted to see
if I can process entire 512-bit chunk in a single clock cycle. I wrote a Python
script to generate some really huge priority encoder. Because of long
combinatorial chains required to implement such encoders, there could be some
problems meeting timing constraints.


Quartus 14.0
============

I had Quartus 14.0

quartus_14_dev_selection.png


The timin closure in Quartus 14.0 fails with clock frequency at 100 MHz. The
reported fmax is 70 and 75 MHz for slow, 85 degC and 0degC models, respectively.

quartus_14_timing_fail_at_100MHz.png

If we observe placement, we can see that logic is placed in a circular shape at
the center of the FPGA fabric. This would indicate that the placer tried to put
logic as close as possible together. The priority encoder uses 1336 (21%) of
LUTs and 2176 (35%) of registers, which is somehow understandable figure, since
we are writing and reading data over a single pin. We need one 512-bit register
to store input and one 512-bit register to store output of encoder.

quartus_14_placement_center.png

Quartus 15.1
============

Quartus 15.1 fails with even greater margin (reported fmax 68 and 73).


Design space exploration
=========================

Seed sweep
----------

quartus_14_dse_settings.png


### Quartus 15.1

➜  bin  ./quartus_dsew
Inconsistency detected by ld.so: dl-close.c: 764: _dl_close: Assertion `map->l_init_called' failed!
quartus_dsew: relocation error: /usr/lib/x86_64-linux-gnu/libssl.so: symbol EVP_aes_128_cbc_hmac_sha256, version OPENSSL_1.0.2 not defined in file libcrypto.so.1.0.0 with link time reference






