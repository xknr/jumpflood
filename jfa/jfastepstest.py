import unittest

from jfa.jfasteps import JfaSteps


class TestJfaSteps(unittest.TestCase):

    def test_maxStep(self):
        self.assertEqual(JfaSteps.calcMaxStep(200, 100), 200)
        self.assertEqual(JfaSteps.calcMaxStep(20, 20), 20)
        

    def test_increasing(self):
        self.assertEqual(JfaSteps.jfaIncreasing(15), [1, 2, 4, 8])
        self.assertEqual(JfaSteps.jfaIncreasing(16), [1, 2, 4, 8])
        self.assertEqual(JfaSteps.jfaIncreasing(17), [1, 2, 4, 8, 16])

    def test_jfa(self):
        self.assertEqual(JfaSteps.jfa(15), [8, 4, 2, 1])
        self.assertEqual(JfaSteps.jfa(16), [8, 4, 2, 1])
        self.assertEqual(JfaSteps.jfa(17), [16, 8, 4, 2, 1])

    def test_1jfa(self):
        self.assertEqual(JfaSteps._1jfa(15), [1, 8, 4, 2, 1])
        self.assertEqual(JfaSteps._1jfa(16), [1, 8, 4, 2, 1])
        self.assertEqual(JfaSteps._1jfa(17), [1, 16, 8, 4, 2, 1])

    def test_jfa1(self):
        self.assertEqual(JfaSteps.jfa1(15), [8, 4, 2, 1, 1])
        self.assertEqual(JfaSteps.jfa1(16), [8, 4, 2, 1, 1])
        self.assertEqual(JfaSteps.jfa1(17), [16, 8, 4, 2, 1, 1])

    def test_jfa2(self):
        self.assertEqual(JfaSteps.jfa2(15), [8, 4, 2, 1, 2, 1])
        self.assertEqual(JfaSteps.jfa2(16), [8, 4, 2, 1, 2, 1])
        self.assertEqual(JfaSteps.jfa2(17), [16, 8, 4, 2, 1, 2, 1])

    def test_jfaPow2(self):
        self.assertEqual(JfaSteps.jfaPow2(15), [8, 4, 2, 1, 8, 4, 2, 1])
        self.assertEqual(JfaSteps.jfaPow2(16), [8, 4, 2, 1, 8, 4, 2, 1])
        self.assertEqual(JfaSteps.jfaPow2(17), [16, 8, 4, 2, 1, 16, 8, 4, 2, 1])
        pass
