
import cirq

# Pick a qubit.
qubit = cirq.GridQubit(0, 0)

# Create a circuit that applies a square root of NOT gate, then measures the qubit.
circuit = cirq.Circuit(cirq.X(qubit) ** 0.5, cirq.measure(qubit, key='m'))
print("Circuit:")
print(circuit)

# Simulate the circuit several times.
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)


import cirq_google;

print(cirq_google.Sycamore)


#Basics of cirq

#you can name a qubit
q0=cirq.NamedQubit('source')
q1=cirq.NamedQubit('target')

# you can make a line of qubits, created individually
q3=cirq.LineQubit(3)
#print(q3)

#or you can create them in a range.
#q0,q1,q2 = cirq.LineQubit(3)

#you can make a grid of qubits
q4_5=cirq.GridQubit(4,5)

# or you can create in bulk a square
#This will make 16 qubits arranged in a square lattice from (0,0) to (3,3)
qubits=cirq.GridQubit.square(4)
print(qubits)

#gates and operators

cnot_gate=cirq.CNOT
puali_z=cirq.Z

#Use exponentiation to get a square root gate
sqrt_x=cirq.X**0.5

#create some qubits to act on
q0, q1 = cirq.LineQubit.range(2)

#example operations
z_op=cirq.Z(q0)
not_op=cirq.CNOT(q0,q1)
sqrt_iswap_op=cirq.SQRT_ISWAP(q0,q1)

print(z_op,sqrt_iswap_op)

# Construct a quantum circuit. This is a collection of moments, i.e. a collection
# of operations that act during a given time slice. Each operation must
# be applied to a disjoint set of qubits compared to each of the other operations in moment.

circuit=cirq.Circuit()
qubits=cirq.LineQubit.range(3)
circuit.append(cirq.H(qubits[0]))
circuit.append(cirq.H(qubits[1]))
circuit.append(cirq.H(qubits[2]))
print(circuit)

#you can also make a list of operators
circuit=cirq.Circuit()
ops=[cirq.H(q) for q in cirq.LineQubit.range(3)]
circuit.append(ops)
print(circuit)

# a generator also works.
circuit=cirq.Circuit()
circuit.append(cirq.H(q) for q in cirq.LineQubit.range(3))
print(circuit)
#initializer with generator
print(cirq.Circuit(cirq.H(q) for q in cirq.LineQubit.range(3)))

#Notice.. H is the hadamard gate

#Notice that all of the hadamard gates are pushed as far left as possible. In the same moment
# if your operations are applied to the same qubits, they will be put in sequential, insertion-ordered moments
# here two qubit gates overlap and placed in consecutive moments
print(cirq.Circuit(cirq.SWAP(q,q+1) for q in cirq.LineQubit.range(3)))


# sometimes you may not want cirq to autmatically shift operations all the way to the left.
#to construct a circuit without doing this you can create the circuit
#moment by moment... or use a different InsertStrategy.. more on this later.

# creates gates momennt by momentum
print(cirq.Circuit(cirq.Moment([cirq.H(q)]) for q in cirq.LineQubit.range(3)))

#####################

# Circuits and devices.

#device objects specify constraints and can be used to validate your circuit...
#checking for illegal operations. More on devices later.

#example.
q0=cirq.GridQubit(5,6)
q1=cirq.GridQubit(5,5)
q2=cirq.GridQubit(4,5)

# create operations using the sycamore gate supported by the sycamore device.
# create operations for both adjacent and no-adjacent qubit pairs.

adjacent_op=cirq_google.SYC(q0,q1)
nonadjacent_op=cirq_google.SYC(q0,q2)

#A workign circuit for the sycamore decive raises no issues.
working_circuit=cirq.Circuit()
working_circuit.append(adjacent_op)
valid=cirq_google.Sycamore.validate_circuit(working_circuit)
print(valid)

#a circuit with invalid operations
bad_circuit=cirq.Circuit()
bad_circuit.append(nonadjacent_op)
try:
    cirq_google.Sycamore.validate_circuit(bad_circuit)
except ValueError as e:
    print(e)

#############################

#Simulation

#The results of the application of a quantum circuit can be calculated by a simulator
#Cirq comes bundled with a simulator that can calculate the results of circuits up to a limit
#of 20 qubits  it is initillized by cirq.Simulator()

#two approaches
#           simulate(): classically simulating a circuit. Directly accesses and views the wave f^
#                       This is useful for debugging and understanding how cirucits function
#           run():      With actual devices, we can only view the result, and we must sample the
#                       the solution to get a distribution of results.
#                       Running the simulator as a smpler mimics this behavior

# exmaple simulate the 2-qubit bell states.

