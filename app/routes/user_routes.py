from flask import Blueprint, request
from flasgger import swag_from
from marshmallow import ValidationError
from app.schemas.user_schema import UserSchema
from app.services.user_service import UserService
from app.utils.response import response

user_bp = Blueprint('user_bp', __name__, url_prefix="/users")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Usuarios'],
    'summary': 'Crear un nuevo usuario',
    'description': 'Crea un usuario a partir de los datos enviados.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'johndoe'},
                    'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'}
                },
                'required': ['username', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'statusCode': {'type': 'integer', 'example': 201},
                    'message': {'type': 'string', 'example': 'Usuario creado exitosamente'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'username': {'type': 'string', 'example': 'johndoe'},
                            'email': {'type': 'string', 'example': 'john@example.com'},
                            'created_at': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Error de validación',
            'schema': {
                'type': 'object',
                'properties': {
                    'statusCode': {'type': 'integer', 'example': 400},
                    'message': {'type': 'string', 'example': 'Datos inválidos'},
                    'error': {'type': 'object', 'example': {"email": ["Not a valid email address."]}}
                }
            }
        },
        500: {
            'description': 'Error inesperado',
            'schema': {
                'type': 'object',
                'properties': {
                    'statusCode': {'type': 'integer', 'example': 500},
                    'message': {'type': 'string', 'example': 'Error inesperado'},
                    'error': {'type': 'string', 'example': 'Internal server error'}
                }
            }
        }
    }
})
def create_user():
    """
    Crear un nuevo usuario
    """
    try:
        data = request.get_json()
        validated_data = user_schema.load(data)  # Valida y deserializa input
        user = UserService.create_user(validated_data)
        user_data = user_schema.dump(user)  # Serializa respuesta
        return response(201, "Usuario creado exitosamente", data=user_data)
    except ValidationError as err:
        return response(400, "Datos inválidos", error=err.messages)
    except Exception as e:
        return response(500, "Error inesperado", error=str(e))


@user_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'summary': 'Listar usuarios con paginación',
    'description': 'Obtiene usuarios paginados. Usa query params: ?page=1&per_page=10',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'description': 'Número de página'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Cantidad de usuarios por página'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuarios paginados correctamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'statusCode': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'Usuarios obtenidos exitosamente'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'username': {'type': 'string', 'example': 'johndoe'},
                                'email': {'type': 'string', 'example': 'john@example.com'},
                                'created_at': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    },
                    'countData': {'type': 'integer', 'example': 100}
                }
            }
        },
        500: {
            'description': 'Error al obtener usuarios',
            'schema': {
                'type': 'object',
                'properties': {
                    'statusCode': {'type': 'integer', 'example': 500},
                    'message': {'type': 'string', 'example': 'Error al obtener usuarios'},
                    'error': {'type': 'string', 'example': 'Internal server error'}
                }
            }
        }
    }
})
def get_users():
    """
    Obtener usuarios paginados
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        result = UserService.get_all_users_paginated(page=page, per_page=per_page)
        users_data = users_schema.dump(result["items"])
        total = result["total"]

        return response(200, "Usuarios obtenidos exitosamente", data=users_data, count_data=total)

    except Exception as e:
        return response(500, "Error al obtener usuarios", error=str(e))
