import numpy as np
import perceval as pcvl
from perceval.rendering.circuit import SymbSkin, PhysSkin
from perceval.components import BS, PERM, Port
from perceval.utils import Encoding

def cx():
    processor = pcvl.Processor("SLOS", 4)
    processor.add(2, pcvl.BS.H())
    processor.add(0, pcvl.catalog["heralded cz"].build_processor())
    processor.add(2, pcvl.BS.H())
    return (processor)


def get_CCZ():
    big_circuit=pcvl.Processor("SLOS", 6) 
    big_circuit.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl')) 
    big_circuit.add_port(2, Port(Encoding.DUAL_RAIL, 'ctrl')) 
    big_circuit.add_port(4, Port(Encoding.DUAL_RAIL, 'data')) 
    
    big_circuit.add(4, pcvl.BS.H())   #To make it a CCX instead of a CCZ for analyzer

    big_circuit.add(2,cx())     ##First CNOT

    big_circuit.add(5, pcvl.PS(phi=-np.pi/4)) ###First T_dag


    big_circuit.add(0,pcvl.PERM([0,1,4,5,2,3]))
    big_circuit.add(0,cx())
    big_circuit.add(0,pcvl.PERM([0,1,4,5,2,3]))   ##Second CNOT, needs to include a swap

    big_circuit.add(5, pcvl.PS(phi=np.pi/4))   ###First T

    big_circuit.add(2,cx())     ##Third CNOT

    big_circuit.add(5, pcvl.PS(phi=-np.pi/4)) ###Second T_dag

    big_circuit.add(0,pcvl.PERM([0,1,4,5,2,3]))
    big_circuit.add(0,cx())
    big_circuit.add(0,pcvl.PERM([0,1,4,5,2,3]))   ##Fourth CNOT, needs to include a swap

    big_circuit.add(3, pcvl.PS(phi=np.pi/4))   ###Second T
    big_circuit.add(5, pcvl.PS(phi=np.pi/4))   ###Third T

    big_circuit.add(0,cx())     ##Fifth CNOT

    big_circuit.add(1, pcvl.PS(phi=np.pi/4))   ###Fourth T

    big_circuit.add(3, pcvl.PS(phi=-np.pi/4))   ###Third T_Dag

    big_circuit.add(0,cx())     ##Sixth CNOT
    
    
    big_circuit.add(4, pcvl.BS.H())   #To make it a CCX instead of a CCZ for analyzer

    states = {
            pcvl.BasicState([1, 0, 1, 0, 1, 0]): "000",
            pcvl.BasicState([1, 0, 1, 0, 0, 1]): "001",
            pcvl.BasicState([1, 0, 0, 1, 1, 0]): "010",
            pcvl.BasicState([1, 0, 0, 1, 0, 1]): "011",
            pcvl.BasicState([0, 1, 1, 0, 1, 0]): "100",
            pcvl.BasicState([0, 1, 1, 0, 0, 1]): "101",
            pcvl.BasicState([0, 1, 0, 1, 1, 0]): "110",
            pcvl.BasicState([0, 1, 0, 1, 0, 1]): "111",
            # Can add as many input states as we want
        }
    truth_table = {"000": "000", "001": "001", "010": "010", "011": "011",
                       "100": "100", "101": "101", "110": "111", "111": "110"}



    ccz_analyzer = pcvl.algorithm.Analyzer(big_circuit, states,"*")

    ccz_analyzer.compute(expected=truth_table)

    pcvl.pdisplay(ccz_analyzer)
    print(f"Performance: {ccz_analyzer.performance}, Fidelity: {ccz_analyzer.fidelity.real}")


get_CCZ()
