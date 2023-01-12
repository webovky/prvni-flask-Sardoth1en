from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools
from mysqlite import SQLite
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3
import random
import string
import re
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")
 



def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")


@app.route("/info/")
def info():
    return render_template("info.html")


@app.route("/abc/")
def abc():
    if "uživatel" not in session:
        flash("Nejsi přihlášen. Pro přístup k téhle stránce se prosím přihlas.","error")
        return redirect(url_for("login", page=request.full_path))
    return render_template("abc.html", slova=slova)

@app.route("/kiwi/", methods=['GET', 'POST'])
def kiwi():
    if "uživatel" not in session:
        flash("Nejsi přihlášen. Pro přístup k téhle stránce se prosím přihlas.","error")
        return redirect(url_for("login", page=request.full_path))
    hmotnost = request.args.get('hmotnost')
    vyska = request.args.get('vyska')
    if hmotnost and vyska != None:
        try:
            bmi = int(hmotnost)/((int(vyska)/100)**2)
        except ZeroDivisionError:
            bmi =None
        except ValueError:
            bmi = None
    else:
        bmi =None
    return render_template("kiwi.html", bmi=bmi)

@app.route("/zkracovac/", methods=['GET', 'POST'])
def zkracovac():
    if request.method == "GET":
        if "uživatel" in session:
            with SQLite('data.db') as cur:
                res = cur.execute("SELECT zkrtaka, url FROM adresy WHERE user=?",[session["uživatel"]] )
                zkratky = res.fetchall()
                if not zkratky:
                    zkratky = []
        else:
            zkratky = []
        return render_template("zkracovac.html",zkratky=zkratky)

    if request.method == "POST":
        url = request.form.get('url')
        if url and re.match("https?://.+", url):
            
            zkratka = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            with SQLite('data.db') as cur:
                if "uživatel" in session:
                    cur.execute('INSERT INTO adresy (zkratka,url,user) VALUES (?,?,?)',[zkratka,url,session["uživatel"]])
                else:
                    cur.execute('INSERT INTO adresy (zkratka,url) VALUES (?,?)',[zkratka,url])
                flash("Adresa uložena")
                return redirect(url_for("zkracovac", new = zkratka))
        else:
            flash("To co jsi zadal není adresa webu")

        return redirect(url_for("zkracovac"))

@app.route("/zkracovac/<zkratka>", methods=['GET'])
def dezkracovac(zkratka):
    with SQLite('data.db') as cur:
        
        res = cur.execute("SELECT url from adresy WHERE zkratka=?", [zkratka])
        odpoved = res.fetchone()
        if odpoved:
            return redirect(odpoved[0])
        else:
            flash("To co jsi zadal není zkratka webu")
            return redirect(url_for("zkracovac"))

    return redirect(url_for("zkracovac"))



@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        jmeno = request.args.get('jmeno')
        heslo = request.args.get('heslo')
        
        
        return render_template("login.html")
    if request.method == "POST":
        jmeno = request.form.get('jmeno')
        heslo = request.form.get('heslo')
        page = request.args.get("page")
        with SQLite('data.db') as cur:
            cur.execute('SELECT passwd FROM user WHERE login = ?',[jmeno])
            ans = cur.fetchall()
        
        if ans and check_password_hash(ans[0][0],heslo):
            flash("Jsi přihlášen!","message")
            session["uživatel"]=jmeno
        else:
            flash("Nesprávné heslo!","message")
            if page:
                return redirect(page)

        """
        if jmeno== "David" and heslo== "webovky":
            flash("Jsi přihlášen!","message")
            session["uživatel"]=jmeno
            if page:
                return redirect(page)
        else:
            flash("Nesprávné heslo!","message")"""
            
        if page:
            return redirect(url_for("login", page=page))
        return redirect(url_for("login"))
@app.route("/registrace/", methods=['GET', 'POST'])
def registrace():
    
    if request.method == "GET":
        new = request.args.get("new")
        return render_template("registrace.html")

    if request.method == "POST":
        jmeno = request.form.get('jmeno')
        heslo = request.form.get('heslo')
        heslo2 = request.form.get('heslo_znovu')
        if not (jmeno and heslo2 and heslo): 
            flash("Není vše vyplněno!","message")
            return redirect(url_for("registrace"))
        if heslo != heslo2:
            flash("Hesla se neshodují!","message")
            return redirect(url_for("registrace"))
        try:
            with SQLite('data.db') as cur:
                cur.execute('INSERT INTO user (login,passwd) VALUES (?,?)',[jmeno,generate_password_hash(heslo)])
                cur.execute('SELECT passwd FROM user WHERE login = ?',[jmeno])
                flash("Jsi registrován!","message")
                flash("Jsi přihlášen!","message")
                session["uživatel"]=jmeno
                return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Jméno již existuje!","message")
            return redirect(url_for("registrace"))
    
    return redirect(url_for("registrace"))  

@app.route("/logout/", methods=['GET', 'POST'])
def logout():
    session.pop("uživatel", None)
    return redirect(url_for("login"))


@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>Toto je text</p> 

"""
