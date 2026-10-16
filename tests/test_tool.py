import unittest
import tool

class BehaviorTests(unittest.TestCase):
    def test_case_0(self):
        self.assertEqual([x["kind"] for x in tool.analyze({'services': {}})], [])

    def test_case_1(self):
        self.assertEqual([x["kind"] for x in tool.analyze({'services': {'web': ['db'], 'db': []}})], ['stage', 'stage'])

    def test_case_2(self):
        self.assertEqual([x["kind"] for x in tool.analyze({'services': {'a': [], 'b': []}})], ['stage'])

    def test_missing_required_input(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            tool.analyze({})


    def test_cycle_rejected(self):
        with self.assertRaises(ValueError): tool.analyze({'services':{'a':['b'],'b':['a']}})
    def test_unknown_dependency_rejected(self):
        with self.assertRaises(ValueError): tool.analyze({'services':{'a':['missing']}})
    def test_diamond_stages(self):
        result=tool.analyze({'services':{'a':[],'b':['a'],'c':['a'],'d':['b','c']}})
        self.assertEqual([x['services'] for x in result],[['a'],['b','c'],['d']])
