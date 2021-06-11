# from app.models.domain.users import UserInDB


# def test_user_in_db():
#     password = "1234567890"

#     user = UserInDB(
#         name="johndoe",
#         email="johndoe@gmail.com",
#         photos="https://unsplash.com/photos/7YVZYZeITc8",
#         is_active=True,
#         is_superuser=False,
#     )
#     user.hash_password(password)

#     assert user.name == "johndoe"
#     assert user.email == "johndoe@gmail.com"
