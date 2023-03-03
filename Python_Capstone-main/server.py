#SERVER FOR LEDGER#
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from model import connect_to_db, db, get_services, Service, get_pricing, Pricing, get_enhancements, Enhancement, get_clients, Client, get_history, History, User, LoginForm, RegistrationForm, HomePage, EditHomePageForm
from datetime import datetime


app = Flask(__name__)
app.secret_key = "dev"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/jslmt'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


##LOGIN FORMS


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error = None
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                error = "Invalid username or password"
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('home'))

@app.route("/home")
@login_required
def home():
    home_page = HomePage.query.first()
    return render_template('home.html', content=home_page.content)

@app.route("/edit_home", methods=['GET', 'POST'])
@login_required
def edit_home():
    form = EditHomePageForm()
    home_page = HomePage.query.first()
    if form.validate_on_submit():
        home_page.content = form.content.data
        db.session.commit()
        return redirect(url_for('home'))
    form.content.data = home_page.content
    return render_template('edit_home.html', form=form)










# ##LOGIN ROUTES
# @app.route("/")
# def loginpage():

#     return render_template("loginpage.html")

# @app.route("/logout")
# def logout():
#     #implement this feature

#     return redirect("/")

# @app.route("/login", methods=["POST"])
# def process_login():

#     username = request.form.get("username")
#     password = request.form.get("password")

#     user = get_user_by_username(username)
#     if not user or user.password != password:
#         flash("The email or password you entered was incorrect.")
#     else:
#         # Log in user by storing the user's email in session
#         session["user_email"] = user.email
#         flash(f"Welcome back, {user.email}!")

#     return redirect("/welcome")





##WELCOME PAGE (for after login)




##PRICING ROUTES
@app.route("/pricing")
@login_required
def pricing():
    pricing = get_pricing()
    return render_template("pricing.html", pricing=pricing)

@app.route("/edit_pricing", methods=['GET', 'POST'])
@login_required
def edit_pricing():
    pricing = get_pricing()
    return render_template("edit_pricing.html", pricing=pricing)

@app.route("/edit_pricing/save", methods=['POST'])
@login_required
def save_pricing():
    pricing_id = request.form['pricing_id']
    pricing_name = request.form['pricing_name']
    pricing_location = request.form['pricing_location']
    pricing_duration = request.form['pricing_duration']
    pricing_price = request.form['pricing_price']
    pricing = Pricing.query.filter_by(pricing_id=pricing_id).first()
    pricing.pricing_id = pricing_id
    pricing.pricing_name = pricing_name
    pricing.pricing_location = pricing_location
    pricing.pricing_duration = pricing_duration
    pricing.pricing_price = pricing_price
    db.session.commit() 
    return redirect("/edit_pricing")

@app.route("/edit_pricing/delete", methods=['POST'])
@login_required
def delete_pricing():
    pricing_id = request.form['pricing_id']
    pricing = Pricing.query.get(pricing_id)
    db.session.delete(pricing)
    db.session.commit()
    return redirect("/edit_pricing")

@app.route("/edit_pricing/add", methods=['POST'])
@login_required
def add_pricing():
    pricing_name = request.form['pricing_name']
    pricing_location = request.form['pricing_location']
    pricing_duration = request.form['pricing_duration']
    pricing_price = request.form['pricing_price']
    new_pricing = Pricing(pricing_name=pricing_name, pricing_location=pricing_location, pricing_duration=pricing_duration, pricing_price=pricing_price)
    db.session.add(new_pricing)
    db.session.commit()
    return redirect("/edit_pricing")

##SERVICES ROUTES
@app.route("/services")
@login_required
def services():
    services = get_services()
    return render_template("services.html", services=services)

@app.route("/edit_services", methods=['GET', 'POST'])
@login_required
def edit_services():
    services = get_services()
    return render_template("edit_services.html", services=services)

@app.route("/edit_services/save", methods=['POST'])
@login_required
def save_services():
    service_id = request.form['service_id']
    service_name = request.form['service_name']
    service_description = request.form['service_description']
    service = Service.query.filter_by(service_id=service_id).first()
    service.service_id = service_id
    service.service_name = service_name
    service.service_description = service_description
    db.session.commit() 
    return redirect("/edit_services")

@app.route("/edit_services/delete", methods=['POST'])
@login_required
def delete_service():
    service_id = request.form['service_id']
    service = Service.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect("/edit_services")

@app.route("/edit_services/add", methods=['POST'])
@login_required
def add_service():
    service_name = request.form['service_name']
    service_description = request.form['service_description']
    new_service = Service(service_name=service_name, service_description=service_description)
    db.session.add(new_service)
    db.session.commit()
    return redirect("/edit_services")

##HISTORY ROUTES


# @app.route("/edit_history/add", methods=['GET', 'POST'])
# def edit_history_add():
#     enhancements = Enhancement.query.all()
#     services = Service.query.all()
#     pricing = Pricing.query.all()
#     clients = Client.query.all()
#     return render_template("edit_history.html", enhancements=enhancements, services=services, pricing=pricing, clients=clients)

