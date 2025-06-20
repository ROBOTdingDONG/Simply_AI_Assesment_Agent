from ai_assessment_tool.core.data_structures import ProjectInput, AssessmentOutput

def assess_survivability(project_input: ProjectInput) -> AssessmentOutput:
    '''
    Assesses the survivability of a project based on simple rules.
    '''
    score = 5  # Neutral base score
    summary_points = []

    # Example rule 1: Market size
    market_size = project_input.details.get('market_size', 'unknown').lower()
    if market_size == 'large':
        score += 2
        summary_points.append("Large market size is a positive factor.")
    elif market_size == 'medium':
        score += 1
        summary_points.append("Medium market size is noted.")
    elif market_size == 'small':
        score -= 1
        summary_points.append("Small market size could be a challenge.")
    else:
        summary_points.append("Market size information is unclear or not provided.")

    # Example rule 2: Competition
    competition = project_input.details.get('competition', 'unknown').lower()
    if competition == 'low':
        score += 2
        summary_points.append("Low competition is advantageous.")
    elif competition == 'medium':
        score += 0
        summary_points.append("Medium competition presents a moderate challenge.")
    elif competition == 'high':
        score -= 2
        summary_points.append("High competition is a significant risk factor.")
    else:
        summary_points.append("Competition level is unclear or not provided.")

    # Example rule 3: Team experience (very simplistic)
    team_experience = project_input.details.get('team_experience_years', 0)
    if team_experience > 5:
        score += 1
        summary_points.append("Experienced team is a plus.")
    elif team_experience < 1 and team_experience > 0:
        score -=1
        summary_points.append("Limited team experience noted.")
    elif team_experience == 0:
        summary_points.append("Team experience not specified or is zero.")


    # Normalize score to be within 0-10
    score = max(0, min(10, score))

    summary = "Survivability Assessment: " + " ".join(summary_points)

    return AssessmentOutput(
        module_name="Survivability",
        score=score,
        text_summary=summary,
        details={'rules_considered': ['market_size', 'competition', 'team_experience']}
    )
