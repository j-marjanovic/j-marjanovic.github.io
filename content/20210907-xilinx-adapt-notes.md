Title: Notes from Xilinx® Adapt 2021
Date: 2021-09-07 21:00

[Xilinx Adapt 2021](https://xilinx.cventevents.com/event/f7c4412f-572a-4b8b-b8d0-6b92aae2cf0d)

# Day 1 (2021-09-07)

## Adaptive Computing: Innovation Accelerated [Ivo Bolsens (Xilinx)]

* the hardware is adapted, rather the other way around
* DSA
* growing gap between the moore's law and AI requirements
* requirements: 6G (100 Gbps, 0.1 ms latency)
* *Xilinx wants to be a platform company*
* Vivado/FPGA -> Vitis/MPSoC -> Vitis-AI/ACAP (Peer Processor)
* "hardware developers are still the key audience for Xilinx"
* Cloud and Edge
* some examples: SmartSSD (partnership with Samsung), SmartNIC
* guest speaker: Alveo U250 in Azure
    * Quantum optimization (10x gains a CPU)
    * Synapse - SQL acceleration (e.g. CSV parsing)
    * external use cases: Financial Services, Bio-Informatics
* AI engine (Scalar ALU, Vector ALU)
* AIE Array (non-blocking interconnect, local memory, ISA-based Vector Engine)
* guest speaker: Samsung
* Bfloat, INT4
* guest speaker: HPC at Pacific Northwest National Lab
    * computational chemistry application
    * outlook: integration between physical science and data science
    * heterogenous testbed: AMD Epyc, AMD Instinct GPU, Alveo
* Xilinx devices can handle the entire applications (e.g. ADAS)
* Kria SOM (most page views ever), comes with predefined bitstreams
* "accessible to software developers, domain experts"


## The Future of Adaptive Computing [Ivo Bolsens, Vamsi Boppana (Xilinx)]

* higher level -> IP Integrator, software
* 2021.1 -> Machine Learning in Vivado
    * "Inteligent Design runs"
    * delay estimation, resource usage predictions
* AI Engines also for liner algebra applications (not only Machine Learning)
* 512-bit-wide vector machine
* chiplets (e.g. larger devices)
* rapidly evolving standards -> adaptable hardware
* DFX (e.g. in automotive, two different algorithms)
* Vitis AI: CNN, RNN, LSTM
* Hennessy & Patterson - Domain Specific Architecture
* open-source (community, de-facto standards)
* Xilinx App Store, Ubuntu software store
* Kria (ready-built application, downloadable from an on-line app store)
* roadmap (up to 1 nm), only for a selected products (cost-sensitive apps)


## Design Rationale of Two Generations of AI Engines [Kees Vissers (Xilinx)]

* again Hennessey and Patterson
* processor designed from a ground up
* comparison between **traditional multi-core** and **AI Engine Array**
* interconnect + DMA (no caches)
* better latency, efficiency than GPU and CPU
* 1GHz+, 400 AI Engines per device
* AI Engine = conventional AI processor
    * VLIW
    * 32-bit RISC
    * 512-bit SIMD (fixed point, floating point)
    * Fixed-Point Vector Unit (similar to DSP48)
    * FPMPY
    * Multi-precision support (also Complex - for RF)
    * memory:
        * double buffering
        * dataflow
        * streaming communication (DMA between memories)
        * multicast support
    * integration into PL: AXI-Stream
* Vitis libraries (vision, finance, linear algebra, ...)
* XAPP1351 (multi-rate filter), XAPP1352 (beamforming), XAPP1356 (FFT)
* Vitis AI (PyTorch/TensorFlow/Caffe to FPGA/AI engines)
* second gen AI Engine
    * use case: ADAS, robotics, media
    * in **Versal AI Edge**
    * bfloat16
    * matrix * matrix multiply [(A0 x B0) + (A1 x B1) + ... ]
    * data multicast (e.g. weights for NN)
    * PCIe gen 5
* high level AIE API (independent of underlying AIE)


---

<div style="font-size: 80%;" >
Xilinx, Inc. Xilinx, the Xilinx logo, Alveo, Vivado, Vitis, Versal, Zynq are trademarks of Xilinx in the United States and
other countries.
</div>

<div style="font-size: 80%;" >
All trademarks and registered trademarks are the property of their respective owners.
</div>
