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


# Day 2

## What's New in Vitis AI 1.4 and Vitis 2021.1 [George Wang (Xilinx)]

### Vitis

* DPU
* libraries for AI engines: FIR, FFT, GEMM, vision
* GZIP, ZSTD library
* FIFO allocation with AI Engine
* x86 simulator for AIE
* Device Tree generator -> ZOCL node
* Vitis HLS: Flow Navigator

### Vitis AI 1.4

* support for 2 Versals and Kria
* 108 AI models in total in AI Model Zoo
* lidar, radar applications
* quantization-aware training, automatic network pruning

## Introduction to Kria System on Module [Karan Kantharia (Xilinx)]

* Xilinx idea: use SoM in final products
* vision market (becoming more fragmented): security camera, obj classifications, medial, AR/VR, emotion

### KRIA K26 SOM

* Zynq (ARM + FPGA)
* several interfaces: LVDS, USB, MIPI, Ethernet, HDMI, DisplayPort, ...
* Xilinx idea: no more RTL/HW design -> up to 9 months faster Time to Market
* "no FPGA experience required"
* three options:
    * for AI Developer: use AI model
    * for SW devloper: use Vitis
    * for HW developer: use Vivado ML
* Yocto and Ubuntu supported
* FCC, ... certified

## Workshop: Vitis AI 101: End-to-End Model Deployment with Vitis AI [Fan Zhang (Xilinx)]

https://github.com/fanz-xlnx/Adapt_Workshop_VAI101

```
ubuntu@ip-***:~$ lspci
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
00:01.0 ISA bridge: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II]
00:01.1 IDE interface: Intel Corporation 82371SB PIIX3 IDE [Natoma/Triton II]
00:01.3 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 01)
00:02.0 VGA compatible controller: Cirrus Logic GD 5446
00:03.0 Ethernet controller: Amazon.com, Inc. Elastic Network Adapter (ENA)
00:1e.0 3D controller: NVIDIA Corporation GK210GL [Tesla K80] (rev a1)
00:1f.0 Unassigned class [ff80]: XenSource, Inc. Xen Platform Device (rev 01)
```

```
ubuntu@ip-***:~$ nvidia-smi
Wed Sep  8 17:20:50 2021
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.57.02    Driver Version: 470.57.02    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla K80           On   | 00000000:00:1E.0 Off |                    0 |
| N/A   55C    P0   121W / 149W |   4188MiB / 11441MiB |     94%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A     19274      C   python                           4185MiB |
+-----------------------------------------------------------------------------+
```

* *IoU* = Intersection over Union = Area of Overlap / Area of Union
* XIR format
* KV260 (KRIA)

```
xcompiler -t DPUCZDX8G_ISA0_B4096_MAX_BG2 -i quantize_result/ENet_int.xmodel -o compilation_results/KV260/ENet_cityscapes_pt/ENet_cityscapes_pt.xmodel
```

```
The compiled xmodel's md5sum is 4bf46f368e9ff2d51fea136a19270c75
```

# Day 3

## Expert Panel: Tips and Tricks

* improvements in silicon
    * "PL is what Xilinx is famous for"
    * "end of Moore's law, end of Amdahl's law, end of Dennard scaling" --> more hardened IP (more like ASIC), e.g. DSP58
* getting started guide for DFX ([xilinx.com/vivado/dfx])
* HDL (VHDL support)
    * simulation: working on the support for the VHDL-2008 (*it is 2021*), based on feature requests
    * simulation: "current focus on SystemVerilog"
    * synthesis: "at the advanced level"
* open-source tools (providing the bitstream information)
    * "secret sauce"
    * "hacking protection"
    * open-source front-end for Vivado and Vitis
    * "leave bitstream generation to experts"
* ML in Vivado
* congestion when 70% CLBs utilized
* revision control
* RTL workflow
    * a couple of features require IPI (e.g. CIPS, NoC)
* porting software to AI Engines
    * start from the C models
* RapidWright
* QEMU

## Team-Based Collaborative Features in IP Integrator

* UG994
* Block Design Container
    * top-down workflow:
        1. create hierarchy
        2. validate
        3. *was distracted*
    * e.g. debug vs no-debug version
    * DFX flow
    * Inter-NOC input

## Vitis HLS for High-Performance Kernels

* v++
* optimizations
    * pipeline (`II`)
    * SIMD
    * dataflow (task parallelism, handshaking)
* data types:
    * arrays: AXI4 Memory Mapped
    * scalar: AXI4-Lite
    * stream: AXI4-Stream

```c
#pragma HLS UNROLL factor=N
```

