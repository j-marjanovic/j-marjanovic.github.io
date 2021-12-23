Title: Notes on "A Primer on Memory Consistency and Cache Coherence"
Date: 2021-12-23 16:00
Tags: Books

[A Primer on Memory Consistency and Cache Coherence, Second Edition](https://www.morganclaypool.com/doi/abs/10.2200/S00962ED2V01Y201910CAC049)

Authors:

- Vijay Nagarajan, University of Edinburgh
- Daniel J. Sorin, Duke University
- Mark D. Hill, University of Wisconsin, Madison
- David A. Wood, University of Wisconsin, Madison

> "This primer is intended for readers who have encountered memory consistency
> and cache coherence informally, but now want to understand what they entail
> in more detail."

- \[this book talks to me\]

# Chapter 1

- *memory consistency* - effects of stores and loads on the memory, correct behavior
- *cache coherence* - HW implementation to ensure correct behavior when caches are involved
- *memory (consistency) model* - the specification about allowed behavior of MT programs
- *snooping* - cache controller performs a broadcast

# Chapter 2

- *memory-side cache* (last-level cache) - not a concern in regards to coherence, just reduces the latency
- "Informally, a coherence protocol must ensure that writes are made visible to all processors."
- *consistency-agnostic* coherence (atomic writes) vs *consistency-directed* coherence (\[posted\] writes, ordering rules)
- *single-writer-multiple-reader (SWMR) invariant*
* *data-value invariant*
* other definitions of invariants

# Chapter 3

- reordering, write buffer
- *MC (memory consistency) model*
- core pipeline can have an impact on the consistency


## Sequential consistency

- [L. Lamport: How to Make a Correct Multiprocess Program Execute Correctly on a Multiprocessor](https://lamport.azurewebsites.net/pubs/lamport-how-to-make.pdf)
- *program order*, *memory order*
- `op1 <m op2`, `op1 <p op2`
- **for SC**: `op1 <p op2 ==> op1 <m op2` (`==>` = implies)
- requirement: LL, LS, SS, SL dependencies, loads get the value of the last store, atomic RWM
- naive implementation: **the switch**
- speculative loads are just discarded, speculative stores only present the address and not the data -->
  cache can check if (or inform) other caches have the datum
- multi-threading: other threads must have independent write buffer (so to behave like other processors);
  normal write buffers (with queue) are anyway not possible in SC
- \[ [Mod-01 Lec-32 Case study: MIPS R10000](https://www.youtube.com/watch?v=EYmEaF4qJ9I) \]

# Chapter 4

- *total store order (TSO)*
- "[TSO] model astonishes some people..."
- TSO behaves equally for programs that: 1. store data first, 2. then store `done` flag
- write buffer, FIFO
- `FENCE` instr

# Chapter 5

- *relaxed (weak) memory consistency*
- most application do not require strong consistency
- accesses can be re-ordered, *Coalescing Write Buffer*

## Example Relaxed Consistency Model (XC)

- `FENCE` instruction
- TSO for accessing the same address (LL, LS, SS)
- *data race* - two or more programs accessing the same memory, at least one access is a write

## Release Consistency

- `ACQUIRE`, `RELEASE` instead of `FENCE`

## RVWMO

- *dependency-induced ordering*
- *same address ordering*
- *Atomic Memory Operation (AMO)* and *Load Reserve/Store Conditional*

## IBM POWER

> "On a first pass of this primer, readers may wish to skim or skip this
> section; this memory model is significantly more complicated than the models
> presented thus far in this primer."

## ARMv7, ARMv8

- ARMv7 similar to POWER
- ARMv8 provides a total memory order, has `ACQUIRE` and `RELEASE`

## High-level Language Models

- SC for DRF

# Chapter 6

- two invariants: SWMR, data-value
- *coherence controller*: a FSM, one per each cache (*cache controller*) or memory (*memory controller*)
- *coherence protocol*: communication between FSM

"Other agents, such as I/O devices, may behave like cache controllers, memory
controllers, or both depending upon their specific requirements."

## States

- four characteristics:

  * validity
  * dirtiness
  * exclusivity
  * ownership

- stable states:

  * **M**odified: valid and potentially dirty
  * **O**wned: valid and owned, possibly stale, read-only
  * **E**xclusive: no other cache has a copy, read-only
  * **S**hared: valid but not exclusive and not dirty, read-only
  * **I**nvalid: not present in the cache or stale

- transient states:
  $$ XY^Z $$

* *snooping* vs *directory*
- *invalidate* vs *update*

# Chapter 7

"all coherence controllers observe (snoop) coherence requests in the same order
and collectively "do the right thing" to maintain coherence."

- transactions need to be ordered
- *serialization (ordering) point*, e.g. bus arbitration

## baseline: MSI

- atomic requests and atomic transactions
- processor loads go from Invalid to Shared
- processor stores go from Invalid to Modified
- both loads and stores wait for the data before transitioning to the steady state
- if Modified, GetS and GetM from other cores transition to Shared and Invalid, respectively

## Non-atomic requests, atomic transactions

- queue or buffer between the cache controller and the bus (or interconnect)

## Exclusive state

- handles case when the block is first read and then written -> no need to inform other cores
- GetS brings the block state to S or E (depends on states of other controllers)

## Owned state

- when a block is in state M or E and receives GetS

## Non-atomic bus

- *in-order* vs *out-of-order*
- FIFO queues between the controller and request and response bus

## Interconnect network

- tree topology
- *Timestamp Snooping*

# Chapter 8

"Directory protocols were originally developed to address the lack of
scalability of snooping protocols."

- *directory* with a global view
- transactions typically involve 2 or 3 steps:
  - a request by the controller and a reply by the directory
  - a request by the controller, requests to other controllers and replies from other controllers
  - 4th step is also possible

- *directory* as the serialization point
- for some requests (e.g. GetM) all caches with a block in state S must ACK

## MSI

- an entry (per each block) consists of the state bits, owner id (if in state M)
  and sharer list (bit vector, if in state S)
- I or S to M: directory returns to the requestor the number of controllers which must ACK
- PutM: contains data (from the controller to the directory)
- *virtual networks* (message class) to avoid deadlocks (requests blocking responses)

## Exclusive state

- GetS and not shared by other controllers --> E
- a core can silently (no coherence request required) upgrade E to M
- E block: owned vs not-owned
- PutE (directory from E to I)

## Owned state

- \[how did it got dirty if it is read-only?\]
- Owned is basically a frozen Modified state

## Directory state

- full representation only for smaller number of cores
- *coarse directory*: more controllers are "grouped" in a same bit
- *limited pointer directory*: broadcast after I sharers, invalidate one of the sharers, trap to a SW handler

## Directory organization

- one entry per each block of the memory
- *directory cache*: accesses have (usually) good locality, smaller datums (\[ROMANES EUNT DOMUS\])--> even small caches have a high hit rate
  - backed by DRAM
  - *inclusive*: only for blocks cached, a miss indicates the I state
  - *Null Directory Cache*: \[this sounds more like a snooping protocol\]

## Optimizations

> "The typical, general solution to the problem of a centralized bottleneck is
>  to distribute the resource."

- distributed directories
- non-stalling directory protocols
- eviction of blocks in S state

# Chapter 9

## Instruction caches

> "[...] truly self-modifying code is rare,"

- core writes to D$, I$ only observers writes
- `icbi` (instruction cache block invalidate) instruction on POWER

## Virtual caches

- advantage: no need for address translation (on the critical path)
- require reverse address translation
- *synonyms*: same virtual address mapped to multiple physical addresses

## Write-true caches

- two-state protocol (VI)
- simpler evictions
- some issues with multi-threading

## Coherent DMA

> "DMA controllers have very different locality patterns than conventional cores"
- GetMs are wasteful, the entire block is typically overwritten --> special requests

## Multi-level caches

- *inclusive cache*: e.g. L2 contains a superset of L1
- multiple multi-processors: LLC as a *memory-side* or *core-side* cache
- hierarchical protocol: *intra-chip*, *inter-chip* (e.g. intra-chip snooping, inter-chip directory)

## Performance optimization

### Migratory sharing

- one thread reads and writes, then another thread reads and writes, ...
- E state already helps
- HW to detect GetS and then GetM
- alternatively, add Migratory M state (I -> S -> M)

### False sharing

- more cores accessing the same block without actually dependencies; solutions: sub-block coherence, speculation

## Liveness

- deadlock - cyclical dependencies
- protocol deadlock
- cache resource deadlock
- virtual networks
- livelock - a special case of starvation
- starvation (solved with fair arbitration)

## Token Coherence

- a third method (alongside snooping and directory-based protocols)
- tokens instead of status bits
- cores exchange tokens
- a core with one token can read, a core with all tokens can write to a block

# Chapter 10

> "This is the age of specialization."

- SoC share one physical memories, e.g. GPUs have two separate physical memories
- *cooperative thread array (CTA)*
- *SIMT - Single-Instruction-Multiple-Thread*
- http://www0.cs.ucl.ac.uk/staff/j.alglave/papers/asplos15.pdf
- GPU: relaxed memory order
- one approach: consistency-agnostics coherence protocol - not suitable for GPUs (large L1 caches, many threads = many transactions)

## Temporal coherence

- lease (limited amount of time), block gets automatically invalidated
- global notion of time
- GetV(t), Write, WriteV(t)
- stalled writes (until the lease expires)

- GWCT (Global Write Completion Time) - all FENCE must stall until this time
- performance sensitive to the selection of lease time
- timestamp complexity (e.g. rollover)

## Release consistency-directed coherence

- atomic operations which order memory accesses in one direction (in contrast with FENCE)
- scope (CTA vs GPU)

## Heterogeneous systems

- more devices with different memory consistency models
- intuition: the weaker model of the two
- OpenCL: SC for HRF (Heterogeneous-Race-Free)

## Heterogeneous coherence protocols

- global controller
- local controllers contain shims (or translators)

> "the global coherence interface must disambiguate CPU sharers from GPU
> sharers"

- coherence tracking at a larger granularity (e.g. page instead of a cache line)
- *scratchpads* in GPUs (programmer-controlled memories)

# Chapter 11

- specification = contract between the user and the implementation
- *input actions*, *internal actions*, *output actions*
- *safety* and *liveness*

## Operational specification

- state machine
- liveness ensured with *temporal logic*
- *linearizability*
- [CMurphi](http://mclab.di.uniroma1.it/site/index.php/software/18-cmurphi) and TLA

## Axiomatic specification

- Alloy, Herd

## Litmus tests

- https://www.cl.cam.ac.uk/~sf502/regressions/rmem/
- https://github.com/nvlabs/litmustestgen

## Validation

### Formal methods

- manual methods (e.g. assigning timestamps as values)
- model checkers (state space becomes quickly very large)

## Testing

- Off-line testing
- On-line testing (checker implemented in HW)
