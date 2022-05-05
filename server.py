import os

from flask import Flask, render_template, request, redirect, url_for, session, make_response
import webbrowser
from forms import *
import json
from random import randrange
import uuid
from data.db_session import *
from data.__all_models import *

app = Flask(__name__)
global_init("/db/blogs.sqlite")
app.config['SECRET_KEY'] = "Tarantino_is_ugly"


@app.route("/add_work", methods=['POST', 'GET'])
def add_work():
    form = Job()
    name = session['name']
    if request.method == 'GET':
        return render_template("add_work.html", form=form, LOGGED_PERSON_NAME=name)
    else:
        id = session['id']
        s = create_session()
        job = Jobs()
        job.team_leader = int(id)
        job.job = form.job.data
        job.work_size = int(form.work_size.data)
        job.collaborators = int(id)
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = False
        s.add(job)
        s.commit()
        s.close()
        return "<h1>Форма добавлена</h1>"


@app.route("/edit/<int:work_id>", methods=['POST', 'GET'])
def editing(work_id):
    form = Job()
    id = session['id']
    name = session['name']
    if request.method == 'GET':
        return render_template('add_work.html', LOGGED_PERSON_NAME=name, form=form)
    elif request.method == 'POST':
        s = create_session()
        work = s.query(Jobs).filter(Jobs.id == work_id).first()
        s.close()
        if work.team_leader == int(id):
            s = create_session()
            job = s.query(Jobs).filter(work.id == Jobs.id).first()
            job.team_leader = int(id)
            job.job = form.job.data
            job.work_size = int(form.work_size.data)
            job.collaborators = int(id)
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = False
            s.commit()
            s.close()
            return render_template('add_work.html', LOGGED_PERSON_NAME=name, form=form)
        return "<h1> Access denied </h1>"


@app.route('/index/<name>')
@app.route("/<name>")
def main_page(name):
    return render_template("main.html", TITLE=name)


@app.route("/promotion")
def promotion_page():
    return   """<h1>Человечество вырастает из детства.</h1></br>
                <h1>Человечеству мала одна планета.</h1></br>
                <h1>Мы сделаем обитаемыми безжизненные пока планеты.</h1></br>
                <h1>И начнем с Марса!</h1></br>
                <h1>Присоединяйся!</h1></br>"""


@app.route("/image_mars")
def image():
    return render_template("image_mars.html")


@app.route("/promotion_image")
def promotion_image():
    LOGGED = session['name']
    return render_template("promotion_image.html", LOGGED_PERSON_NAME=LOGGED)


@app.route("/astronaut_selection", methods=['GET', 'POST'])
def reaction():
    form = LoginForm()
    # if not form.validate_on_submit():
    #     return "<h1>BAD REQUEST</h1>", 404
    if request.method == "GET":
        return render_template("astro_selection.html", list=form)
    elif request.method == "POST":
        return render_template("auto_answer.html", form=form)


@app.route("/load_image", methods=["GET", "POST"])
def load_photo():
    if request.method == "GET":
        return render_template("load_image.html")
    if request.method == "POST":
        f = request.files['file']
        with open("./static/img/buffer.jpg", 'wb') as image:
            image.write(f.read())
        return render_template("answer_image.html")


@app.route("/carousel", methods=["GET", "POST"])
def carousel():
    form = UploadForm()
    if request.method == "GET":
        result = []
        for _, _, files in os.walk("./static/img/carousel"):
            result = ["/static/img/carousel/" + f for f in files]
        return render_template("carousel.html", form=form, files=result)
    elif request.method == "POST":
        f = request.files['file']
        with open("./static/img/carousel/" + str(uuid.uuid4()) + '.jpg', mode='wb') as file:
            file.write(f.read())
        return redirect("/carousel")


@app.route("/choice/<planet>")
def choice(planet):
    return render_template("choice.html", planet_name=planet)


@app.route("/results/<name>/<int:step>/<float:score>")
def results(**keys):
    return render_template("results.html", name=keys['name'], hello=keys['step'], score=keys['score'])


@app.route("/training/<prof>")
def training(prof):
    if "строитель" in prof.lower() or "инженер" in prof.lower():
        return render_template("training.html", TITLE="Инженерная специальность", prof="Инженерная", filepath=url_for('static', filename='/img/engineer.jpeg'))
    return render_template("training.html", TITLE="Научная специальность", prof="Научная", filepath=url_for('static', filename='/img/scientist.jpeg'))


@app.route("/list_prof/<outt>")
def list_prof(outt):
    list_ = ['Машиностроитель', 'Строитель', 'Конструктор', 'Учёный', 'Биолог']
    return render_template("list_prof.html", value=outt, list=list_)


@app.route("/answer", methods=["POST", "GET"])
def answer():
    return redirect("/astronaut_selection")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm2()
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        s = create_session()
        user = s.query(User).first()
        s.close()
        if user:
            id_ = user.id
            user_name = user.name
            session['id'] = str(id_)
            session['name'] = str(user_name)
            return make_response(redirect('/distribution'))
        return "<h1>Error!</h1>"


@app.route("/works", methods=["POST", "GET"])
def works():
    name = session['name']
    s = create_session()
    works = s.query(Jobs).all()
    return render_template("all_works.html", works=works, LOGGED_PERSON_NAME=name)


@app.route("/distribution")
def distrib():
    name = session['name']
    list_ = ['Бэккет Рейнольдс', "Эмануэль Густав", "Шарль Де Голь", "Эрнесто Мадуро"]
    return render_template("distrib.html", list = list_, LOGGED_PERSON_NAME = name)


@app.route("/tables/<sex>/<int:age>")
def table(sex, age):
    color = "#ff0000" if sex == 'female' else "#0000ff"
    image = "/static/img/alien_b.jpeg" if age > 21 else "/static/img/alien_l.jpeg"
    return render_template("tables.html", color=color, filename=image)


@app.route("/member")
def member():
    f = open("templates/comrades.json")
    dict_ = json.load(f)
    crewmate = dict_['crew'][randrange(0, len(dict_['crew']))]
    return render_template("member.html", name=crewmate['name'], filename=crewmate['photo'], specs=crewmate['specs'])


webbrowser.open("http://127.0.0.1:8081/add_work")
app.run(port=8081)
