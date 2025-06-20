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
        self.score = score
        self.text_summary = text_summary
        self.details = details if details is not None else {}

    def __repr__(self):
        return f"AssessmentOutput(module_name='{self.module_name}', score={self.score}, summary='{self.text_summary}')"

    # Helper for session serialization if needed, though vars() might be enough for simple cases
    def to_dict(self):
        return vars(self)

    # @classmethod
    # def from_dict(cls, data):
    #     return cls(**data)
