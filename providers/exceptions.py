class ProviderException(Exception):
    """
    A custom exception class for provider-related errors.
    """

    def __init__(self, message: str):
        super().__init__(message)

    def __str__(self):
        return f"ProviderException: {self.args[0]}"
