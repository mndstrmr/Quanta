import unittest
import quantum as Q
import random

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)
        return callHelper
    return repeatHelper

class QTesting(unittest.TestCase):
    @repeat(20)
    def test_0X(self):
        bit = Q.Qubit(Q.State.zero())
        bit.X()
        self.assertTrue(bit.M())

    def test_0H(self):
        average = 0
        for i in range(1000):
            bit = Q.Qubit(Q.State.zero())
            bit.H()
            if bit.M(): average += 1

        self.assertTrue(abs(average - 500) < 50)

    @repeat(100)
    def test_01CNOT(self):
        bit1 = Q.Qubit(Q.State.zero())
        bit2 = Q.Qubit(Q.State.one())
        Q.CNOT(bit1, bit2)
        m1, m2 = bit1.M(), bit2.M()

        self.assertTrue((not m1) and m2)

    @repeat(100)
    def test_H1CNOT(self):
        bit1 = Q.Qubit(Q.State.zero())
        bit1.H()
        bit2 = Q.Qubit(Q.State.one())
        Q.CNOT(bit1, bit2)
        m1, m2 = bit1.M(), bit2.M()

        self.assertNotEqual(m1, m2)

    @repeat(100)
    def test_1H1CCNOT(self):
        reg = Q.create_register(3)
        reg[0].set(Q.State.one())
        reg[1].H()
        reg[2].set(Q.State.one())
        Q.CCNOT(*reg)
        m1, m2, m3 = Q.observe_all(*reg)

        self.assertTrue(m1 and (m2 != m3))

    @repeat(100)
    def test_QnumberADD(self):
        a = random.randint(0, 32)
        b = random.randint(0, 32)

        n1 = Q.number.QInteger.from_pyint(a)
        n2 = Q.number.QInteger.from_pyint(b)
        
        self.assertEqual((n1 + n2).to_pyint(), a + b)

if __name__ == "__main__":
    unittest.main()