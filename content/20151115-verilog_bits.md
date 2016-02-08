Title: HDL data type for Python parser implementations
Date: 2015-11-15 22:00
Category: Projects
Tags: Python, Verilog, FPGA, HDL

Recently I had to implement a parser for the PCIe protocol. The data was
captured with Xilinx ChipScope and saved as TSV (tab-separated value) text file.
I wanted to implement a parser in Python, my favorite language for this kind of
tasks. I have stumbled to a problem when I needed an elegant way to represent
the vector of bits of arbitrary length. I have found several libraries but none
of them satisfied my needs, so I put together a small class, which mimics
SystemVerilog vectors.


<script src="https://gist.github.com/j-marjanovic/348499e6cae3622554a4.js"></script>


Let's have a look at other alternatives which were available but did not
completely suit my needs. I wanted a vector slicing syntax which is similar to
the one in SystemVerilog and it allows to catch the typos quickly.

bitstring
---------

From their site: [bitstring](https://pypi.python.org/pypi/bitstring/3.1.3) is a
pure Python module designed to help make the creation and analysis of binary
data as simple and natural as possible.

It quick test finds two things which I would did not like: taking slice wider
than vector length pads the resulting vector with zeros and the slice indexes
are inverted compared to more used [higher_limit:lower_limit] notation in HDLs.
The output of the slicing is a closed interval, which is the behavior I would
expect.


BitArray
---------

The first thing which comes in mind is that there is not an easy way to create a
bitarray and initialize it from int in a single step (using constructor). The
only way to initialize BitArray is to use binary-formated string. This requires
a call of bin() function and dropping first two characters if your data is
stored as an int. At this point one can already start thinking of implementing
it's own class. The slicing has the same behavior as bitstring, which I did not
like for the application I need.


A simple solution on Stack Overflow
-----------------------------------

There is a [similar solution](http://stackoverflow.com/a/150411/4059686) already
posted on Stack Overflow, however it lacks an equality operator.


MyHDL
-----

Since MyHDL is a way to write HDL with Python it comes as obvious choice to use
it in a simple Python parser. MyHDL has a *intbv* data type which is very
similar to vectors in Verilog and VHDL. However, there are some minor things
which discouraged me from using it in my parser.

Lets have a look at a modified version of the VerilogBits unit test:

	import unittest
	import myhdl

	class Testmyhdlintbv(unittest.TestCase):
	    def test_equality(self):
	        self.assertEqual(myhdl.intbv(0xAB), myhdl.intbv(0xAB))
	        self.assertEqual(myhdl.intbv(0xAB), myhdl.intbv(0x0AB))
	        self.assertNotEqual(myhdl.intbv(0xAB), myhdl.intbv(0xCD))

	    def test_slicing(self):
	        ab = myhdl.intbv(0xAB)
	        self.assertEqual(ab[7:4], myhdl.intbv(0xA))
	        self.assertEqual(ab[3:0], myhdl.intbv(0xB))

	    def test_unpack(self):
	        abcd = myhdl.intbv(0xABCD)
	        a, b, c, d = abcd[15:12], abcd[11:8], abcd[7:4], abcd[3:0]
	        self.assertEqual(a, myhdl.intbv(0xA))
	        self.assertEqual(b, myhdl.intbv(0xB))
	        self.assertEqual(c, myhdl.intbv(0xC))
	        self.assertEqual(d, myhdl.intbv(0xD))

	    def test_slice_up_vect(self):
	        with self.assertRaises(ValueError):
	            dummy = myhdl.intbv(0xAB)[0:7]

	    def test_invalid_slice(self):
	        with self.assertRaises(IndexError):
	            dummy = myhdl.intbv(0xAB)[9:0]


	if __name__ == '__main__':
	    unittest.main()


This results are 3 failing tests: test_invalid_slice, test_slicing, and
test_unpack. test_invalid_slice fails because taking a slice wider than a vector
width produces fills the missing bits with zero. This is similar to
SystemVerilog vector of bits, which is a 2-level data type (it can be only 0 or
1). I prefer more rigorous behavior when slicing vectors, since errors like that
can be quite hard to catch. The VerilogBits throws an exception when an invalid
slice is requested.

If the zero padding problem with MyHDL is something I could live with, the other
two failing test are much more discouraging for someone who sometimes dreams
(System)Verilog. The [bit slicing in
MyHDL](http://docs.myhdl.org/en/stable/manual/hwtypes.html#bit-slicing) is half-
open as is expected in Python and not a closed interval as expected from HDLs
(e.g.  to get the LSB one should write [8:0] instead of [7:0]). Again, this is
just a convention and the software world is using the half-open interval for
decades ([E.W.Dijkstra: Why numbering should start at
zero](https://www.cs.utexas.edu/users/EWD/ewd08xx/EWD831.PDF)). But if your
parser in Python is there to find bugs in your SystemVerilog code, it makes much
more sense to use the same notation in both languages.


SystemVerilog
-------------

The SystemVerilog provide all the necessary tools to effectively manipulate bits
(duh), but the Python with the generators, list comprehensions and dictionaries
(well, SystemVerilog does have associative array) is much more elegant language.
The ability to test commands on-the-fly in the interpreter is also much
welcomed.
