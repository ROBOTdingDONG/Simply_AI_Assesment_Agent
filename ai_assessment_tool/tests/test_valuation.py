import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_assessment_tool.core.data_structures import ProjectInput
from ai_assessment_tool.assessments.valuation import assess_valuation

class TestValuationAssessment(unittest.TestCase):

    def test_high_potential_valuation(self):
        project = ProjectInput(
            name="Growth Rocket Inc.",
            description="To the moon!",
            details={
                'initial_investment_usd': 1500000,
                'revenue_stage': 'growth',
                'team_size': 25
            }
        )
        assessment = assess_valuation(project)
        self.assertEqual(assessment.module_name, "Valuation")
        # Score: 3 (invest) + 4 (rev) + 2 (team) = 9
        self.assertEqual(assessment.score, 9)
        self.assertIn("Growth Stage Potential - Strong Outlook", assessment.details['qualitative_label'])
        self.assertIn("Significant initial investment", assessment.text_summary)
        self.assertIn("growth stage", assessment.text_summary)
        self.assertIn("Large team size", assessment.text_summary)

    def test_early_stage_valuation(self):
        project = ProjectInput(
            name="Seedling Co.",
            description="Just starting out.",
            details={
                'initial_investment_usd': 50000, # Score +1
                'revenue_stage': 'Pre-Revenue', # Score +1, label "Pre-Revenue / Seed Stage"
                'team_size': 3 # Label "Small team"
            }
        )
        assessment = assess_valuation(project)
        self.assertEqual(assessment.module_name, "Valuation")
        # Score: 1 (invest) + 1 (rev) + 0 (team) = 2
        self.assertEqual(assessment.score, 2)
        self.assertIn("Pre-Revenue / Seed Stage - Speculative Outlook", assessment.details['qualitative_label'])
        self.assertIn("Initial investment of $50,000", assessment.text_summary) # Test formatting
        self.assertIn("pre-revenue", assessment.text_summary)
        self.assertIn("Small team size", assessment.text_summary)

    def test_moderate_valuation(self):
        project = ProjectInput(
            name="Steady Progress LLC",
            description="Making headway.",
            details={
                'initial_investment_usd': 200000, # Score +2
                'revenue_stage': 'early-revenue', # Score +2, label "Early Revenue Stage"
                'team_size': 10 # Score +1
            }
        )
        assessment = assess_valuation(project)
        self.assertEqual(assessment.module_name, "Valuation")
        # Score: 2 (invest) + 2 (rev) + 1 (team) = 5
        self.assertEqual(assessment.score, 5)
        self.assertIn("Early Revenue Stage - Moderate Outlook", assessment.details['qualitative_label'])
        self.assertIn("Moderate initial investment", assessment.text_summary)
        self.assertIn("Early revenue", assessment.text_summary)
        self.assertIn("Moderate team size", assessment.text_summary)

    def test_unknown_details_valuation(self):
        project = ProjectInput(
            name="Mystery Corp",
            description="Who knows?"
            # No details
        )
        assessment = assess_valuation(project)
        self.assertEqual(assessment.module_name, "Valuation")
        # Score: 0 (invest) + 0 (rev) + 0 (team) = 0
        self.assertEqual(assessment.score, 0)
        self.assertIn("Unknown Revenue Stage - Speculative Outlook", assessment.details['qualitative_label'])
        self.assertIn("No significant initial investment", assessment.text_summary)
        self.assertIn("Revenue stage is unclear", assessment.text_summary)
        self.assertIn("Small team size (0)", assessment.text_summary) # team_size defaults to 0

if __name__ == "__main__":
    unittest.main()
