import cirq

# The primary rep of quantum programs in cirq is the Circuit class.
# a circuit is collection of moments.
# A moment is a collection of operations
# An operation is the application of an operator on a subset of qubits
# the most common type is a GateOperation

# qubits are instances of subclasses of the base class cirq.Qid
#example the qubits that google uses are often arranged on a square grid.

# create a square grid 9 qubits
qubits=cirq.GridQubit.square(3)
print(qubits[0])
print(qubits)

# a cirq.Gate represents a physical process that occurs on a qubit.
# it can be applied to more then one qubit

#The pauli X gate
x_gate=cirq.X
# applying it to the qubit at lattice site (0,0) turns it into an operation
x_op=x_gate(qubits[0])

print(x_op)

# recall a moment is a collection of operations at a given time slice.
#Note the moment structure is not required to be related to the actual scheduling of the operations
#on a quantum computer.
#Example a moment where X and CZ gate act on three qubits
cz=cirq.CZ(qubits[0],qubits[1])
x=cirq.X(qubits[2])
moment=cirq.Moment(x,cz)
print(moment)

# cirq.Circuit is an ordered series of cirq.Moment objects. Here is a simple circuit
#made up of two moments

cz01=cirq.CZ(qubits[0],qubits[1])
x2=cirq.X(qubits[2])
cz12=cirq.CZ(qubits[1],qubits[2])
moment0=cirq.Moment([cz01,x2])
moment1=cirq.Moment([cz12])
circuit=cirq.Circuit((moment0,moment1))

print(circuit)

# It is tedious to construct this by hand. append is a very useful way to construct circuits

q0, q1, q2 = [cirq.GridQubit(i,0) for i in range(3)]
circuit= cirq.Circuit()
circuit.append([cirq.CZ(q0,q1),cirq.H(q2)])
print(circuit)

# now continue appending moments

circuit.append([cirq.H(q0),cirq.CZ(q1,q2)])
print(circuit)

circuit.append([cirq.H(q0),cirq.H(q1),cirq.H(q2)])
print(circuit)

# you can also just string these altogether at once

circuit=cirq.Circuit()
circuit.append([cirq.CZ(q0,q1),cirq.H(q2),cirq.H(q0),cirq.CZ(q1,q2)])
print(circuit)

print(circuit)

# Notice... it got it right... how? Th eCircuit.append method take an argument called
# strategy... cirq.InsertStrategy. by default, InsertStrategy is InsertStrategy.Earliest

# What about other strategies?

# there are four such strategies based on the counter of Moment.
# InsertStrategy.EARLIEST,
# InsertStrategy.NEW,
# InsertStrategy.INLINE
# InsertStrategy.NEW_THEN_INLINE
# InsertStrategy.EARLIEST, which is the default, is defined as:
#Scans backward from the insert location until a moment
# with operations touching qubits affected by the operation to insert is found.
# The operation is added to the moment just after that location.

# example time using earliest means that the code can shuffle operations to the earliest
# moment if possible

from cirq.circuits import InsertStrategy

circuit=cirq.Circuit()
circuit.append([cirq.CZ(q0,q1)])
circuit.append([cirq.H(q0),cirq.H(q2)],strategy=InsertStrategy.EARLIEST)

print(circuit)

# compare to New
circuit=cirq.Circuit()
circuit.append([cirq.CZ(q0,q1)])
circuit.append([cirq.H(q0),cirq.H(q2)],strategy=InsertStrategy.NEW)

print(circuit)

# with new, each insertion is at a new time slice.

# compare now again with inline

circuit = cirq.Circuit()
circuit.append([cirq.CZ(q1,q2)])
circuit.append([cirq.CZ(q1,q2)])
circuit.append([cirq.H(q0),cirq.H(q1),cirq.H(q2)],strategy=InsertStrategy.INLINE)

print(circuit)

# This attempts to insert the operation before the current moment. If anything is already there
# then it creates a new moment for these operations and inserts the others in the previous moment

# finally new then inline.. creates a new moment for the first operation.
# then reverts to the inline strategy
circuit = cirq.Circuit()
circuit.append([cirq.H(q0)])
circuit.append([cirq.CZ(q1,q2),cirq.H(q0)],strategy=InsertStrategy.NEW_THEN_INLINE)

print(circuit)

# you