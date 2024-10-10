from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .schemas import (
    UserModel,
    UserCreateModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
    PasswordResetModel,
    PasswordResetConfirmModel,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from .utils import (
    create_access_token,
    verify_password,
    generate_password_hash,
    create_url_safe_token,
    decode_url_safe_token,
)
from datetime import timedelta, datetime
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken
from src.mail import mail, create_message
from src.config import Config
from src.errors import UserNotFound
from src.db.main import get_session
from src.celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin"])

REFRESH_TOKEN_EXPIRY = 30


@auth_router.post("/send_email")
async def send_mail(emails: EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to our app</h1>"
    subject = "Welcome to our app"

    send_email.delay(emails, subject, html)

    return {"message": "Email sent successfully"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})
    link = f"{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html = f"""
    <h1>Verify your email</h1>
    <p>Please click on the following link to verify your email address: <a href="{link}"></a></p>
    """
    emails = [email]
    subject = "Verify your email"

    send_email.delay(emails, subject, html)

    return {
        "message": "User created successfully. Please verify your email address",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(session, user_email)

        if not user:
            raise UserNotFound()

        await user_service.update_user(session, user, {"is_verified": True})

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Invalid token"}, status_code=status.HTTP_401_UNAUTHORIZED
    )


@auth_router.post("/login", response_model=UserModel)
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(session, email)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "id": user.id,
                    "email": user.email,
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.post("/reset-password-request")
async def reset_password(email_data: PasswordResetModel):
    email = email_data.email

    token = create_url_safe_token({"email": email})
    link = f"{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
    html_message = f"""
    <h1>Reset your password</h1>
    <p>Please click on the following link to reset your password: <a href="{link}"></a></p>
    """

    message = create_message(
        recipients=[email], subject="Reset your password", body=html_message
    )

    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    new_password = passwords.new_password
    confirm_new_password = passwords.confirm_new_password
    if new_password != confirm_new_password:
        raise HTTPException(
            detail="Passwords do not match",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(session, user_email)

        if not user:
            raise UserNotFound()

        password_hash = generate_password_hash(new_password)
        await user_service.update_user(session, user, {"password_hash": password_hash})

        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during password reset"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
