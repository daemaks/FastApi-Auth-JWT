import os as _os

import dotenv as _dotenv
import sqlalchemy.orm as _orm
import email_validator as _email_validator
import fastapi as _fastapi
import fastapi.security as _security
import passlib.hash as _hash
import jwt as _jwt

import database as _database
import models as _models
import schemas as _schemas

_dotenv.load_dotenv()

_JWT_SECRET = _os.environ['JWT_SECRET']

oauth2schema = _security.OAuth2PasswordBearer("/api/token")


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db=_orm.Session):
    try:
        valid = _email_validator.validate_email(email=user.email)
        email = valid.email
    except _email_validator.EmailNotValidError:
        raise _fastapi.HTTPException(
            status_code=404, detail="Enter a valid email"
        )
    hashed_password = _hash.bcrypt.hash(user.password)
    user_obj = _models.User(email=email, hashed_password=hashed_password)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: _models.User):
    user_schema_obj = _schemas.User.from_orm(user)

    user_dict = user_schema_obj.dict()
    del user_dict["created_at"]

    token = _jwt.encode(user_dict, _JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def auth_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(password=password):
        return False

    return user


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid email or password"
        )

    return _schemas.User.from_orm(user)


async def create_post(
    user: _schemas.User, db: _orm.Session, post: _schemas.PostCreate
):
    post = _models.Post(**post.dict(), owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)

    return _schemas.Post.from_orm(post)


async def get_user_posts(user: _schemas.User, db: _orm.Session):
    posts = db.query(_models.Post).filter_by(owner_id=user.id)
    return list(map(_schemas.Post.from_orm, posts))
