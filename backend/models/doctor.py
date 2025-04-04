class Doctor:

    def __init__(
        self,
        code: str,
        name: str,
        seniority_id: int,
        shift_count: int,
        shift_areas: list,
        shift_duration: int,
        optional_leaves: list = None,
        mandatory_leaves: list = None,
    ):
        self.code = code
        self.name = name
        self.seniority_id = seniority_id
        self.shift_count = shift_count
        self.shift_areas = shift_areas
        self.shift_duration = shift_duration
        self.optional_leaves = optional_leaves or []
        self.mandatory_leaves = mandatory_leaves or []

    def __repr__(self):
        return (
            f"Doctor(code={self.code}, name={self.name}, seniority_id={self.seniority_id}, "
            f"shift_count={self.shift_count}, shift_areas={self.shift_areas}, shift_duration={self.shift_duration})"
        )

