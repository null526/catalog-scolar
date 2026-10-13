from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'cheie_secreta_pentru_sesiune'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'profesor', 'elev', 'parinte'
    is_approved = db.Column(db.Boolean, default=True)
    
    elevi_parinte = db.relationship('Elev', foreign_keys='Elev.parinte_id', backref='parinte_user', lazy=True)
    profil_elev = db.relationship('Elev', foreign_keys='Elev.user_id', backref='cont_utilizator', uselist=False, lazy=True)

class Elev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    parinte_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    note = db.relationship('Nota', backref='elev', lazy=True, cascade="all, delete-orphan")
    absente = db.relationship('Absenta', backref='elev', lazy=True, cascade="all, delete-orphan")

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valoare = db.Column(db.Integer, nullable=False)
    materie = db.Column(db.String(50), nullable=False)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)

class Absenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    materie = db.Column(db.String(50), nullable=False)
    motivata = db.Column(db.Boolean, default=False)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('username')
        pass_input = request.form.get('password')
        
        user = User.query.filter_by(username=user_input, password=pass_input).first()
        if user:
            if not user.is_approved and user.role != 'admin':
                return "Contul tău așteaptă aprobarea administratorului!"
            
            cereri_in_asteptare = User.query.filter_by(is_approved=False).all() if user.role == 'admin' else []
            toti_elevii = Elev.query.all() if user.role == 'admin' else []
            toti_parintii = User.query.filter_by(role='parinte').all()
            toti_elevii_utilizatori = User.query.filter_by(role='elev').all()
            
            return render_template('dashboard.html', 
                                 user=user,
                                 username=user.username, 
                                 role=user.role, 
                                 cereri=cereri_in_asteptare,
                                 elevi=toti_elevii,
                                 parinti=toti_parintii,
                                 elevi_utilizatori=toti_elevii_utilizatori)
        else:
            return "Date incorecte! Încearcă din nou."
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        existing = User.query.filter_by(username=username).first()
        if existing:
            return "Acest utilizator există deja!"
            
        nou_user = User(username=username, password=password, role=role, is_approved=False)
        db.session.add(nou_user)
        db.session.commit()
        return "Cont înregistrat cu succes! Așteaptă aprobarea administratorului. <a href='/'>Mergi la Login</a>"
        
    return render_template('register.html')

@app.route('/aprobare/<int:user_id>/<action>')
def aprobare(user_id, action):
    user = User.query.get_or_404(user_id)
    if action == 'accept':
        user.is_approved = True
        db.session.commit()
    elif action == 'decline':
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('login'))

@app.route('/adauga_parinte', methods=['POST'])
def adauga_parinte():
    email = request.form.get('email_parinte')
    parola = request.form.get('parola_parinte')
    cont_parinte = User(username=email, password=parola, role='parinte', is_approved=True)
    db.session.add(cont_parinte)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/adauga_cont_elev', methods=['POST'])
def adauga_cont_elev():
    email = request.form.get('email_elev_cont')
    parola = request.form.get('parola_elev_cont')
    cont_elev = User(username=email, password=parola, role='elev', is_approved=True)
    db.session.add(cont_elev)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/adauga_elev_catalog', methods=['POST'])
def adauga_elev_catalog():
    nume = request.form.get('nume_elev')
    user_id = request.form.get('user_id')
    parinte_id = request.form.get('parinte_id')
    
    nou_elev = Elev(
        nume=nume, 
        user_id=user_id if user_id else None, 
        parinte_id=parinte_id if parinte_id else None
    )
    db.session.add(nou_elev)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/adauga_nota', methods=['POST'])
def adauga_nota():
    elev_id = request.form.get('elev_id')
    materie = request.form.get('materie')
    valoare = request.form.get('valoare')
    
    noua_nota = Nota(valoare=int(valoare), materie=materie, elev_id=elev_id)
    db.session.add(noua_nota)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/adauga_absenta', methods=['POST'])
def adauga_absenta():
    elev_id = request.form.get('elev_id')
    materie = request.form.get('materie')
    data = request.form.get('data')
    
    noua_absenta = Absenta(data=data, materie=materie, elev_id=elev_id, motivata=False)
    db.session.add(noua_absenta)
    db.session.commit()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(username='yanys2889@gmail.com').first()
        if not admin_user:
            admin_user = User(
                username='yanys2889@gmail.com', 
                password='yanyseboss12ez', 
                role='admin', 
                is_approved=True
            )
            db.session.add(admin_user)
            db.session.commit()
            
    app.run(debug=True, port=8080)