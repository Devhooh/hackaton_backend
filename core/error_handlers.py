from flask import jsonify
from app.utils.response import response
from werkzeug.exceptions import HTTPException
import traceback

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return response(
            status_code=e.code,
            message=str(e),
            error=e.name
        )

    @app.errorhandler(400)
    def handle_bad_request(e):
        return response(400, "Solicitud inválida", error=str(e))

    @app.errorhandler(404)
    def handle_not_found(e):
        return response(404, "Recurso no encontrado", error=str(e))

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        # Opcional: imprimir traceback para debug
        traceback.print_exc()
        return response(500, "Error interno del servidor", error=str(e))
