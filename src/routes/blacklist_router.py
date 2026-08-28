

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.blacklist_service import BlacklistService

class AddEmailResource(Resource):
    @jwt_required()
    def post(self):
        """Endpoint para agregar un email a la lista negra"""
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='El email es requerido')
        parser.add_argument('app_id', required=True, help='El app_id es requerido')
        parser.add_argument('reason', required=False)
        args = parser.parse_args()
        
        # Obtener usuario autenticado (para auditoría)
        current_user = get_jwt_identity()
        print(f"Usuario {current_user} agregando email: {args['email']}")
        
        # Llamar al servicio
        result, error, status_code = BlacklistService.add_email(
            args['email'],
            args['app_id'],
            args.get('reason')
        )
        
        if error:
            return error, status_code
        
        return result, status_code

class CheckEmailResource(Resource):
    @jwt_required()
    def get(self):
        """Endpoint para consultar si un email está en la lista negra"""
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='El email es requerido')
        args = parser.parse_args()
        
        result, error, status_code = BlacklistService.check_email(args['email'])
        
        if error:
            return error, status_code
        
        return result, status_code