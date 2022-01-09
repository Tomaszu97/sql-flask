import os
from flask import Flask, app, render_template, request, jsonify, abort, make_response
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'projects.sqlite')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
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
        form_data = request.form
        nowy_rodzaj = Rodzaj(nazwa_rodzaj=form_data['rodzaj'])
        db.session.add(nowy_rodzaj)
        db.session.commit()
    return render_template('dodaj_rodzaj.html')

@app.route('/dodaj_status')
def dodaj_status():
    return render_template('dodaj_status.html')

@app.route('/edytuj_rodzaj')
def edytuj_rodzaj():
    return render_template('edytuj_rodzaj.html')

@app.route('/edytuj_status')
def edytuj_status():
    return render_template('edytuj_status.html')

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
