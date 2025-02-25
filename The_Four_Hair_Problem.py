

# In this python code we will encode the four hair problem using quantum circuits.

# The problem is as follows. Alice, Bob, Charlie and Dylan all line up on a stage such that
# Alice can see Bob, Charlie, Dylan
# Bob can see Charlie and Dylan,
# and Charlie can see Dylan.

# Hair dye is randomly placed on all four participants hair, Orange (0) or Indigo (1).
# Come up with a strategy to correctly identity all four hair colors with highest probability given
# that each person can only speak one word.

# One strategy is to use parity. If Alice sees an even number of Indigo hair colors
# She says orange. If it is odd, she says indigo. Alice gets the wrong color 1 out of 2 times.
# But all other participants can get the correct answer of their hair color.


# We can do this with the CNOT gate and the Hadamard gate.

# Call
# Alice q0,
# Bob q1,
# Charlie q2,
# Dylan q3,

# and let q4 - q8 be qubits that represent each of the participants thought processes
import cirq

q0, q1, q2, q3, q4, q5, q6, q7 =cirq.LineQubit.range(8)

# Call the zero state even or orange.
# call the one state odd or indigo.
circuit=cirq.Circuit()

# Now lets begin by placing each of qubits in a superposition state of 0 and 1.
circuit.append([cirq.H(q) for q in (q0,q1,q2,q3)])
print(circuit)

# begin with alice, she sees all the participants and flips her quantum state
# representing her thought process depending on what she sees in front of her. Hence
circuit.append([cirq.CNOT(q,q4) for q in (q1,q2,q3)])
print(circuit)
# Now, the next three participants bob, charlie and dylan listen to the answer
# represented in the state of qubit q4 and take note of the parity of qubit 4

circuit.append([cirq.CNOT(q4,q) for q in (q5,q6,q7)])
print(circuit)

from cirq.circuits import InsertStrategy

# now the process repeats and bob looks in front of him and uses this to determine his own
# hair color. i.e.
circuit.append([cirq.CNOT(q,q5) for q in (q2,q3)],strategy=InsertStrategy.NEW)
print(circuit)
# and the others take note.
circuit.append([cirq.CNOT(q5,q) for q in (q6,q7)],strategy=InsertStrategy.NEW)
print(circuit)

# Now charlie can determine his hair color

circuit.append([cirq.CNOT(q3,q6)],strategy=InsertStrategy.NEW)
print(circuit)
# finally, Dylan can answer what hair color she has
circuit.append([cirq.CNOT(q6,q7)],strategy=InsertStrategy.NEW)
print(circuit)

# now , lets take a measurement


circuit.append(cirq.measure(q4,q5,q6,q7,key='measure_all'))

# here we measured q4-q7, these are the answers we gave. We would see that q5-q7 match up with
# q1-q3 while q4 is the partity counter, and q0 has a 50% chance of being correct.
s=cirq.Simulator()
results=s.simulate(circuit)



#sample the circuit
samples=s.run(circuit,repetitions=1500)



# label ticks with the binary states

import matplotlib.pyplot as plt

def binary_labels(num_qubits):
    return [bin(x)[2:].zfill(num_qubits) for x in range(2 ** num_qubits)]

print(binary_labels(4))

#histogram=result.histogram(key='measure_all')
# plot the results
cirq.plot_state_histogram(samples, plt.subplot(), title = 'Quantum four hair simulation', xlabel = 'State of the hair color', ylabel = 'State counts', tick_label=binary_labels(4))


plt.show()

# Notice that the more times you run the simulation, the closer the system comes to
# having equal probability of all four options.

