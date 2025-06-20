import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_assessment_tool.core.data_structures import ProjectInput
from ai_assessment_tool.assessments.popularity import assess_popularity

class TestPopularityAssessmentPlaceholder(unittest.TestCase):

    def test_placeholder_output(self):
        project = ProjectInput(
            name="Test Project Pop",
            description="Some description."
        )
        assessment = assess_popularity(project)
        self.assertEqual(assessment.module_name, "Popularity")
        self.assertEqual(assessment.score, "Not Implemented")
        self.assertIn("not yet implemented", assessment.text_summary.lower())
        self.assertEqual(assessment.details['status'], 'placeholder')

if __name__ == "__main__":
    unittest.main()
