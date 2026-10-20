from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'cheie_secreta_catalog_sigura_123'

# Setăm calea bazei de date în folderul persistent /tmp pe Render
if os.environ.get('RENDER'):
    db_path = '/tmp/catalog.db'
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'catalog.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    parola = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='elev')
    aprobat = db.Column(db.Boolean, default=False)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=True)

class Elev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    clasa = db.Column(db.String(20), nullable=False)
    note = db.relationship('Nota', backref='elev', cascade='all, delete-orphan', lazy=True)
    absente = db.relationship('Absenta', backref='elev', cascade='all, delete-orphan', lazy=True)

    def calculeaza_medie(self):
        if not self.note:
            return 0.0
        total = sum(n.valoare for n in self.note)
        return round(total / len(self.note), 2)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valoare = db.Column(db.Integer, nullable=False)
    materie = db.Column(db.String(50), nullable=False)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)

class Absenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    materie = db.Column(db.String(50), nullable=False)
    motivata = db.Column(db.Boolean, default=False)
    motiv = db.Column(db.String(200), nullable=True)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)

with app.app_context():
    db.create_all()
    try:
        admin = User.query.filter_by(email='yanys2889@gmail.com').first()
        if not admin:
            admin = User(
                nume='Admin',
                email='yanys2889@gmail.com',
                parola=generate_password_hash('yanyseboss12ez'),
                rol='admin',
                aprobat=True
            )
            db.session.add(admin)
            db.session.commit()
        else:
            admin.rol = 'admin'
            admin.aprobat = True
            db.session.commit()
    except Exception as e:
        db.session.rollback()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        parola = request.form.get('parola', '').strip()
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.parola, parola):
            if not user.aprobat:
                flash('Contul tău așteaptă aprobarea administratorului.', 'warning')
                return redirect(url_for('login'))
            
            session['user_id'] = user.id
            session['rol'] = user.rol
            session['nume'] = user.nume
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            flash('Email sau parolă incorectă!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            nume = request.form.get('nume', '').strip()
            email = request.form.get('email', '').strip()
            parola = request.form.get('parola', '').strip()
            rol_solicitat = request.form.get('rol', 'elev').strip()
            
            if User.query.filter_by(email=email).first():
                flash('Acest e-mail este deja înregistrat!', 'danger')
                return redirect(url_for('register'))
                
            is_admin = (email == 'yanys2889@gmail.com')
            noul_user = User(
                nume=nume,
                email=email,
                parola=generate_password_hash(parola),
                rol='admin' if is_admin else rol_solicitat,
                aprobat=True if is_admin else False
            )
            db.session.add(noul_user)
            db.session.commit()
            flash('Cererea a fost trimisă cu succes!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Eroare: {str(e)}', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
        
    if user.rol == 'admin':
        elevi = Elev.query.all()
        cereri = User.query.filter_by(aprobat=False).all()
        return render_template('dashboard.html', user=user, elevi=elevi, cereri=cereri)
        
    elif user.rol == 'profesor':
        elevi = Elev.query.all()
        return render_template('dashboard_profesor.html', user=user, elevi=elevi)
        
    elif user.rol in ['elev', 'parinte']:
        if user.rol == 'elev':
            elev = Elev.query.filter_by(nume=user.nume).first()
        else:
            elev = Elev.query.get(user.elev_id) if user.elev_id else None
        return render_template('dashboard_parinte.html', user=user, elev=elev)
        
    return redirect(url_for('login'))

@app.route('/admin/creeaza_elev', methods=['POST'])
def creeaza_elev():
    if session.get('rol') not in ['admin', 'profesor']:
        return redirect(url_for('dashboard'))
    nume = request.form.get('nume', '').strip()
    clasa = request.form.get('clasa', '').strip()
    if nume and clasa:
        noul_elev = Elev(nume=nume, clasa=clasa)
        db.session.add(noul_elev)
        db.session.commit()
        flash(f'Elevul {nume} a fost adăugat cu succes!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/sterge_elev/<int:id>')
def sterge_elev(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('dashboard'))
    elev = Elev.query.get(id)
    if elev:
        db.session.delete(elev)
        db.session.commit()
        flash('Elevul a fost șters.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/admin/adauga_nota', methods=['POST'])
def adauga_nota():
    if session.get('rol') not in ['admin', 'profesor']:
        return redirect(url_for('dashboard'))
    elev_id = request.form.get('elev_id')
    materie = request.form.get('materie', '').strip()
    valoare = request.form.get('valoare')
    if elev_id and materie and valoare:
        db.session.add(Nota(valoare=int(valoare), materie=materie, elev_id=elev_id))
        db.session.commit()
        flash('Notă adăugată cu succes!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/adauga_absenta', methods=['POST'])
def adauga_absenta():
    if session.get('rol') not in ['admin', 'profesor']:
        return redirect(url_for('dashboard'))
    elev_id = request.form.get('elev_id')
    materie = request.form.get('materie', '').strip()
    if elev_id and materie:
        db.session.add(Absenta(materie=materie, elev_id=elev_id))
        db.session.commit()
        flash('Absență adăugată cu succes!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/motiveaza_absenta/<int:id>', methods=['POST'])
def motiveaza_absenta(id):
    if session.get('rol') not in ['admin', 'profesor']:
        return redirect(url_for('dashboard'))
    absenta = Absenta.query.get(id)
    motiv = request.form.get('motiv', 'Motivată')
    if absenta:
        absenta.motivata = True
        absenta.motiv = motiv
        db.session.commit()
        flash('Absență motivată!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/aprobe_user/<int:id>', methods=['POST'])
def aprobe_user(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('dashboard'))
    u = User.query.get(id)
    if u:
        u.aprobat = True
        u.rol = request.form.get('rol', u.rol)
        elev_id = request.form.get('elev_id')
        if elev_id and elev_id != '':
            u.elev_id = int(elev_id)
        db.session.commit()
        flash(f'Utilizatorul {u.nume} a fost aprobat!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/respinge_user/<int:id>')
def respinge_user(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('dashboard'))
    u = User.query.get(id)
    if u:
        db.session.delete(u)
        db.session.commit()
        flash('Cerere respinsă.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Te-ai deconectat.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)