from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)