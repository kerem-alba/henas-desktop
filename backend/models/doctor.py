class Doctor:

    def __init__(
        self,
        code: str,
        name: str,
        seniority_id: int,
        shift_count: int,
        shift_areas: list,
        optional_leaves: list = None,
        mandatory_leaves: list = None,
    ):
        self.code = code
        self.name = name
        self.seniority_id = seniority_id
        self.shift_count = shift_count
        self.shift_areas = shift_areas
        self.optional_leaves = optional_leaves or []
        self.mandatory_leaves = mandatory_leaves or []

    def __repr__(self):
        return (
            f"Doctor(code={self.code}, name={self.name}, seniority={self.seniority}, "
            f"shift_count={self.shift_count}, shift_areas={self.shift_areas})"
        )
