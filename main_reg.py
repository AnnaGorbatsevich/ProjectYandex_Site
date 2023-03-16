from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.product import Product
from data.LoginForm import LoginForm
from data.AddProductForm import ProductForm, ProductForm2
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.register import RegisterForm


from flask import url_for, redirect, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename


import re
import os
from wtforms import TextAreaField, validators, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


class CartForm(FlaskForm):
    submit = SubmitField('Пересчитать')


def main():
    db_session.global_init("db/mars_explorer.sqlite")

    @app.route("/add_product", methods=['GET', 'POST'])
    def add_product():
        if not current_user.is_authenticated:
            return redirect('/register')
        form = ProductForm()
        session = db_session.create_session()
        products = session.query(Product).all()
        users = session.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}
        session.commit()

        if form.validate_on_submit():
            #print(request.form)
            keys = [i for i in request.form][5:-1]
            #print(keys)
            #print(request.form)
            product = Product(
                product=form.product.data,
                country=form.country.data,
                description=form.description.data,
                others='&'.join([request.form.get(j) for j in keys]),
                price=form.price.data
            )
            #print(form.product)
            session.add(product)
            session.commit()
            return redirect('/')
        return render_template("add_product.html", products=products, names=names, title="Work Status", form=form)

    @app.route("/product<id>", methods=['GET', 'POST'])
    def product(id):
        if not current_user.is_authenticated:
            return redirect('/register')
        form = ProductForm2()
        session = db_session.create_session()
        product = session.query(Product).filter(Product.id == id)[0]
        productDict = {}
        productDict["country"] = product.country.split()
        #print(list(request.form))
        price = product.price
        product2 = Product(product=product.product, country=request.form.get('country'),
                           others='&'.join(i + "&" + request.form[i] for i in list(request.form)[1:-2]),
                           count=1, price=product.price, prev_id=product.id)
        cnt = 0
        if product.others and len(product.others.split("&")) != 0:
            for i in range(0, len(product.others.split("&")), 2):
                if product.others.split("&")[i] != '' and product.others.split("&")[i + 1] != "":
                    productDict[product.others.split('&')[i]] = product.others.split('&')[i + 1].split()
                    cnt += 1


        if form.validate_on_submit():
            #print("XX")
            user = session.query(User).filter(User.id == current_user.id).first()
            p = {"id": product.id, "product": product2.product, "country": product2.country, "price": product2.price}
            s = product2.others.split("&")
            #print(s)
            for j in range(0, len(s), 2):
                if len(s[j]) == 0:
                    continue
                #print(s[j])
                if s[j] != '' and s[j + 1] != '':
                    p[s[j]] = s[j + 1]
            for i in range(len(user.product)):
                p2 = {"id": user.product[i].prev_id, "product": user.product[i].product, "country": user.product[i].country,
                     "price": product.price}
                s = user.product[i].others.split("&")
                #print(s)
                for j in range(0, len(s), 2):
                    if len(s[j]) == 0:
                        continue
                    #print(s[j])
                    if s[j] != '' and s[j + 1] != '':
                        p2[s[j]] = s[j + 1]
                fl = True
                print(p)
                print(p2)
                for j in p:
                    if j not in p2 or p[j] != p2[j]:
                        fl = False

                if fl:
                    user.product[i].count += 1
                    session.commit()
                    return redirect('/index')

            #print(product.others.split("&"))
            if not product2.country or cnt != len(list(request.form)) - 3:
                pass
            else:
                user.product.append(product2)
                session.commit()
                #print(product2.others)
                """for i in user.product:
                    #print(i)"""
                return redirect('/')
        #print(request.form)
        return render_template('product.html', product=productDict, title=product.product, description=product.description, price=price, form=form)



    @app.route("/")
    @app.route("/index")
    def index():
        if not current_user.is_authenticated:
            return redirect('/register')
        session = db_session.create_session()
        products = session.query(Product).all()
        users = session.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}
        return render_template("index.html", products=products, names=names, title="Work Status")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if current_user.is_authenticated:
            return redirect('/index')
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                surname=form.surname.data,
                age=form.age.data,
                speciality=form.speciality.data,
                position=form.position.data,
                address=form.address.data,
                # about=form.about.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect('/index')
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/cleaning')
    def cleaning():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        for i in range(len(user.product)):
            user.product[i].count = 0
            session.commit()

        return redirect("https://www.paypal.com/ru/home")


    @app.route("/cart", methods=["POST", "GET"])
    def cart():
        form = CartForm()
        if not current_user.is_authenticated:
            return redirect('/register')
        sm = 0
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if len(list(request.form)) >= 2:
            #print("XX")
            for i in range(len(user.product)):
                user.product[i].count = request.form.get("input" + str(user.product[i].id))
                #print("input" + str(user.product[i].id))
                session.commit()

        products = []
        #print(user.product)
        for i in user.product:
            if not i.count:
                continue
            products.append({"prev_id": i.prev_id, "id": i.id, "Количество": i.count, "Название": i.product, "Страна отправки": i.country})
            sm += i.count * i.price
            s = i.others.split("&")
            #print(s)
            for j in range(0, len(s), 2):
                if len(s[j]) == 0:
                    continue
                #print(s[j])
                products[-1][s[j]] = s[j + 1]
            products[-1]["Цена"] = i.price
        #print(request.form)
        return render_template('cart.html', title='Корзина', products=products, form=form, sm=sm)

    app.run()


if __name__ == '__main__':
    main()

