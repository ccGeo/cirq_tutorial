### Fun example

# Suppose there are two guardians standing in front of two doors. One with treasure, one
# with nothing. 1 of the guardians tells the truth, the other always lies. How can we figure
# out which door is the door we should open by asking a single question?
#

#Answer: We can ask which door would the other guard tell us Not to open?

#suppose the answer is door 2.
# if we ask the truthful guard the question, he will say that the liar would tell us not to open
# door 2.
# if we ask the liar he would tell us not to open door 2.

# Hence the answer is door 2.

# We can make this in terms of three qubits
## q0 guard one
## q1 guard two
## q2 for the lie - i.e. a qubit that encodes if the

# To make the circuit, we place the treasure randomly behind q0 or q1 we use hadamard gate on q0
# and link the state of q0 with q1 with a CNOT or X gate. Now both guardians know the same thing.
# and importanly both qubits would give the same answer after measurement.

# Now we use state of q2 to encode the lie. If q2 is in state 1 then we say guard 2 is lying and
# we flip his answer using a CNOT.
# If guard 1 is lying we flip his answer (again using a CNOT).
# a subtly is after applying CNOT(q2,q1) we must apply a NOT gate to q2 to switch to the
# other possibility then CNOT(q2,q0)
# then we must switch back to the original value of q2 at the end.


#
# By adding a hadamard gate on q2 during initialization, there is a 50/50 chance that guard 1 or 2 is lying.
#
# To encode the question: Which door would the other guard tell me not to open. We use a SWAP gate
# on q0 and q1 and since we want to know the negation of the information we add a NOT gate on
# on q0 and q1 individually.

# Now we must remember that one of the guardians is lying. So we must apply the answer swapping
# circuit we created before

import cirq

#make three qubits
q0, q1, q2 = cirq.LineQubit.range(3)

#initialize the circuit
circuit=cirq.Circuit(cirq.H(q0),cirq.H(q2),cirq.CNOT(q0,q1))
print(circuit)




circuit.append([cirq.CNOT(q2,q1),cirq.X(q2),cirq.CNOT(q2,q0),cirq.X(q2)])
# append this to the circuit after initialization to implement the lie.


print(circuit)


# Now ask the question.
circuit.append([cirq.SWAP(q0,q1),cirq.X(q0),cirq.X(q1)])
print(circuit)

# Now we need to remember that one of the guardians is lying... hence we need to change the liars
#answer.


circuit.append([cirq.CNOT(q2,q1),cirq.X(q2),cirq.CNOT(q2,q0),cirq.X(q2)])
print(circuit)


# we need to add a measurement at the end
circuit.append(cirq.measure(q0,q1,q2,key='result'))

s=cirq.Simulator()
results=s.simulate(circuit)



#sample the circuit
samples=s.run(circuit,repetitions=100000)


# label ticks with the binary states

import matplotlib.pyplot as plt

def binary_labels(num_qubits):
    return [bin(x)[2:].zfill(num_qubits) for x in range(2 ** num_qubits)]

# plot the results
cirq.plot_state_histogram(samples, plt.subplot(), title = 'Treasure Door Simulation', xlabel = 'End state', ylabel = 'State counts', tick_label=binary_labels(3))


plt.show()

# Notice that the more times you run the simulation, the closer the system comes to
# having equal probability of all four options.

