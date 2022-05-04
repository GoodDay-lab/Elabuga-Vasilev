from flask import Flask, render_template, request, redirect, url_for
import webbrowser
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "Tarantino_is_ugly"


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
    return render_template("promotion_image.html")


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
    if request.method == "GET":
        return render_template("carousel.html")


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
    form = Authorization()
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        return "<h1>Error</h1>"


@app.route("/distribution")
def distrib():
    list_ = ['Бэккет Рейнольдс', "Эмануэль Густав", "Шарль Де Голь", "Эрнесто Мадуро"]
    return render_template("distrib.html", list = list_)


@app.route("/tables/<sex>/<int:age>")
def table(sex, age):
    color = "#ff0000" if sex == 'female' else "#0000ff"
    image = "/static/img/alien_b.jpeg" if age > 21 else "/static/img/alien_l.jpeg"
    return render_template("tables.html", color=color, filename=image)


webbrowser.open("http://127.0.0.1:8081/tables/male/20")
app.run(port=8081)
