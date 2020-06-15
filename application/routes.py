from application import app, db, bcrypt,mail
from application.forms import LoginForm, RegisterationForm
from application.models import User, Customer
from flask import render_template, redirect, flash, url_for, session, request
from flask_mail import Message
from application.utils import mail_send

@app.route("/",methods=["GET","POST"])
def home():
	if request.method == "POST":
		print("hello")
		fullname = request.form.get('fullname')
		email = request.form.get('email')
		message = request.form.get('message')

		value = mail_send(fullname,email,message)
		return value
	else:
		return render_template("home.html",title="Moody Bank",role=session.get('ROLE'))


@app.route("/login", methods=['GET', 'POST'])
def login():
	if session.get('USER_ID'):
		return redirect(url_for('home'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(user_id=form.username.data).first()
			if bcrypt.check_password_hash(user.password, form.password.data):
				flash("Successfully logged in!!!", category="success")
				session['USER_ID'] = user.user_id
				session['ROLE'] = user.role
				return redirect('home.html', title="Home", role=session.get('ROLE'))
			else:
				flash("Wrong password entered!!!", category="danger")
		else:
			flash("Wrong username entered!!!", category="danger")
		return render_template("login.html", title="Login", form=form)
  
 
@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        customer = Customer(ssn=form.ssn_id.data,cust_id=form.cust_id.data,cust_name=form.cust_name.data,
                           cust_address=form.address.data,cust_contact = form.contact.data,cust_age=form.cust_age.data,cust_state=form.state.data,cust_city=form.city.data)
        db.session.add(customer)
        db.session.commit()
        return redirect("/register")
    return render_template("register.html",form=form)

