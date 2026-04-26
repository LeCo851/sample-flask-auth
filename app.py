from flask import Flask, request,jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'message': 'Acesso negado. Faça login para continuar.'}), 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    
    if not data:
        return jsonify({'message': 'Nenhum dado JSON foi enviado na requisição'}), 400
        
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        user = User.query.filter_by(username= username).first()
        
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message': 'Login bem-sucedido'})
    
    return jsonify({'message': 'credenciais inválidas'}), 400

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout bem-sucedido'})


@app.route("/user", methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return jsonify({'message': 'Nenhum dado JSON foi enviado na requisição'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso'})
    
    return jsonify({'message': 'Dados inválidos'}), 400

@app.route("/user/<int:user_id>", methods=['GET'])
@login_required
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username})
    return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route("/user/<int:user_id>", methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.json
    if not data:
        return jsonify({'message': 'Nenhum dado JSON foi enviado na requisição'}), 400
    
    user = db.session.get(User, user_id)
    if user and data.get('password'):

        user.password = data.get('password')
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} atualizado com sucesso"})
    
    return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route("/user/<int:user_id>", methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    
    if user_id == current_user.id:
        return jsonify({'message':'Deleção não permitida para o usuário atual'}), 403
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} deletado com sucesso"})
    
    return jsonify({'message': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)