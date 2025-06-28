from app.models.user import User
from core.extensions import db

class UserService:

    @staticmethod
    def create_user(user):
        db.session.add(user)
        db.session.commit()
        return user


    @staticmethod
    def get_all_users_paginated(page=1, per_page=10):
        pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }
