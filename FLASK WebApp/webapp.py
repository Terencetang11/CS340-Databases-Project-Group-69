from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!"

@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)

@webapp.route('/home')
def home():
    db_connection = connect_to_database()
    query = "DROP TABLE IF EXISTS diagnostic;"
    execute_query(db_connection, query)
    query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
    execute_query(db_connection, query)
    query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
    execute_query(db_connection, query)
    query = "SELECT * from diagnostic;"
    result = execute_query(db_connection, query)
    for r in result:
        print(f"{r[0]}, {r[1]}")
    return render_template('home.html', result = result)

@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/ingredients')
#the name of this function is just a cosmetic thing
def browse_ingredients():
    print("Fetching and rendering ingredients web page")
    db_connection = connect_to_database()
    query = "SELECT ingredientID, ingredientName, isVegan, inventory FROM ingredients"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('ingredients.html', rows=result)

@webapp.route('/menuItems')
#the name of this function is just a cosmetic thing
def browse_menuItems():
    print("Fetching and rendering Menu Items web page")
    db_connection = connect_to_database()
    query = "SELECT menuItemID, menuItemName, menuItems.cuisineID, cuisines.cuisineName, price FROM menuItems LEFT JOIN cuisines ON cuisines.cuisineID = menuItems.cuisineID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('menuItems.html', rows=result)

@webapp.route('/cuisines')
#the name of this function is just a cosmetic thing
def browse_cuisines():
    print("Fetching and rendering Cuisines web page")
    db_connection = connect_to_database()
    query = "SELECT cuisineID, cuisineName FROM cuisines"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('cuisines.html', rows=result)

@webapp.route('/restaurantSchedule')
#the name of this function is just a cosmetic thing
def browse_restuarantSchedule():
    print("Fetching and rendering Restaurant Schedule web page")
    db_connection = connect_to_database()
    query = "SELECT dayofWeek, restaurantSchedule.cuisineID, cuisines.cuisineName FROM restaurantSchedule LEFT JOIN cuisines ON cuisines.cuisineID = restaurantSchedule.cuisineID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('restaurantSchedule.html', rows=result)

@webapp.route('/chefs')
#the name of this function is just a cosmetic thing
def browse_chefs():
    print("Fetching and rendering Chefs web page")
    db_connection = connect_to_database()
    query = "SELECT chefID, firstName, lastName, chefs.cuisineID, cuisines.cuisineName FROM chefs LEFT JOIN cuisines ON cuisines.cuisineID = chefs.cuisineID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('chefs.html', rows=result)

@webapp.route('/chefSchedule')
#the name of this function is just a cosmetic thing
def browse_chefSchedule():
    print("Fetching and rendering Chef Schedule web page")
    db_connection = connect_to_database()
    query = "SELECT dayofWeek, chefSchedule.chefID, chefs.firstName, chefs.lastName FROM chefSchedule LEFT JOIN chefs ON chefs.chefID = chefSchedule.chefID ORDER BY chefSchedule.chefID ASC"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('chefSchedule.html', rows=result)


