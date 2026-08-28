from flask import Flask
from flask_restful import Api
from src.db.database import db, ma, jwt, init_db
from src.routes.blacklist_router import AddEmailResource, CheckEmailResource
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blacklist.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    
    # Inicializar extensiones
    init_db(app)
    
    # Configurar rutas
    api = Api(app)
    api.add_resource(AddEmailResource, '/api/blacklist')
    api.add_resource(CheckEmailResource, '/api/blacklist/check')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)