#create a circuit to generate the Bell state.
bell_circuit=cirq.Circuit()
q0, q1 = cirq.LineQubit.range(2)
bell_circuit.append(cirq.H(q0))
bell_circuit.append(cirq.CNOT(q0,q1))

#Init the simulator
s=cirq.Simulator()

print('Simulate the circuit:')
results=s.simulate(bell_circuit)
print(results)

#for sampling, we need to add a measurement at teh end
bell_circuit.append(cirq.measure(q0,q1,key='result'))

#sample the circuit
samples=s.run(bell_circuit,repetitions=1000)


##############

# #visulaization


# cirq provides a quantum virtual machine, a simulated virtual version of quantum hardware

# two components
    # a virtual engine interface. Enables you to verify and run circuits with the same interface
    # that the quantum hardware would have
    #A set of noise models that try to realistically replicate the noise present in actual quantum
    #hardware devices

#when you use run get a smaple distribution of measurements you can directly graph the simulated
#result as a histogram

import matplotlib.pyplot as plt

cirq.plot_state_histogram(samples,plt.subplot())
plt.show()

#notice this has sparse qubit states. therefore pull from teh result data structure
#and ignore qubit states that are not seen

counts=samples.histogram(key='result')
print(counts)

#graph the histogram counts instead of the results
cirq.plot_state_histogram(counts,plt.subplot())
plt.show()


# parameter sweeps

#cirq allows for gates to have sybols as free parameters within the circuit. This is useful for
#variational algorithms, to optimize a cost function.
#for parameters cirq uses sympy to add symp.Symbol as parameters to gates and operations

# once the circuit is complete you can fill in the possible values of each of these parameters with
#a sweep.

# there are several possibilities.

#cirq.Points: a list of manually specified values ofr one specific symbol as a sequence of floats
#cirq.Linspace: a linear sweep from a starting value to an ending value
#cirq.ListSweep: a list of manually specified values of rseveral different sym, specified as a list of directories
#cirq.Zip and cirq.Product: Sweeps can be combined list-wise by zipping them together or through their catesian product

# run() to run_sweep() can be used to run a parameterized circuit and sweep together

# example

# sweeping an exponent of the X gate

import sympy

# Perform an X gate with variable exponent
q=cirq.GridQubit(1,1)
circuit=cirq.Circuit(cirq.X(q) ** sympy.Symbol('t'), cirq.measure(q,key='m'))

# sweep exponent from zero to on and back to off.
param_sweep=cirq.Linspace('t', start=0, stop=2,length=200)

#simulate the sweep
s=cirq.Simulator()
trials=s.run_sweep(circuit,param_sweep,repetitions=1000)


#Plotting the results
x_data=[trial.params['t'] for trial in trials]
y_data=[trial.histogram(key='m')[1]/1000.0 for trial in trials]
plt.scatter('t','p',data={'t':x_data,'p':y_data})
plt.xlabel("trials")
plt.ylabel("freq. of qubit measured to be one")
plt.show()



#############################3

### Unitary matrices and decomp.

# unitary matrix representations  can be accessed by applying cirq.unitary(operation)
# applyable to : gates, operations, circuits etc.

print('Unitary of the X gate')
print(cirq.unitary(cirq.X))

print('Unitary of SWAP operator on two qubits')
q0, q1 = cirq.LineQubit.range(2)
print(cirq.unitary(cirq.SWAP(q0,q1)))

print('Unitary of s sample circuit')
print(cirq.unitary(cirq.Circuit(cirq.X(q0),cirq.SWAP(q0,q1))))


##### decompositions

# many gates can be decomposed into an equibalent circuit with simpler operations and gates.
# it can be done with cirq.deompose

#exmaple the Hadamard gate H can be decomposed into x and y gates
print(cirq.decompose(cirq.H(cirq.LineQubit(0))))


### another example is the 3qubit Toffoli gate=controlled-controlled-X gate.
# many devices do not support three qubit gates. Hence we must decompose them into one and two qubit gates

q0, q1, q2 = cirq.LineQubit.range(3)
print(cirq.Circuit(cirq.decompose(cirq.TOFFOLI(q0,q1,q2))))


# final example of the tutorial Transformers

# transformers modify circuits.

#Example: cirq.merge_single_qubit_gates_to_phxz will take consecutive single-qubit operations
#and merge them into a single PhasedXZ operation

q=cirq.GridQubit(1,1)
c=cirq.Circuit(cirq.X(q)**0.25 , cirq.Y(q)**0.25,cirq.Z(q)**0.25)
#now display the circuit
print(c)
#now transform teh circuit by merging the operations
c=cirq.merge_single_qubit_moments_to_phxz(c)
#view the result of the merge
print(c)



#Thats it. The basic tutorial is complete. Now on to other bigger better topics.