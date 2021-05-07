from app.errors.database import EntityDoesNotExist
from app.services.users import UserService


async def check_username_is_taken(service: UserService, name: str) -> bool:
    try:
        await service.get_user_by_name(name=name)
    except EntityDoesNotExist:
        return False

    return True


async def check_email_is_taken(service: UserService, email: str) -> bool:
    try:
        await service.get_user_by_email(email=email)
    except EntityDoesNotExist:
        return False
    return True
