import unittest
import sys
import os

# Adjust path to import from parent directory's modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_assessment_tool.core.data_structures import ProjectInput
from ai_assessment_tool.assessments.survivability import assess_survivability

class TestSurvivabilityAssessment(unittest.TestCase):

    def test_high_survivability_scenario(self):
        project = ProjectInput(
            name="Test Project Alpha",
            description="A promising venture.",
            details={'market_size': 'Large', 'competition': 'Low', 'team_experience_years': 6}
        )
        assessment = assess_survivability(project)
        self.assertEqual(assessment.module_name, "Survivability")
        self.assertGreaterEqual(assessment.score, 7) # 5 + 2 (market) + 2 (comp) + 1 (exp) = 10
        self.assertIn("Large market size", assessment.text_summary)
        self.assertIn("Low competition", assessment.text_summary)
        self.assertIn("Experienced team", assessment.text_summary)

    def test_low_survivability_scenario(self):
        project = ProjectInput(
            name="Test Project Beta",
            description="A risky business.",
            details={'market_size': 'Small', 'competition': 'High', 'team_experience_years': 0.5}
        )
        assessment = assess_survivability(project)
        self.assertEqual(assessment.module_name, "Survivability")
        self.assertLessEqual(assessment.score, 3) # 5 - 1 (market) - 2 (comp) - 1 (exp) = 1
        self.assertIn("Small market size", assessment.text_summary)
        self.assertIn("High competition", assessment.text_summary)
        self.assertIn("Limited team experience", assessment.text_summary)

    def test_neutral_survivability_scenario(self):
        project = ProjectInput(
            name="Test Project Gamma",
            description="An average idea.",
            details={'market_size': 'Medium', 'competition': 'Medium', 'team_experience_years': 3}
        )
        assessment = assess_survivability(project)
        self.assertEqual(assessment.module_name, "Survivability")
        # Base 5 + 1 (market) + 0 (comp) + 0 (exp for 3 years) = 6
        self.assertTrue(4 <= assessment.score <= 7)
        self.assertIn("Medium market size", assessment.text_summary)
        self.assertIn("Medium competition", assessment.text_summary)

    def test_unknown_details(self):
        project = ProjectInput(
            name="Test Project Delta",
            description="Not much info provided."
            # No details provided
        )
        assessment = assess_survivability(project)
        self.assertEqual(assessment.module_name, "Survivability")
        self.assertTrue(3 <= assessment.score <= 7) # Base 5, other factors are neutral
        self.assertIn("Market size information is unclear", assessment.text_summary)
        self.assertIn("Competition level is unclear", assessment.text_summary)
        self.assertIn("Team experience not specified", assessment.text_summary)

if __name__ == "__main__":
    unittest.main()
