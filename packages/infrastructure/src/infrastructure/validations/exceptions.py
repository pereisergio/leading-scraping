class InfrastructureError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @classmethod
    def when(cls, *, has_error: bool, message: str) -> None:
        if has_error:
            raise cls(message)
