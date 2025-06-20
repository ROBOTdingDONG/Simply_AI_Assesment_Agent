import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_assessment_tool.core.data_structures import AssessmentOutput
from ai_assessment_tool.recommendation_engine import generate_recommendations

class TestRecommendationEngine(unittest.TestCase):

    def test_low_survivability_recommendation(self):
        assessments = [
            AssessmentOutput("Survivability", 2, "Low survivability due to high competition.")
        ]
        recs = generate_recommendations(assessments)
        self.assertTrue(any("Critical review of project viability" in r for r in recs))

    def test_high_valuation_recommendation(self):
        assessments = [
            AssessmentOutput("Valuation", 9, "Strong growth prospects.", {'qualitative_label': 'Growth Stage - Strong Outlook'})
        ]
        recs = generate_recommendations(assessments)
        self.assertTrue(any("Leverage this strong position" in r for r in recs))

    def test_mixed_scores_recommendation(self):
        assessments = [
            AssessmentOutput("Survivability", 8, "Very robust."),
            AssessmentOutput("Valuation", 3, "Needs better monetization.", {'qualitative_label': 'Pre-Revenue - Speculative Outlook'})
        ]
        recs = generate_recommendations(assessments)
        self.assertTrue(any("High survivability but lower valuation confidence" in r for r in recs))
        self.assertTrue(any("Score is high. Continue to monitor risks" in r for r in recs)) # Survivability rec
        self.assertTrue(any("Potential/Confidence score (3) is low." in r for r in recs)) # Valuation rec


    def test_with_placeholder_module(self):
        assessments = [
            AssessmentOutput("Survivability", 7, "Good outlook."),
            AssessmentOutput("Popularity", "Not Implemented", "To be done.")
        ]
        recs = generate_recommendations(assessments)
        self.assertTrue(any("Score is high. Continue to monitor risks" in r for r in recs)) # Survivability rec
        self.assertTrue(any("Note: The 'Popularity' module is not yet implemented." in r for r in recs))

    def test_only_placeholder_modules(self):
        assessments = [
            AssessmentOutput("Popularity", "Not Implemented", "To be done."),
            AssessmentOutput("Property Assessment", "Not Implemented", "Later.")
        ]
        recs = generate_recommendations(assessments)
        self.assertTrue(any("No specific recommendations generated" in r for r in recs))
        self.assertTrue(any("Note: The 'Popularity' module is not yet implemented." in r for r in recs))
        self.assertTrue(any("Note: The 'Property Assessment' module is not yet implemented." in r for r in recs))

    def test_no_assessments(self):
        assessments = []
        recs = generate_recommendations(assessments)
        self.assertTrue(any("No specific recommendations generated" in r for r in recs))

if __name__ == "__main__":
    unittest.main()
