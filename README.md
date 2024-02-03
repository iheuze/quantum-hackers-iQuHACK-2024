# quantum-hackers
# Quantum Gate Implementation with Perceval

## Introduction

project on quantum gate implementation using the Perceval quantum simulation framework. 
  design and analysis of CZ and CCZ gates.
  aiming to reproduce specific results and look at the fidelity and performance of these quantum gates.

## Implementation Details

### CZ Gate
At the moment, the CZ gate is made up of beam splitters with by the parameter 'theta'. The `get_CZ()` function in `main.py` creates a Processor for the CZ gate and the reproduces results for predefined input states.

### CCZ Gate
Then the CCZ gate uses both beam splitters and phase shifters. The `get_CCZ()` function in `main.py` creates a Processor for the CCZ gate, circuit open for customisation based on what we want.

## Executing the Code

To reproduce results for the CZ gate, use the following command:

```bash
python main.py reproduce_CZ_results
