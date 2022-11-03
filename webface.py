from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools

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
    return render_template("abc.html", slova=slova)

@app.route("/kiwi/", methods=['GET', 'POST'])
def kiwi():
    if "uživatel" not in session:
        flash("Nejsi přihlášen. Pro přístup k téhle stránce se prosím přihlas.")
        return redirect(url_for("login"))
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

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        jmeno = request.args.get('jmeno')
        heslo = request.args.get('heslo')
        return render_template("login.html")
    if request.method == "POST":
        jmeno = request.form.get('jmeno')
        heslo = request.form.get('heslo')
        if jmeno== "David" and heslo== "webovky":
            session["uživatel"]=jmeno

        return redirect(url_for("login"))
    
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
