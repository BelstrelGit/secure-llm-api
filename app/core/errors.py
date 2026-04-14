class AppError(Exception):
    def __init__(self, detail: str = "application error"):
        self.detail = detail


class ConflictError(AppError):
    def __init__(self, detail: str = "resource already exists"):
        super().__init__(detail)


class UnauthorizedError(AppError):
    def __init__(self, detail: str = "unauthorized"):
        super().__init__(detail)


class ForbiddenError(AppError):
    def __init__(self, detail: str = "forbidden"):
        super().__init__(detail)


class NotFoundError(AppError):
    def __init__(self, detail: str = "not found"):
        super().__init__(detail)


class ExternalServiceError(AppError):
    def __init__(self, detail: str = "external service error"):
        super().__init__(detail)