```c
__attribute__((vector_size(64)))
```

* Cppcon 2019: Faster Code Through Parallelism on CPU and GPU
* `RAM 1WnR`
* `#pragma HLS BIND STORAGE`
* function call viewer


## Versal Architecture Solutions for PCIe and Cache Coherent Interconnect [Eric Crabill (Xilinx)]

* in Versal
    * CPM4 and CPM5 (gen 4 and gen 5)
    * PL PCIE4 and PL PCIE5
    * SRIOV
    * integrated DMAs (QDMA and XDMA in hard IP)
    * CCIX support
    * connection to NoC
    * CCIX to CHI bridge

### CPM vs PL PCIE

* CPM - feature rich
* PL PCIE - migration from previous architectures

### QDMA vs XDMA

### CCIX and CXL

* hetergeneous computing
    * CPU + GPU
    * CPU + ACAP
    * CPU + Smart NIC
    * ...
* classic PCIe = moving the data with DMA (SW-controlled)
* Cache cohherence = "move the data without using a driver"
* CCIX = symmetrical (CPU and accelerators are peers)
* CXL = CPU is the owner, multiple protocols: `cxl.io`, `cxl.mem`, `cxl.cache`

### Documentation

* PG347 (for CPM)


# Day 6

## The Xilinx SN1000: Accelerate Your Cloud Data Centers for Scalability and Performance

* evolution (according to Xilinx)
    1. "traditional NIC"
    2. "offload NIC"
    3. "Programmable SmartNIC"
* specific requirements, needs to adapt to changing workloads
* Alveo SN1000 (PCIe gen3 x16, up to 16 A72)
* Vitis Networking Stack (P4), HLS (C, C++), RTL
* Architecture: plugins
* Virtio, `vhost-vdpa`, VirtIO NET PF
* vDPA - virtual Data-Path Acceleration (control plane managed by host)
* example: NVME-over-fabric, Ceph, `virtio-blk`


## Azure Quantum Optimizing on FPGAs

- "Scaled Quantum Computing"
- `Q#`, Python SDK
- problem formulalation
- PUBO [0, 1], Ising [-1, 1]
- provides: Honeywell, IonQ, 1QBit
- example
    - scheduling problem
    - CPU runtime - 3 min 12 sec
    - ```python
      from azure.quantum.optimization import SimulatedAnealing
      ```
    - ` ..., platform=HardwarePlatform.FPGA)`
    - FPGA runtime - 23 sec
    - "10x speedup"
- `aka.ms/qsharp-blog`

## FPGA-Accelerated Structured Query Language (FAStQL) for Azure Synapse Analytics

- Apache Spark, Data Source v2 (DSv2) interface
- FPGA handles: parsing, filter, projection
- support for Decimal
- profiling: 80% on parsing, 20% on query
- plans for the future: compression/decompression, hash join, ...
- architecture: row scheduler, N row parsers, row combiners
- parsing: 6 - 7 GB/s
- filtering: stack-based processor (same arch: scheduler, N proc, output)


## Improving Spark Storage Efficiency with NoLoad Transparent Compression

- "Data Tsunami"
- computational storage
- CSP (Computational Storage Processor): computation, no persistant storage
- CSD (Compuational Storage Drive): computation + peristent data storage (FPGA + SSD)
- *NVMe computation* - in the process of standardization, expected in 2022
- NoLoad (r)
    - NVMe-compilant front-end (looks like an NVMe device to the OS)
    - certified by UNH-IOL
    - accelerators: compression, decompression
    - compute: analytics, ML, AI
- NVMe-oF, Peer-to-Peer
- Apache Spark (data size up to PB), NoLoadFS, ZLIB compression offload
    - Cisco UCS


## Breaking the Bonds of CPU-Centric AI Inferencing with NeuReality

- "Server-on-a-Chip"
- cost, complexity
- current state
    - training pods (NVIDIA, GRAPHCORE, SambaNova, Cerebras)
    - Inferecne Servers: tenstorrent, untether.ai, nvidia, groq, Qualcomm
- issue with current systems (according to NeuReality):
    moving the data between NIC --> CPU --> DLA (Deep Learning Accelerator)
- Versal ACAP + unique IP
- Kubernetes-managed


---

<div style="font-size: 80%;" >
Xilinx, Inc. Xilinx, the Xilinx logo, Alveo, Vivado, Vitis, Versal, Zynq are trademarks of Xilinx in the United States and
other countries.
</div>

<div style="font-size: 80%;" >
All trademarks and registered trademarks are the property of their respective owners.
</div>
