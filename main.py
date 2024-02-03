""" 
This is what the main.py from quandela says: 
This is an example of the file you must have in your main git branch
import perceval as pcvl

def get_CCZ() -> pcvl.Processor:
    return pcvl.catalog["postprocessed ccz"].build_processor()

def get_CZ() -> pcvl.Processor:
    return pcvl.Processor("SLOS",6).add(0, pcvl.Unitary(pcvl.Matrix.eye(6)))
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

And the requirements.txt said:
perceval-quandela==0.10.3
    
"""

"""
Then this is like the bare bones of an attempt
"""

import perceval as pcvl

def get_CCZ() -> pcvl.Processor:
    # Create a Processor for the CCZ gate
    processor = pcvl.Processor("SLOS", 6)

    # Customise the linear optical circuit for the CCZ gate based on our design
    # Example: Using beam splitters (BS) and phase shifters (PS)
    processor.add(0, pcvl.BS.H())
    processor.add(2, pcvl.BS(theta=0.5))  # Adjust theta as needed
    processor.add(4, pcvl.BS(theta=0.8))  # Adjust theta as needed
    processor.add(1, pcvl.PS(phi=0.2))    # Adjust phi as needed
    processor.add(3, pcvl.PS(phi=0.4))    # Adjust phi as needed
    processor.add(5, pcvl.PS(phi=0.6))    # Adjust phi as needed

    # Return the Processor for the CCZ gate
    return processor

def get_CZ() -> pcvl.Processor:
    # Example: Create a Processor for a CZ gate
    return pcvl.Processor("SLOS", 6).add(0, pcvl.Unitary(pcvl.Matrix.eye(6)))

if __name__ == "__main__":
    # Need to add code for testing or further analysis here
    pass


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

"""
First Attempt before I saw the main.py or requirements.txt
"""

import perceval as pcvl

def get_CCZ():
    # Create a Processor for the CCZ gate
    processor = pcvl.Processor("SLOS", 6)  # Adjust the number of modes

    # Add the linear optical circuit for the CCZ gate
    # Can customise the circuit based on our design for the CCZ gate

    # This is just a random example
    # Adding beam splitters and phase shifters
    processor.add(0, pcvl.BS.H())
    # We can more components based on the design

    # Define the input states for the CCZ gate
    states = {
        pcvl.BasicState([1, 0, 0, 0, 1, 0]): "000",
        # Can add as many input states as we want
    }

    # Create an analyser to compute fidelity and performance
    ca = pcvl.algorithm.Analyzer(processor, states)

    # Define a truth table for expected results 
    truth_table = {"000": "000", "001": "001", "010": "010", "011": "011",
                   "100": "100", "101": "101", "110": "110", "111": "111"}
    
    # Compute fidelity and performance
    ca.compute(expected=truth_table)

    # Display results
    pcvl.pdisplay(ca)
    print(f"Performance: {ca.performance}, Fidelity: {ca.fidelity.real}")

    # Return the Processor for the CCZ gate
    return processor