@app.route("/edit_history/add", methods=['POST', 'GET'])
@login_required
def edit_history_add():
    client_name = request.form.get('client_name')
    service_name= request.form.get('service_name')
    pricing_name = request.form.get('pricing_name')
    enhancement_name = request.form.get('enhancement_name')
    history_date = request.form.get('history_date')
    history_total_price = request.form.get('history_total_price') 
    new_history = History(client_name=client_name, service_name=service_name, pricing_name=pricing_name, enhancement_name=enhancement_name, history_date=history_date, history_total_price=history_total_price)
    db.session.add(new_history)
    db.session.commit()
    return redirect("/edit_history")


@app.route("/history")
@login_required
def history():
    history = get_history()
    history.sort(key=lambda x: datetime.strptime(x.history_date, '%m-%d-%Y'), reverse=True)
    return render_template("history.html", history=history)

@app.route("/edit_history", methods=['GET', 'POST'])
@login_required
def edit_history():

    history = get_history()
    history.sort(key=lambda x: datetime.strptime(x.history_date, '%m-%d-%Y'), reverse=True)

    client_names = db.session.query(Client.client_name).all()
    service_names = db.session.query(Service.service_name).all()
    pricing_names = db.session.query(Pricing.pricing_name).all()
    enhancement_names = db.session.query(Enhancement.enhancement_name).all()

    return render_template("edit_history.html", history=history, client_names=client_names, service_names=service_names, pricing_names=pricing_names, enhancement_names=enhancement_names)


@app.route("/edit_history/delete", methods=['POST'])
@login_required
def delete_history():
    history_id = request.form['history_id']
    history = History.query.get(history_id)
    db.session.delete(history)
    db.session.commit()
    return redirect("/edit_history")

@app.route("/edit_history/save", methods=['POST'])
@login_required
def save_history():
    history_id = request.form['history_id']
    client_name = request.form['client_name']
    service_name = request.form['service_name']
    enhancement_name = request.form['enhancement_name']
    history_date = request.form['history_date']
    history_total_price = request.form['history_total_price']
    history = History.query.filter_by(history_id=history_id).first()
    history.client_name = client_name
    history.service_name = service_name
    history.enhancement_name = enhancement_name
    history.history_date= history_date
    history.history_total_price = history_total_price
    db.session.commit() 
    return redirect("/edit_history")


#CLIENTS ROUTES
@app.route("/clients")
@login_required
def clients():
    clients = get_clients()
    return render_template("clients.html", clients=clients)

@app.route("/edit_clients", methods=['GET', 'POST'])
@login_required
def edit_clients():
    clients = get_clients()
    return render_template("edit_clients.html", clients=clients)

@app.route("/edit_clients/save", methods=['POST'])
@login_required
def save_clients():
    client_id = request.form['client_id']
    client_name = request.form['client_name']
    client_address = request.form['client_address']
    client_phonenumber = request.form['client_phonenumber']
    client = Client.query.filter_by(client_id=client_id).first()
    client.client_id = client_id
    client.client_name = client_name
    client.client_address = client_address
    client.client_phonenumber = client_phonenumber
    db.session.commit() 
    return redirect("/edit_clients")

@app.route("/edit_clients/delete", methods=['POST'])
@login_required
def delete_client():
    client_id = request.form['client_id']
    client = Client.query.get(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect("/edit_clients")

@app.route("/edit_clients/add", methods=['POST'])
@login_required
def add_client():
    client_name = request.form['client_name']
    client_address = request.form['client_address']
    client_phonenumber = request.form['client_phonenumber']
    new_client = Client(client_name=client_name, client_address=client_address, client_phonenumber=client_phonenumber)
    db.session.add(new_client)
    db.session.commit()
    return redirect("/edit_clients")

#ENHANCEMENTS ROUTES
@app.route("/enhancements")
@login_required
def enhancements():
    enhancements = get_enhancements()
    return render_template("enhancements.html", enhancements=enhancements)

@app.route("/edit_enhancements", methods=['GET', 'POST'])
@login_required
def edit_enhancements():
    enhancements = get_enhancements()
    return render_template("edit_enhancements.html", enhancements=enhancements)

@app.route("/edit_enhancements/save", methods=['POST'])
@login_required
def save_enhancements():
    enhancement_id = request.form['enhancement_id']
    enhancement_name = request.form['enhancement_name']
    enhancement_price = request.form['enhancement_price']
    enhancement_description = request.form['enhancement_description']
    enhancement = Enhancement.query.filter_by(enhancement_id=enhancement_id).first()
    enhancement.enhancement_id = enhancement_id
    enhancement.enhancement_name = enhancement_name
    enhancement.enhancement_price = enhancement_price
    enhancement.enhancement_description = enhancement_description
    db.session.commit() 
    return redirect("/edit_enhancements")

@app.route("/edit_enhancements/delete", methods=['POST'])
@login_required
def delete_enhancement():
    enhancement_id = request.form['enhancement_id']
    enhancement = Enhancement.query.get(enhancement_id)
    db.session.delete(enhancement)
    db.session.commit()
    return redirect("/edit_enhancements")

@app.route("/edit_enhancements/add", methods=['POST'])
@login_required
def add_enhancement():
    enhancement_name = request.form['enhancement_name']
    enhancement_price = request.form['enhancement_price']
    enhancement_description = request.form['enhancement_description']
    new_enhancement = Enhancement(enhancement_name=enhancement_name, enhancement_price=enhancement_price, enhancement_description=enhancement_description)
    db.session.add(new_enhancement)
    db.session.commit()
    return redirect("/edit_enhancements")



########################################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
