from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

# Health check na raiz
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'DocxWeb está rodando'}), 200

# Extensões
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota de registro
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado.'}), 400
    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuário registrado com sucesso.'}), 201

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Login realizado com sucesso.'})
    return jsonify({'error': 'Credenciais inválidas.'}), 401

# Rota protegida
@app.route('/protected')
@login_required
def protected():
    return jsonify({'email': current_user.email, 'id': current_user.id})

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Desconectado.'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
