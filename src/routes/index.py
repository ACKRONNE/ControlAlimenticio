from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.db import db
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_mail import Mail, Message
from flask import current_app as app

# Entidades
from src.models.models import Paciente, Especialista, Alimento, Comida, AC
# //

ind = Blueprint('index', __name__)

# Configuración del correo
def send_reset_email(user, email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = s.dumps(email, salt='email-confirm')
    msg = Message('Password Reset Request', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
    link = url_for('index.reset_token', token=token, _external=True)
    msg.body = f'''To reset your password, visit the following link:
{link}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail = Mail(app)
    try:
        mail.send(msg)
        app.logger.info(f'Password reset email sent to {email}')
    except Exception as e:
        app.logger.error(f'Failed to send email to {email}: {e}')

# Pagina principal <
@ind.route('/')
def index():
    return render_template('index.html')
# // >

# Tipo de usuario <
@ind.route('/registro')
def registro():
    return render_template('registro.html')
# // >

# Iniciar sesion <
@ind.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        _correo = request.form['ind-correo']
        _clave = request.form['ind-clave']

        # Check if the user exists in the database
        account = db.session.query(Paciente.id_paciente, Paciente.clave).filter(Paciente.correo == _correo).first()
        
        if account: # Temporal para hacer pruebas sin seguridad
            session['logueado'] = True
            session['id'] = account.id_paciente
            _id = session['id']
        
            return redirect(url_for('paciente.inicio', id=_id))

        else:    
            account = db.session.query(Especialista.id_espe, Especialista.clave).filter(Especialista.correo == _correo).first()

            if account: # Temporal para hacer pruebas sin seguridad
                session['logueado'] = True
                session['id'] = account.id_espe
                _id = session['id']
            
                return redirect(url_for('especialista.inicio', id=_id))            
            else:
                return render_template('index.html', mensaje = 'El usuario no se encuentra registrado o la contraseña es incorrecta')

    else:
        return render_template('index.html', mensaje = 'El usuario no se encuentra registrado o la contraseña es incorrecta')
# // >

# Cerrar sesion del usuario <
@ind.route('/logout/<id>', methods=['GET'])
def logout(id):
    user = Paciente.query.get(id)
    user2 = Especialista.query.get(id)

    if user is None and user2 is None:
        return "Usuario no encontrado"

    if (user is not None and user.id_paciente == int(id) and session['logueado']) \
       or (user2 is not None and user2.id_espe == int(id) and session['logueado']):
        session.pop('id', None)
        session.clear()
        return redirect(url_for('index.index'))
    else:
        return "Error 404, No se pudo cerrar la sesion"
# // >

# Recuperar contraseña <
@ind.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        user = db.session.query(Paciente).filter_by(correo=email).first()
        if user:
            send_reset_email(user, email)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('index.login'))
        else:
            flash('Email not found', 'danger')
    return render_template('reset_request.html')

@ind.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        flash('The token is invalid or has expired', 'warning')
        return redirect(url_for('index.reset_request'))

    if request.method == 'POST':
        password = request.form['password']
        user = db.session.query(Paciente).filter_by(correo=email).first()
        if user:
            user.clave = generate_password_hash(password)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('index.login'))
    return render_template('reset_token.html')
# // >

# Test email route
@ind.route('/test_email')
def test_email():
    msg = Message('Test Email', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=['your_email@gmail.com'])
    msg.body = 'This is a test email.'
    mail = Mail(app)
    try:
        mail.send(msg)
        return 'Test email sent successfully!'
    except Exception as e:
        return f'Failed to send test email: {e}'
