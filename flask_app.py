import os
from flask import Flask, app, render_template, request, jsonify, abort, make_response, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'projects.sqlite')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
app.secret_key = b'_5#nkj24390uy2L"F4ss123123Q8z\n\xec]/'
db = SQLAlchemy(app)

################## DATABASE #####################

class Projekt(db.Model):
    id_projekt = db.Column(db.Integer, primary_key=True, unique=True)
    nr_projekt = db.Column(db.Text)
    temat_projekt = db.Column(db.Text)
    data_rozpoczecia = db.Column(db.Date)
    data_zakonczenia = db.Column(db.Date)
    kwota = db.Column(db.Numeric)
    uwagi = db.Column(db.Text)

class Status(db.Model):
    id_status = db.Column(db.Integer, primary_key=True, unique=True)
    nazwa_status = db.Column(db.Text)

class Rodzaj(db.Model):
    id_rodzaj = db.Column(db.Integer, primary_key=True, unique=True)
    nazwa_rodzaj = db.Column(db.Text)

#    def __repr__(self) -> str:
#        return f'<ClassName {self.index}, {self.email}, {self.message}>'


db.create_all()

################## /DATABASE ####################

################## ROUTES #######################


@app.route('/')
@app.route('/strona_glowna')
def strona_glowna():
    return render_template('strona_glowna.html')

@app.route('/wykaz_projektow')
def wykaz_projektow():
    return render_template('wykaz_projektow.html')

@app.route('/dodaj_rodzaj', methods=['GET', 'POST'])
def dodaj_rodzaj():
    if request.method == 'POST':
        nowy_rodzaj = request.form['rodzaj']

        if nowy_rodzaj == '':
            flash('Pole nie może być puste!')
        elif db.session.query(Rodzaj.nazwa_rodzaj).\
             filter(Rodzaj.nazwa_rodzaj == nowy_rodzaj).\
             first() is not None:
            flash('Podany rodzaj już istnieje!')
        else:
            nowy_rekord = Rodzaj(nazwa_rodzaj=nowy_rodzaj)
            db.session.add(nowy_rekord)
            db.session.commit()

    return render_template('dodaj_rodzaj.html')

@app.route('/dodaj_status', methods=['GET', 'POST'])
def dodaj_status():
    if request.method == 'POST':
        nowy_status = request.form['status']

        if nowy_status == '':
            flash('Pole nie może być puste!')
        elif db.session.query(Status.nazwa_status).\
             filter(Status.nazwa_status == nowy_status).\
             first() is not None:
            flash('Podany status już istnieje!')
        else:
            nowy_rekord = Status(nazwa_status=nowy_status)
            db.session.add(nowy_rekord)
            db.session.commit()

    return render_template('dodaj_status.html')

@app.route('/edytuj_rodzaj', methods=['GET','POST'])
def edytuj_rodzaj():
    db_class  = Rodzaj
    db_pk     = Rodzaj.id_rodzaj
    db_pk_str = 'id_rodzaj'
    editable_columns = ['nazwa_rodzaj']

    if request.method == 'POST':
        if request.form['action'] == 'send':
            query = db.session.query(db_class).filter(db_pk == request.form[db_pk_str])
            if query is not None:
                mydict = { column.name : request.form[column.name] for column in db_class.__table__.columns if column.name in editable_columns }
                query.update(mydict)
                db.session.commit()

        elif request.form['action'] == 'delete':
            query = db.session.query(db_class).filter(db_pk == request.form[db_pk_str])
            if query is not None:
                query.delete()
                db.session.commit()

    return render_template('edytuj_rodzaj.html',
           db_class=db_class,
           db_query=db.session.query(db_class),
           editable_columns=editable_columns)

@app.route('/edytuj_status', methods=['GET','POST'])
def edytuj_status():
    db_class  = Status
    db_pk     = Status.id_status
    db_pk_str = 'id_status'
    editable_columns = ['nazwa_status']

    if request.method == 'POST':
        if request.form['action'] == 'send':
            query = db.session.query(db_class).filter(db_pk == request.form[db_pk_str])
            if query is not None:
                mydict = { column.name : request.form[column.name] for column in db_class.__table__.columns if column.name in editable_columns }
                query.update(mydict)
                db.session.commit()

        elif request.form['action'] == 'delete':
            query = db.session.query(db_class).filter(db_pk == request.form[db_pk_str])
            if query is not None:
                query.delete()
                db.session.commit()

    return render_template('edytuj_status.html',
           db_class=db_class,
           db_query=db.session.query(db_class),
           editable_columns=editable_columns)

@app.route('/dodaj_projekt')
def dodaj_projekt():
    return render_template('dodaj_projekt.html')

@app.route('/projekty_wg_rodzaj')
def projekty_wg_rodzaj():
    return render_template('projekty_wg_rodzaj.html')

@app.route('/projekty_wg_status')
def projekty_wg_status():
    return render_template('projekty_wg_status.html')

@app.route('/edytuj_projekt')
def edytuj_projekt():
    return render_template('edytuj_projekt.html')

'''
@app.route('/search')
def search_page():
    return render_template('searchpage.html')
'''

################## /ROUTES ######################


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
