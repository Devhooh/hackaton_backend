from core.extensions import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
