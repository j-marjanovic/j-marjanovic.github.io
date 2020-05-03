Status: draft

Chisel is a Hardware Description Language based on Scala. It should provide a
more productive way to write RTL, by providing a language which is better suited
for the task than Verilog and VHDL. I personally see Verilog and VHDL as an
equivalent to assembly, new generation of HDLs (MyHDL, Chisel, ...) equivalent
to C and High Level Synthesis (HLS) equivalent to modern programming languages
(Python, Scala, Java, C++14, Haskell) where much of the underlying mechanisms
are hidden from the programmer. This, combined with good optimization (and the
programmer's understanding of the under-the-hood mechanisms) provides higher
productivity, better quality of result and easier exploration of the design
space.

The posts on this blog will describe my journey into the world of modern HDLs. I
am quite comfortable with SystemVerilog, and although I agree that the syntax
can be cumbersome it also provides fine grained control over code. On the other
side of the spectrum the experience with Vivado HLS is really great, it greatly
simplifies coding signal-processing algorithms, for example. How much easier is
to write an IIR filter in C than in Verilog! And how easier is to define an AXI
Stream port (`hls::stream& data_in`) and to check if there is data available (
`if (!data_in.isempty())`)! It is not completely without flaws, I remember that
there was quite significant difference between how the operations
(multiplication and accumulation) were grouped together with parenthesis.
Anyway, HLS has a bright future in the FPGA and ASIC world.

The presentation of Chisel at DAC2012 describes basic building blocks of the
language and demonstrates their use. There are several documents available on
GitHub: XXX, but none of them describes the implementation into more detail.
What I miss from Chisel is a support for tasks, which would simplify development
of testbenches. Quite often I use two tasks to verify the behavior of DUTs in
testbenches, one task is exercising the inputs and another one is collecting the
outputs. This is somehow simplified version of UVM methodology, which uses
independent agents with driver and monitor on each port of the DUT.

Let's have a closer look on how the simulation in Chisel is performed. There are
several ways to run the Chisel simulation, described
here[https://chisel.eecs.berkeley.edu/2.0.0/chisel-cs250-3.pdf] on slide 1.
The most simple one is the Scala based simulation. In this method the user must
create a testbenche by subclassing `Tester` class and use the `peek`, `poke`,
`step` and `expect` methods to control the testbench.

The following example will be used to have a look on how the code is simulated.
The `SquarePlus1` is a module which calculates a square of the input and adds 1
in a 2-stage pipeline. The `SquarePlus1Tester` is a testbench, which feeds a
value to the input and waits for the result.

	import Chisel._

	class SquarePlus1 extends Module {
	  val io = new Bundle {
	    val data_i = UInt(INPUT, 16)
	    val data_o = UInt(OUTPUT, 32)
	  }

	  val squared_reg = Reg(UInt(width = 32))
	  val output_reg = Reg(UInt(width = 32))

	  io.data_o := output_reg

	  squared_reg := io.data_i * io.data_i
	  output_reg  := squared_reg + UInt(1)
	}

	class SquarePlus1Tester (c: SquarePlus1) extends Tester(c) {
	  poke(c.io.data_i, 5)
	  step(1)
	  peek(c.io.data_o)
	  step(1)
	  peek(c.io.data_o)
	}

	object AdvTestExample extends App {

	    val argz: Array[String] = Array("--backend", "c", "--genHarness", "--compile", "--test", "--vcd")

	    chiselMainTest(argz, () => Module(new SquarePlus1())) { c => new SquarePlus1Tester(c) }
	}

Connected to the target VM, address: '127.0.0.1:40410', transport: 'socket'
hello
CPP elaborate
[info] [216.860] // COMPILING < (class AdvTestExample.SquarePlus1)>(0)
[info] [217.138] giving names
[info] [217.249] executing custom transforms
[info] [217.261] convert masked writes of inline mems
[info] [217.268] adding clocks and resets
[info] [217.301] inferring widths
[info] [217.384] checking widths
[info] [217.390] lowering complex nodes to primitives
[info] [217.391] removing type nodes
[info] [217.398] compiling 0 nodes
[info] [217.399] computing memory ports
[info] [217.412] resolving nodes to the components
[info] [217.498] creating clock domains
[info] [217.505] pruning unconnected IOs
[info] [217.525] checking for combinational loops
[info] [217.536] NO COMBINATIONAL LOOP FOUND
[info] [355.011] populating clock domains
CppBackend::elaborate: need 0, redundant 0 shadow registers
[info] [363.699] generating cpp files
CppBackend: createCppFile SquarePlus1.cpp
[info] [527.472] g++ -c -o ./SquarePlus1-emulator.o  -I../ -I/csrc/  ./SquarePlus1-emulator.cpp RET 0
[info] [529.561] g++ -c -o ./SquarePlus1.o  -I../ -I/csrc/  ./SquarePlus1.cpp RET 0
[info] [562.430] g++   -o ./SquarePlus1 ./SquarePlus1.o ./SquarePlus1-emulator.o RET 0
sim start on jan-ThinkPad-T510 at Tue May 10 22:48:16 2016
inChannelName: 00006025.in
outChannelName: 00006025.out
cmdChannelName: 00006025.cmd
SEED 1462912665947
STARTING ./SquarePlus1 
  POKE  <- NOT ALLOWED
STEP 1 -> 1
Can't find id for ''
  PEEK  <- -0x1
STEP 1 -> 2
Cannot find the object, 
Can't find id for ''
  PEEK  <- -0x1
RAN 2 CYCLES PASSED
Disconnected from the target VM, address: '127.0.0.1:40410', transport: 'socket'

Process finished with exit code 0
