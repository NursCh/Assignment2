from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import text
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:San1209@localhost/assignment2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aboba'
db = SQLAlchemy(app)


@app.route('/MainPage')
def MainPage():
    if 'user_id' in session:
        
        return render_template("index.html")
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))


@app.route('/')
@app.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        query = text("SELECT * FROM public.user WHERE email=:email")
        user = db.session.execute(query, {"email": email}).fetchone()
        if user and user.password == password:
            session['user_id'] = user.user_id
            flash('Login successful!', 'success')
            return redirect(url_for('MainPage'))
        else: 
            flash('Login failed.','danger')

    return render_template('login.html')

@app.route('/delete', methods =['GET','POST'])
def delete():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = text("DELETE FROM public.user WHERE email=:email")
        user = db.session.execute(query, {"email": email})
        if user:
            db.session.commit()
            return redirect(url_for('login'))
        else: 
            flash('delete unsucessful')
    return render_template('delete.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        given_name = request.form['given_name']
        surname = request.form['surname']
        city = request.form['city']
        phone_number = request.form['phone_number']
        profile_description = request.form['profile_description']
        password = request.form['password']
        user_type = request.form['user_type']
        
        query = text("SELECT * FROM public.user WHERE email=:email")
        user = db.session.execute(query, {"email": email}).fetchone()
        if user:
            if user.email == email:
                flash('Email is already registered. Please use a different email.', 'danger')
                return redirect(url_for('register'))


        query = text( "INSERT INTO public.user (email, given_name, surname, city, phone_number, profile_description, password) " 
                     "VALUES (:email, :given_name, :surname, :city, :phone_number, :profile_description, :password)"
                     "RETURNING user_id" )
        result = db.session.execute(
            query,
            {
                "email": email,
                "given_name": given_name,
                "surname": surname,
                "city": city,
                "phone_number": phone_number,
                "profile_description": profile_description,
                "password": password,
            }
        )
        
        user_id = result.scalar() 
    
        if (user_type == 'caregiver'):
            photo = request.form['photo']
            gender = request.form['gender']
            caregiving_type = request.form['caregiving_type']
            hourly_rate = float(request.form['hourly_rate'])
            caregiver_insert_query = text(
                "INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate)"
                "VALUES (:caregiver_user_id, :photo, :gender, :caregiving_type, :hourly_rate)"
                )
            db.session.execute(caregiver_insert_query,
                                    { 
                                     'caregiver_user_id': user_id,
                                     'photo': photo,
                                     'gender': gender,
                                     'caregiving_type': caregiving_type,
                                     'hourly_rate': hourly_rate,
                                    }
                               )

            db.session.commit()

        elif(user_type == 'member'):
            house_rules = request.form['house_rules']
            house_number = request.form['house_number']
            street = request.form['street']
            town = request.form['town']

            member_insert_query = text(
                "INSERT INTO member (member_user_id, house_rules)"
                "VALUES (:member_user_id, :house_rules)"
                )
            db.session.execute(member_insert_query,
                               {
                                   'member_user_id': user_id,
                                   'house_rules': house_rules,
                               }
                               )
            address_query = (
              text(  "INSERT INTO address (member_user_id, house_number, street, town) "
                   "VALUES(:member_user_id, :house_number,:street,:town)")
            )
            db.session.execute(address_query,
                               {
                                   'member_user_id':user_id,
                                   'house_number':house_number,
                                   'street':street,
                                   'town':town,
                               }
                               )
            db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/Caregiver_info/<int:caregiver_user_id>')
def display_caregiver(caregiver_user_id):
    caregiver_query = text("""
        SELECT caregiver_user_id, photo, gender, caregiving_type, hourly_rate
        FROM caregiver
        WHERE caregiver_user_id = :caregiver_user_id
    """)
    caregiver_result = db.session.execute(caregiver_query,{'caregiver_user_id':caregiver_user_id }).first()

    user_query = text("""
        SELECT user_id, email, given_name, surname, city, phone_number, profile_description
        FROM public.user
        WHERE user_id = :caregiver_id
    """)
    user_result = db.session.execute(user_query, {'caregiver_id':caregiver_user_id}).first()

    return render_template('caregiver_profile.html', caregiver=caregiver_result, user=user_result)

@app.route('/Member_info/<int:member_user_id>')
def display_member(member_user_id):
    member_query = text("""
        SELECT member_user_id, house_rules
        FROM member
        WHERE member_user_id = :member_user_id
    """)
    member_result = db.session.execute(member_query,{'member_user_id':member_user_id }).first()
    address_query = text("""
    SELECT member_user_id, house_number, street, town
    FROM address
    WHERE member_user_id = :member_user_id
    """)
    address_result = db.session.execute(address_query,{'member_user_id':member_user_id }).first()

    user_query = text("""
        SELECT user_id, email, given_name, surname, city, phone_number, profile_description
        FROM public.user
        WHERE user_id = :member_id
    """)

    user_result = db.session.execute(user_query, {'member_id':member_user_id}).first()
    return render_template('member_profile.html', member=member_result, user=user_result, address = address_result)


@app.before_request
def before_request():
    allowed_routes = ['login', 'check_database','logout','register']  # Add other routes that don't require login

    if request.endpoint not in allowed_routes and 'user_id' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

@app.route('/check_database')
def check_database():
    try:
        # Perform a simple query to check if the User table exists
        result = db.session.execute(text("SELECT * FROM public.user LIMIT 1")).fetchone()

        if result:
            return f"Connected to the correct database with User table. Example result: {result}"
        else:
            return "User table not found. Check your database configuration."

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/create_user',methods =['POST'])
def create_user():
    conn = psycopg2.connect(database = 'assignment2', user ='postgres', password= 'San1209', host = 'localhost', port = '5432')
    cur = conn.cursor()
    email = request.form['email']
    given_name = request.form['given_name']
    surname = request.form['surname']
    city = request.form['city']
    phone_number = request.form['phone_number']
    profile_description = request.form['profile_description']
    password = request.form['password']

    cur.execute( '''INSERT INTO user \
            (email, given_name, surname, city, phone_number, profile_description, password) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (email,given_name,surname, city, phone_number, profile_description, password))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))
#@app.route('/Jobs')
#def MyinfoPage():
#    return render_template("Myinfo.html")
@app.route('/Myinfo')
def MyinfoPage():
    return render_template("Myinfo.html")

if __name__ == "__main__":
    app.run(debug = True)
