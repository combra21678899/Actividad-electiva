import re
import uuid

def validate_uuid(value):
    """Valida que un string sea un UUID válido"""
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def validate_email(email):
    """Valida que el email tenga formato correcto"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
