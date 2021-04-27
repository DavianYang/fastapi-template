from app.adapter.repositories.base import BaseRepository
from app.adapter.orms import orm
from app.domain.user import User

class UserRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
        
    def _create(self, user: User):
        self.session.add(user)
        
        