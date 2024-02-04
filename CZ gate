import perceval as pcvl
from perceval.components import Circuit, Processor
from perceval.components.unitary_components import *
from perceval.components.component_catalog import CatalogItem, AsType
from perceval.components.port import Port, Encoding


class HeraldedCzItem(CatalogItem):
    article_ref = "https://arxiv.org/abs/quant-ph/0110144"
    description = r"""CZ gate with 2 heralded modes"""
    str_repr = r"""                      ╭─────╮
ctrl (dual rail) ─────┤     ├───── ctrl (dual rail)
                 ─────┤     ├─────
                      │     │
data (dual rail) ─────┤     ├───── data (dual rail)
                 ─────┤     ├─────
                      ╰─────╯"""

    theta1 = 2*math.pi*54.74/180
    theta2 = 2*math.pi*17.63/180
    #The additional 2 factor takes into account the difference between the beam-splitter conventions of Perceval and the paper

    def __init__(self):
        super().__init__("heralded cz")
        self._default_opts['type'] = AsType.PROCESSOR

    def build_circuit(self, **kwargs) -> Circuit:
        # the matrix of this first circuit is the same as the one presented in the reference paper, the difference in the second phase shift - placed on mode 3 instead of mode 1 - is due to a different convention for the beam-splitters (signs inverted in second column).
        last_modes_cz = (Circuit(4)
                         .add(0, PS(math.pi), x_grid=1)
                         .add(3, PS(math.pi), x_grid=1)
                         .add((1, 2), PERM([1, 0]), x_grid=1)
                         .add((0, 1), BS.H(theta=self.theta1), x_grid=2)
                         .add((2, 3), BS.H(theta=self.theta1), x_grid=2)
                         .add((1, 2), PERM([1, 0]))
                         .add((0, 1), BS.H(theta=-self.theta1))
                         .add((2, 3), BS.H(theta=self.theta2)))

        return (Circuit(6, name="Heralded CZ")
                .add(1, PERM([1, 0]))
                .add(2, last_modes_cz, merge=True)
                .add(1, PERM([1, 0])))

    def build_processor(self, **kwargs) -> Processor:
        p = self._init_processor(**kwargs)
        return p.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl')) \
            .add_port(2, Port(Encoding.DUAL_RAIL, 'data')) \
            .add_herald(4, 1) \
            .add_herald(5, 1)



heralded_cz = HeraldedCzItem()
cz_circuit = heralded_cz.build_circuit()
cz_processor = heralded_cz.build_processor()
pcvl.pdisplay(cz_circuit) # the regular circuit



states = {
    pcvl.BasicState([1, 0, 1, 0]): "00",
    pcvl.BasicState([1, 0, 0, 1]): "01",
    pcvl.BasicState([0, 1, 1, 0]): "10",
    pcvl.BasicState([0, 1, 0, 1]): "11"
}

ca = pcvl.algorithm.Analyzer(cz_processor, states)

truth_table = {"00": "00", "01": "01", "10": "10", "11": "11"}
ca.compute(expected=truth_table)

pcvl.pdisplay(ca)
print(
    f"performance = {ca.performance}, fidelity = {ca.fidelity.real}")
pcvl.pdisplay(cz_processor, recursive=True) # circuit plus processing
