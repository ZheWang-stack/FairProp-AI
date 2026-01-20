import unittest
import sys
import os

from fairprop import FairHousingAuditor

class TestFairHousingAuditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize auditor with the rules file in the parent directory
        rules_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fha_rules.json")
        cls.auditor = FairHousingAuditor(rules_path=rules_path)

    def test_clean_text(self):
        """Test that a compliant listing passes with a high score."""
        text = "Beautiful 3-bedroom home with a modern kitchen and spacious backyard. Close to schools and parks."
        report = self.auditor.scan_text(text)
        self.assertTrue(report['is_safe'])
        self.assertEqual(len(report['flagged_items']), 0)
        self.assertEqual(report['score'], 100)

    def test_explicit_bias_fail(self):
        """Test that 'no kids' flags a critical familial status violation."""
        text = "Cozy studio, perfect for professional. No kids allowed."
        report = self.auditor.scan_text(text)
        self.assertFalse(report['is_safe'])
        
        # Check for specific rule ID FHA-FAM-001
        found_ids = [item['id'] for item in report['flagged_items']]
        self.assertIn("FHA-FAM-001", found_ids)
        
        # Verify severity
        for item in report['flagged_items']:
            if item['id'] == "FHA-FAM-001":
                self.assertEqual(item['severity'], "Critical")

    def test_implicit_bias_warning(self):
        """Test that 'walking distance' triggers a warning."""
        text = "Newly renovated condo, walking distance to downtown shops."
        report = self.auditor.scan_text(text)
        
        # It might still be 'safe' depending on score threshold, 
        # but it should have a warning flag.
        found_ids = [item['id'] for item in report['flagged_items']]
        self.assertIn("FHA-HAND-003", found_ids)
        
        # Verify severity is Warning
        for item in report['flagged_items']:
            if item['id'] == "FHA-HAND-003":
                self.assertEqual(item['severity'], "Warning")

if __name__ == '__main__':
    unittest.main()
