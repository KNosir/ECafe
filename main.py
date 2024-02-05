from sqlalchemy import engine
from flask import Flask, jsonify
from sqlalchemy.orm import Session
from routes import app as routes_app
from flask_jwt_extended import JWTManager
from datetime import timedelta

# from models import Base

# создаем таблицы
# Base.metadata.create_all(bind=engine)

app = Flask(__name__)



app.config['JWT_SECRET_KEY'] = 'CodiPentagon'  
app.config['JWT_ALGORITHM'] = 'HS256'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)

jwt =JWTManager(app)

app.register_blueprint(routes_app)

if __name__ == '__main__':
    app.run(debug=True)
