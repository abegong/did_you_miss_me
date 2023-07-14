import unittest
from missingness_patterns import NeverMissingPattern, AlwaysMissingPattern, FractionMissingPattern, ContingentMissingPattern

class TestMissingnessPatterns(unittest.TestCase):
    def test_never_missing_pattern(self):
        # Test case for NeverMissingPattern
        pattern = NeverMissingPattern()
        self.assertEqual(pattern.is_missing(), False)

    def test_always_missing_pattern(self):
        # Test case for AlwaysMissingPattern
        pattern = AlwaysMissingPattern()
        self.assertEqual(pattern.is_missing(), True)

    def test_fraction_missing_pattern(self):
        # Test case for FractionMissingPattern
        pattern = FractionMissingPattern(0.5)
        self.assertIn(pattern.is_missing(), [True, False])

    def test_contingent_missing_pattern(self):
        # Test case for ContingentMissingPattern
        pattern = ContingentMissingPattern('column1', {'value1': 0.2, 'value2': 0.8})
        self.assertIn(pattern.is_missing(), [True, False])

if __name__ == '__main__':
    unittest.main()