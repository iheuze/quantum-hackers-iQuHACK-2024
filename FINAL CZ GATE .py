import perceval as pcvl
from perceval.components import Circuit, Processor
from perceval.components.unitary_components import *
from perceval.components.component_catalog import CatalogItem, AsType
from perceval.components.port import Port, Encoding

# Catalog Item for the Heralded CZ gate
class HeraldedCzItem(CatalogItem):
    # asking for inputs theta1 and theta2
    def __init__(self, theta1, theta2):
        super().__init__("heralded cz")
        self._default_opts['type'] = AsType.PROCESSOR
        self.theta1 = theta1
        self.theta2 = theta2

    def build_circuit(self, **kwargs) -> Circuit:
        # The 180 PhaseShift is placed on mode 3 instead of mode 1 due to a different convention for the beam-splitters in Perceval (signs inverted in second column).
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



# Testing the gate
# defining input states and truth table
states = {
    pcvl.BasicState([1, 0, 1, 0]): "00",
    pcvl.BasicState([1, 0, 0, 1]): "01",
    pcvl.BasicState([0, 1, 1, 0]): "10",
    pcvl.BasicState([0, 1, 0, 1]): "11"
}
truth_table = {"00": "00", "01": "01", "10": "11", "11": "10"}



#The additional 2 factor in the angle takes into account the difference between the beam-splitter conventions of Perceval and the paper
list1=np.linspace(10,80,60)
list2=np.linspace(10,80,60)
theta1_list = 2*math.pi*list1/180
theta2_list = 2*math.pi*list2/180
performance_list = []

# iterating through angles for the beamsplitters and phase shifts in the circuit, searching for the best fidelity and accuracy
for theta1_val in theta1_list:
  for theta2_val in theta2_list:
    heralded_cz = HeraldedCzItem(theta1=theta1_val, theta2=theta2_val)

    processor = pcvl.Processor("SLOS", 4)
    processor.add(2, pcvl.BS.H())
    processor.add(0, heralded_cz.build_processor())
    processor.add(2, pcvl.BS.H())

    ca = pcvl.algorithm.Analyzer(processor, states)
    ca.compute(expected=truth_table)

    performance_dict = {
                'theta1': theta1_val,
                'theta2': theta2_val,
                'performance': ca.performance,
                'fidelity' : ca.fidelity.real
            }
    performance_list.append(performance_dict)







import matplotlib.pyplot as plt

# Plotting Results

# Extracting theta1, theta2, and performance values from the performance_list
theta1_values = [d['theta1'] for d in performance_list]
theta2_values = [d['theta2'] for d in performance_list]
performances = [d['performance'] for d in performance_list]
fidelities = [d['fidelity'] for d in performance_list]

fig, axs = plt.subplots(1, 2, figsize=(12, 6)) # 1 row, 2 columns of graphs

# Plotting performance vs theta1
axs[0].scatter(theta1_values, performances, label = 'performance')
axs[0].scatter(theta1_values, fidelities, label = 'fidelity')
axs[0].set_title('Performance and Fidelity vs Theta1')
axs[0].set_xlabel('Theta1 (radians)')
axs[0].set_ylabel('Performance')
axs[0].legend()

# Plotting performance vs theta2
axs[1].scatter(theta2_values, performances, label = 'performance')
axs[1].scatter(theta2_values, fidelities, label = 'fidelity')
axs[1].set_title('Performance and Fidelity vs Theta2')
axs[1].set_xlabel('Theta2 (radians)')
axs[1].legend()
# No need to set ylabel for the second plot if they share the same y-axis label

plt.tight_layout() # Adjusts subplot params so that subplots fit into the figure area.
plt.show()






# Obtaining the perfomrances of the top 10 highest fidelities

sorted_performance_list = sorted(performance_list, key=lambda x: x['fidelity'], reverse=True)

# Get the top 10 entries with the highest fidelity
top_10_fidelity = sorted_performance_list[:10]

# Initialize empty lists for each parameter
theta1_top = []
theta2_top = []
performance_top = []
fidelity_top = []

# Iterate through the top 10 fidelity entries
for entry in top_10_fidelity:
    # Append each parameter to its respective list
    theta1_top.append(entry['theta1'])
    theta2_top.append(entry['theta2'])
    performance_top.append(entry['performance'])
    fidelity_top.append(entry['fidelity'])

print("Theta1:", theta1_top)
print("Theta2:", theta2_top)
print("Performance:", performance_top)
print("Fidelity:", fidelity_top)

fig, axs = plt.subplots(1, 2, figsize=(12, 6)) # 1 row, 2 columns of graphs

# Plotting performance vs theta1
axs[0].scatter(theta1_top, performance_top)
axs[0].scatter(theta1_top, fidelity_top)
axs[0].set_title('Performance vs Theta1')
axs[0].set_xlabel('Theta1 (radians)')
axs[0].set_ylabel('Performance')

# Plotting performance vs theta2
axs[1].scatter(theta2_top, performance_top)
axs[1].scatter(theta2_top, fidelity_top)
axs[1].set_title('Performance vs Theta2')
axs[1].set_xlabel('Theta2 (radians)')
# No need to set ylabel for the second plot if they share the same y-axis label

plt.tight_layout() # Adjusts subplot params so that subplots fit into the figure area.
plt.show()






#As we can see we obatin a performance of 0.07230068007628097 for the highest fidelity measurement (with a fidelity of 0.9999667669263683) but if we accept a very high fidelity of 0.9997316971470791 then we achieve a performance of 0.07559270785728286, higher than the paper from Knill
