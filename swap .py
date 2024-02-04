import perceval as pcvl

def swap_test(unitary_function):
    # Define Quantum Registers
    qubit_Alice = pcvl.Register(1, 'Alice')
    qubit_Bob = pcvl.Register(1, 'Bob')
    auxiliary = pcvl.Register(2, 'Aux')

    # Create a Processor for the swap test circuit
    swap_test_circuit = pcvl.Processor("SLOS", 4)

    # Apply Hadamard gate on first ancillary qubit
    swap_test_circuit.add(0, pcvl.H(), targets=[auxiliary[0]])

    # Apply swap gate
    swap_test_circuit.add([1, 2], pcvl.CSWAP(), targets=[auxiliary[0]])

    # Apply Hadamard gate on first ancillary qubit again
    swap_test_circuit.add(0, pcvl.H(), targets=[auxiliary[0]])

    # Measure first ancillary qubit
    swap_test_circuit.measure([0], [2])

    # Apply unitary function on Alice's qubit
    swap_test_circuit.add(3, pcvl.Unitary(unitary_function), targets=[qubit_Alice[0]])

    return swap_test_circuit
