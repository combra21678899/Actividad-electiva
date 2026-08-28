from src.repositories.blacklist_repository import BlacklistRepository
from src.utils.validation import validate_uuid
import re

class BlacklistService:
    
    @staticmethod
    def validate_email(email):
        """Valida que el email tenga formato correcto"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def add_email(email, app_id, reason=None):
        """Agrega un email a la lista negra con validaciones"""
        # Validar email
        if not BlacklistService.validate_email(email):
            return None, {"error": "Formato de email inválido"}, 400
        
        # Validar app_id (UUID)
        if not validate_uuid(app_id):
            return None, {"error": "app_id debe ser un UUID válido"}, 400
        
        # Validar reason (máximo 255 caracteres)
        if reason and len(reason) > 255:
            return None, {"error": "El motivo no puede exceder 255 caracteres"}, 400
        
        # Agregar a la base de datos
        result, error = BlacklistRepository.add_email(email, app_id, reason)
        
        if error:
            return None, {"error": error}, 400
        
        return result.to_dict(), None, 201
    
    @staticmethod
    def check_email(email):
        """Consulta si un email está en la lista negra"""
        # Validar email
        if not BlacklistService.validate_email(email):
            return None, {"error": "Formato de email inválido"}, 400
        
        # Buscar en la base de datos
        result = BlacklistRepository.get_by_email(email)
        
        if result:
            return {
                "email": email,
                "is_blacklisted": True,
                "reason": result.reason,
                "app_id": result.app_id,
                "created_at": result.created_at.isoformat() if result.created_at else None
            }, None, 200
        else:
            return {
                "email": email,
                "is_blacklisted": False,
                "reason": None
            }, None, 200
