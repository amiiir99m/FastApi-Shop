from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = 522
        self.detail = "user not found!"


class UserAlreadyExists(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "user alreadt exists!"


class UsernameOrPasswordIncorrect(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "username or password is incorrect!"


class CategoryAlreadyExists(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "category alreadt exists!"


class CategoryNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = 522
        self.detail = "CategoryNotFound!"


class AccessDenied(HTTPException):
    def __init__(self) -> None:
        self.status_code = 522
        self.detail = "AccessDenied!"


class ProductNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = 522
        self.detail = "ProductNotFound!"


class ImageNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = 522
        self.detail = "ProductNotFound!"
