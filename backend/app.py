import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
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

# Configurações e seed de admin
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def initialize():
    if not User.query.filter_by(email=os.getenv('ADMIN_EMAIL')).first():
        admin = User(email=os.getenv('ADMIN_EMAIL'))
        admin.set_password(os.getenv('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()

# Página de login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Processa login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page', error='Credenciais inválidas'))

# Dashboard para criar usuários
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        if not User.query.filter_by(email=email).first():
            new_user = User(email=email)
            new_user.set_password(pwd)
            db.session.add(new_user)
            db.session.commit()
            message = f'Usuário {email} criado com sucesso.'
        else:
            message = 'Email já cadastrado.'
    users = User.query.all()
    return render_template('dashboard.html', users=users, message=message)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
