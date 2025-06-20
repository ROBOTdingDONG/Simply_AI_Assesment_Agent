from ai_assessment_tool.core.data_structures import ProjectInput, AssessmentOutput

def assess_valuation(project_input: ProjectInput) -> AssessmentOutput:
    '''
    Provides a very basic, qualitative valuation assessment.
    '''
    score = 0  # Base score representing potential/confidence
    qualitative_valuation = "Not Yet Assessed"
    summary_points = []

    initial_investment = project_input.details.get('initial_investment_usd', 0)
    revenue_stage = str(project_input.details.get('revenue_stage', 'unknown')).lower()
    team_size = project_input.details.get('team_size', 0)

    # Rule for initial investment
    if initial_investment > 1000000: # > M
        score += 3
        summary_points.append(f"Significant initial investment of ${initial_investment:,.0f} noted.")
    elif initial_investment > 100000: # > 00k
        score += 2
        summary_points.append(f"Moderate initial investment of ${initial_investment:,.0f}.")
    elif initial_investment > 0:
        score += 1
        summary_points.append(f"Initial investment of ${initial_investment:,.0f} is a starting point.")
    else:
        summary_points.append("No significant initial investment specified.")

    # Rule for revenue stage
    if revenue_stage == 'growth':
        score += 4
        qualitative_valuation = "Growth Stage Potential"
        summary_points.append("Project is in growth stage, indicating market traction.")
    elif revenue_stage == 'early-revenue':
        score += 2
        qualitative_valuation = "Early Revenue Stage"
        summary_points.append("Early revenue is a positive sign.")
    elif revenue_stage == 'pre-revenue':
        score += 1
        qualitative_valuation = "Pre-Revenue / Seed Stage"
        summary_points.append("Project is pre-revenue; valuation is speculative.")
    else:
        qualitative_valuation = "Unknown Revenue Stage"
        summary_points.append("Revenue stage is unclear.")

    # Rule for team size (very crude)
    if team_size > 20:
        score += 2
        summary_points.append(f"Large team size ({team_size}) may indicate scaling.")
    elif team_size > 5:
        score += 1
        summary_points.append(f"Moderate team size ({team_size}).")
    else:
        summary_points.append(f"Small team size ({team_size}).")

    # Normalize score
    score = max(0, min(10, score))

    if score > 7:
        qualitative_valuation += " - Strong Outlook"
    elif score > 4:
        qualitative_valuation += " - Moderate Outlook"
    else:
        qualitative_valuation += " - Speculative Outlook"


    summary = f"Valuation Assessment ({qualitative_valuation}): " + " ".join(summary_points)

    return AssessmentOutput(
        module_name="Valuation",
        score=score, # Confidence/Potential score
        text_summary=summary,
        details={
            'qualitative_label': qualitative_valuation,
            'rules_considered': ['initial_investment_usd', 'revenue_stage', 'team_size']
        }
    )
