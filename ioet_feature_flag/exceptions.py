class ToggleNotFoundError(Exception):
    """
    Exception raised when a toggle is not found or registered
    """


class InvalidDecisionFunction(Exception):
    """
    Exception raised when a invalid decision function is detected
    """


class ToggleEnvironmentError(Exception):
    """
    Exception raised when the toggle environmnet is not specified
    """


class InvalidToggleType(Exception):
    """
    Exception raised when the toggle type is not valid
    """


class MissingToggleAttributes(Exception):
    """
    Exception raised when a specific toggle type is missing attributes.
    For example, when the toggle type "cutover" is missing the "date" attribute.
    """


class InvalidToggleAttribute(Exception):
    """
    Exception raised when a specific toggle attribute not valid.
    For example, when the toggle attribute "date" is not a valid date.
    """


class MissingToggleContext(Exception):
    """
    Exception raised when a toggle type needs a toggle context, but it was not provided.
    For example, when the toggle type "pilot_users" is called without a context to know the user.
    """
