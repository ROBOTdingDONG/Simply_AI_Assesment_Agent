import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_assessment_tool.core.data_structures import ProjectInput
from ai_assessment_tool.assessments.business_assessment import assess_business

class TestBusinessAssessmentPlaceholder(unittest.TestCase):

    def test_placeholder_output(self):
        project = ProjectInput(
            name="Test Project Biz",
            description="Some description about business strategy."
        )
        assessment = assess_business(project)
        self.assertEqual(assessment.module_name, "Business Assessment")
        self.assertEqual(assessment.score, "Not Implemented")
        self.assertIn("not yet implemented", assessment.text_summary.lower())
        self.assertEqual(assessment.details['status'], 'placeholder')

if __name__ == "__main__":
    unittest.main()
