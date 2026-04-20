class ComplianceChecker:
    """Checks if the calculated RA value complies with IRC standards."""

    def __init__(self):
        print("ComplianceChecker initialized.")
        self.irc_thresholds = {
            "road_marking": {"danger": 100, "warning": 150},
            "sign_board": {"danger": 250, "warning": 375},
            "road_stud": {"danger": 150, "warning": 225}
        }

    def check_compliance(self, object_type, ra_value):
        """Checks the RA value against IRC standards for the given object type.

        Args:
            object_type (str): Type of the object (e.g., "road_marking").
            ra_value (float): Calculated RA value.

        Returns:
            str: "DANGER", "WARNING", or "SAFE".
        """
        thresholds = self.irc_thresholds.get(object_type)
        if not thresholds:
            return "UNKNOWN_TYPE"

        if ra_value < thresholds["danger"]:
            return "DANGER"
        elif ra_value < thresholds["warning"]:
            return "WARNING"
        else:
            return "SAFE"
