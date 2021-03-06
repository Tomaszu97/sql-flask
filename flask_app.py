import os
from flask import Flask, app, render_template, request, jsonify, abort, make_response, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import time

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
    id_rodzaj = db.Column(db.Integer, db.ForeignKey("rodzaj.id_rodzaj"))
    id_status = db.Column(db.Integer, db.ForeignKey("status.id_status"))
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

db.create_all()

################## /DATABASE ####################

################## ROUTES #######################


@app.route('/')
@app.route('/strona_glowna')
def strona_glowna():
    return render_template('strona_glowna.html')


@app.route('/wykaz_projektow')
def wykaz_projektow():
    columns = [
        (Projekt, 'id_projekt'),
        (Projekt, 'nr_projekt'),
        (Projekt, 'temat_projekt'),
        (Projekt, 'data_rozpoczecia'),
        (Projekt, 'data_zakonczenia'),
        (Projekt, 'kwota'),
        (Projekt, 'uwagi'),
        (Rodzaj, 'nazwa_rodzaj'),
        (Status, 'nazwa_status'),
    ]

    rows = db.session.query(Projekt,Rodzaj,Status)\
        .join(Rodzaj)\
        .join(Status)\
        .all()

    return render_template('wykaz_projektow.html', columns=columns, rows=rows)

@app.route('/dodaj_rodzaj', methods=['GET', 'POST'])
def dodaj_rodzaj():
    if request.method == 'POST':
        nowy_rodzaj = request.form['rodzaj']

        if nowy_rodzaj == '':
            flash('Pole nie mo??e by?? puste!')
        elif db.session.query(Rodzaj.nazwa_rodzaj).\
             filter(Rodzaj.nazwa_rodzaj == nowy_rodzaj).\
             first() is not None:
            flash('Podany rodzaj ju?? istnieje!')
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
            flash('Pole nie mo??e by?? puste!')
        elif db.session.query(Status.nazwa_status).\
             filter(Status.nazwa_status == nowy_status).\
             first() is not None:
            flash('Podany status ju?? istnieje!')
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

@app.route('/dodaj_projekt', methods=['GET','POST'])
def dodaj_projekt():
    if request.method == 'POST':
        try:
            new_project = {}
            new_project['nr_projekt'] = request.form['nr_projekt']
            new_project['temat_projekt'] = request.form['temat_projekt']
            new_project['data_rozpoczecia'] = dt.strptime(request.form['data_rozpoczecia'], '%Y-%m-%d')
            new_project['data_zakonczenia'] = dt.strptime(request.form['data_zakonczenia'], '%Y-%m-%d')
            val = int(request.form['kwota'])
            assert(val > 0)
            new_project['kwota'] = val
            new_project['uwagi'] = request.form['uwagi']
            assert(all(new_project.values()))
            new_project['id_rodzaj'] = db.session.query(Rodzaj).filter(Rodzaj.nazwa_rodzaj == request.form['rodzaj']).first().id_rodzaj
            new_project['id_status'] = db.session.query(Status).filter(Status.nazwa_status == request.form['status']).first().id_status
            new_project = Projekt(**new_project)
            db.session.add(new_project)
            db.session.commit()
        except Exception as e:
            flash(f'Wype??nij poprawnie wszystkie pola!')
            db.session.rollback()

    return render_template('dodaj_projekt.html', db=db, Rodzaj=Rodzaj, Status=Status)

@app.route('/projekty_wg_rodzaj', methods=['GET','POST'])
def projekty_wg_rodzaj():
    columns = [
        (Projekt, 'id_projekt'),
        (Projekt, 'nr_projekt'),
        (Projekt, 'temat_projekt'),
        (Projekt, 'data_rozpoczecia'),
        (Projekt, 'data_zakonczenia'),
        (Projekt, 'kwota'),
        (Projekt, 'uwagi'),
        (Rodzaj, 'nazwa_rodzaj'),
        (Status, 'nazwa_status'),
    ]

    if request.method == 'POST':
        rows = db.session.query(Projekt,Rodzaj,Status)\
            .join(Rodzaj)\
            .join(Status)\
            .filter(Rodzaj.nazwa_rodzaj == request.form['rodzaj'])\
            .all()
    else:
        rows = []

    return render_template('projekty_wg_rodzaj.html', db=db, Rodzaj=Rodzaj, columns=columns, rows=rows)

@app.route('/projekty_wg_status', methods=['GET','POST'])
def projekty_wg_status():
    columns = [
        (Projekt, 'id_projekt'),
        (Projekt, 'nr_projekt'),
        (Projekt, 'temat_projekt'),
        (Projekt, 'data_rozpoczecia'),
        (Projekt, 'data_zakonczenia'),
        (Projekt, 'kwota'),
        (Projekt, 'uwagi'),
        (Rodzaj, 'nazwa_rodzaj'),
        (Status, 'nazwa_status'),
    ]

    if request.method == 'POST':
        rows = db.session.query(Projekt,Rodzaj,Status)\
            .join(Rodzaj)\
            .join(Status)\
            .filter(Status.nazwa_status == request.form['status'])\
            .all()
    else:
        rows = []

    return render_template('projekty_wg_status.html', db=db, Status=Status, columns=columns, rows=rows)

# most ellastic implementation
# supports foreign key connected tables, implements pulldown menu for these options
# note - foreign_key_colname must be the same for both main and helper tables
# note2 - input type select == pull select values by foreign key from another table
@app.route('/edytuj_projekt', methods=['GET','POST'])
def edytuj_projekt():
    main_table=Projekt
    #table class, column name string, is_editable, input_type, foreign_key_colname
    columns = [
        (Projekt, 'id_projekt',       False, 'number', None),
        (Projekt, 'nr_projekt',       True,  'text',   None),
        (Projekt, 'temat_projekt',    True,  'text',   None),
        (Projekt, 'data_rozpoczecia', True,  'date',   None),
        (Projekt, 'data_zakonczenia', True,  'date',   None),
        (Projekt, 'kwota',            True,  'number', None),
        (Projekt, 'uwagi',            True,  'text',   None),
        (Rodzaj,  'nazwa_rodzaj',     True,  'select', 'id_rodzaj'),
        (Status,  'nazwa_status',     True,  'select', 'id_status'),
    ]

    if request.method == 'POST':
        if request.form['action'] == 'send':
            query = db.session.query(main_table).filter(
                main_table.__mapper__.primary_key[0] == \
                request.form[main_table.__mapper__.primary_key[0].name])
            if query is not None:
                mydict = {}
                for column in columns:
                    idx=4
                    if column[4] is None:
                        idx=1
                    if column[3] == 'date':
                        mydict[column[idx]] = dt.strptime(request.form[column[idx]], '%Y-%m-%d')
                    else: #text, number
                        mydict[column[idx]] = request.form[column[idx]]
                print(80*'#')
                print(mydict)
                query.update(mydict)
                db.session.commit()

        elif request.form['action'] == 'delete':
            db.session.delete(main_table.query.get(
                request.form[main_table.__mapper__.primary_key[0].name]))
            db.session.commit()

    rows = db.session.query(Projekt,Rodzaj,Status)\
        .join(Rodzaj)\
        .join(Status)\
        .all()

    return render_template('edytuj_projekt.html',
                           db=db,
                           main_table=main_table,
                           Projekt=Projekt,
                           Rodzaj=Rodzaj,
                           Status=Status,
                           columns=columns,
                           rows=rows)

'''
@app.route('/search')
def search_page():
    return render_template('searchpage.html')
'''

################## /ROUTES ######################

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
