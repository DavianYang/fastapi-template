from fastapi import APIRouter

router = APIRouter()

@router.get("", name="users:get-current-user")
async def get_current_user():
    return {
        "Key": "Hello World"
    }