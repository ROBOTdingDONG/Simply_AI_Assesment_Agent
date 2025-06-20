from typing import List
from ai_assessment_tool.core.data_structures import AssessmentOutput

def generate_recommendations(assessments: List[AssessmentOutput]) -> List[str]:
    '''
    Generates basic recommendations based on a list of assessment outputs.
    '''
    recommendations = []
    scores = {}
    summaries = {}

    for assessment in assessments:
        if assessment: # Ensure assessment is not None
            scores[assessment.module_name] = assessment.score
            summaries[assessment.module_name] = assessment.text_summary

    # --- Survivability Based Recommendations ---
    survivability_score = scores.get("Survivability")
    if survivability_score is not None: # Check if it was implemented and scored
        if not isinstance(survivability_score, (int, float)):
            recommendations.append("Recommendation: Survivability score is not numeric, cannot generate specific advice based on it yet.")
        elif survivability_score < 4:
            recommendations.append("Recommendation (Survivability): Score is low. Critical review of project viability, market fit, and competitive landscape is strongly advised. Identify and mitigate key risks.")
        elif survivability_score < 7:
            recommendations.append("Recommendation (Survivability): Score is moderate. Focus on strengthening areas of weakness and solidifying competitive advantages.")
        else:
            recommendations.append("Recommendation (Survivability): Score is high. Continue to monitor risks and build on current strengths.")

    # --- Valuation Based Recommendations ---
    valuation_score = scores.get("Valuation")
    valuation_summary = summaries.get("Valuation", "")
    if valuation_score is not None: # Check if it was implemented and scored
        if not isinstance(valuation_score, (int, float)):
            recommendations.append("Recommendation: Valuation score is not numeric, cannot generate specific advice based on it yet.")
        elif valuation_score < 4:
            recommendations.append(f"Recommendation (Valuation): Potential/Confidence score ({valuation_score}) is low. Focus on fundamentals, demonstrating traction, or clarifying the business model to improve valuation outlook. {valuation_summary}")
        elif valuation_score < 7:
            recommendations.append(f"Recommendation (Valuation): Potential/Confidence score ({valuation_score}) is moderate. Explore avenues to enhance value proposition and market position. {valuation_summary}")
        else:
            recommendations.append(f"Recommendation (Valuation): Potential/Confidence score ({valuation_score}) is high. Leverage this strong position for strategic growth or funding opportunities. {valuation_summary}")

    # --- Cross-module Recommendation Example ---
    if survivability_score is not None and valuation_score is not None and        isinstance(survivability_score, (int, float)) and isinstance(valuation_score, (int, float)):
        if survivability_score >= 7 and valuation_score < 4:
            recommendations.append("Recommendation (Cross-Analysis): High survivability but lower valuation confidence suggests the project is fundamentally sound but may need to better articulate its financial potential or explore monetization strategies.")
        elif survivability_score < 4 and valuation_score >= 7:
            recommendations.append("Recommendation (Cross-Analysis): Higher valuation confidence than survivability score is unusual. Ensure that the valuation isn't overly optimistic given potential survivability risks. Double-check risk factors.")


    if not recommendations:
        recommendations.append("No specific recommendations generated based on available implemented modules. Ensure assessment modules provide numeric scores for detailed advice.")

    # Add note about placeholder modules
    for assessment in assessments:
        if assessment and assessment.score == "Not Implemented":
            recommendations.append(f"Note: The '{assessment.module_name}' module is not yet implemented. Its insights will be incorporated into recommendations once available.")

    return recommendations
