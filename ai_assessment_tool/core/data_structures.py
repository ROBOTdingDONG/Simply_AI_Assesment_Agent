class ProjectInput:
    def __init__(self, name, description, details=None):
        self.name = name
        self.description = description
        self.details = details if details is not None else {}

    def __repr__(self):
        return f"ProjectInput(name='{self.name}', description='{self.description}', details={self.details})"

class AssessmentOutput:
    def __init__(self, module_name, score, text_summary, details=None):
        self.module_name = module_name
        self.score = score  # Could be numeric, qualitative string, or a dict
        self.text_summary = text_summary
        self.details = details if details is not None else {}

    def __repr__(self):
        return f"AssessmentOutput(module_name='{self.module_name}', score={self.score}, summary='{self.text_summary}')"
