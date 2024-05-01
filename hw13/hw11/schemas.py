from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    """
    Pydantic model representing contact data used for creating contacts.

    Attributes:
    - first_name (str): The first name of the contact (max length: 50).
    - last_name (str): The last name of the contact (max length: 50).
    - email (str): The email address of the contact (max length: 100).
    - phone (str): The phone number of the contact (max length: 100).
    - birthday (date): The birthday of the contact.
    """
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=100)
    birthday: date


class ContactResponse(ContactModel):
    """
    Pydantic model representing a contact response.

    Inherits from ContactModel.

    Attributes:
    - id (int): The unique identifier of the contact.
    """
    id: int

    class ConfigDict:
        from_attributes = True


class UserModel(BaseModel):
    """
    Pydantic model representing user data used for user creation.

    Attributes:
    - username (str): The username of the user (min length: 5, max length: 16).
    - email (str): The email address of the user.
    - password (str): The password of the user (min length: 6, max length: 10).
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Pydantic model representing user data retrieved from the database.

    Attributes:
    - id (int): The unique identifier of the user.
    - username (str): The username of the user.
    - email (str): The email address of the user.
    - created_at (datetime): The timestamp when the user was created.
    - avatar (str): The URL of the user's avatar.
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class ConfigDict:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Pydantic model representing the response after user creation.

    Attributes:
    - user (UserDb): The user data.
    - detail (str): Additional detail message (default: "User successfully created").
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Pydantic model representing the token response.

    Attributes:
    - access_token (str): The access token.
    - refresh_token (str): The refresh token.
    - token_type (str): The type of token (default: "bearer").
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Pydantic model representing the request for email confirmation.

    Attributes:
    - email (EmailStr): The email address for confirmation.
    """
    email: EmailStr
