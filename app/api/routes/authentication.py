from fastapi import APIRouter
from fastapi import Body, Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.models.schemas.users import UserInResponse, UserInLogin, UserInCreate
from app.services.users import UserService

router = APIRouter()

@router.post('/login', response_model=UserInResponse, name='auth:login')
async def login(
    user_login: UserInLogin
):
    pass


@router.post(
    '/register', # demo routes -> removes "register"
    status_code=HTTP_201_CREATED,
    # response_model=UserInResponse
    name="auth:register"
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    user_service: UserService = Depends(UserService)
):
    user = await user_service.create_user(**user_create.dict())
    
    return user
    