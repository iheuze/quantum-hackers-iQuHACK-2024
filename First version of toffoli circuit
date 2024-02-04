import perceval as pcvl
from perceval.rendering.circuit import SymbSkin, PhysSkin

def cx():
    processor = pcvl.Processor("SLOS", 4)
    processor.add(2, pcvl.BS.H())
    processor.add(0, pcvl.catalog["heralded cz"].build_processor())
    processor.add(2, pcvl.BS.H())
    return (processor)

big_circuit=pcvl.Processor("SLOS", 6)

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

pcvl.pdisplay(big_circuit, skin=SymbSkin())
