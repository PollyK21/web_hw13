from libgravatar import Gravatar
from sqlalchemy.orm import Session
from hw11.database.models import User
from hw11.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by email from the database.

    Parameters:
    - email (str): The email address of the user to retrieve.
    - db (Session): The database session.

    Returns:
    - User: The retrieved user.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user in the database.

    Parameters:
    - body (UserModel): The user data.
    - db (Session): The database session.

    Returns:
    - User: The created user.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update the refresh token for a user.

    Parameters:
    - user (User): The user whose token is being updated.
    - token (str | None): The new refresh token, or None if no token is provided.
    - db (Session): The database session.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Mark a user's email as confirmed.

    Parameters:
    - email (str): The email address of the user.
    - db (Session): The database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Update a user's avatar URL.

    Parameters:
    - email (str): The email address of the user.
    - url (str): The new avatar URL.
    - db (Session): The database session.

    Returns:
    - User: The updated user.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
