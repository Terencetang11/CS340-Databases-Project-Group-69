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


@webapp.route('/ingredients', methods=['POST','GET'])
#the name of this function is just a cosmetic thing
def browse_ingredients():
    db_connection = connect_to_database()

    # checks URL params for type = insert for adding a new ingredient and then executes query for adding new ingredient
    if request.args.get('type') == "insert":
        print("Add new ingredient!")
        ingredientName = request.form['ingredientName']
        isVegan = request.form['isVegan']
        inventory = request.form['inventory']

        query = 'INSERT INTO ingredients (ingredientName, isVegan, inventory) VALUES (%s,%s,%s)'
        data = (ingredientName, isVegan, inventory)
        execute_query(db_connection, query, data)

        print('Ingredient added!')

    # renders ingredients form with latest results from query
    print("Fetching and rendering ingredients web page")
    query = "SELECT ingredientID, ingredientName, isVegan, inventory FROM ingredients"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('ingredients.html', rows=result)


@webapp.route('/add_new_ingredient', methods=['POST','GET'])
def add_new_ingredient():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT ingredientID, ingredientName, isVegan, inventory from ingredients'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('ingredient_add_new.html', ingredients = result)
    elif request.method == 'POST':
        print("Add new ingredient!")
        ingredientName = request.form['ingredientName']
        isVegan = request.form['isVegan']
        inventory = request.form['inventory']

        query = 'INSERT INTO ingredients (ingredientName, isVegan, inventory) VALUES (%s,%s,%s)'
        data = (ingredientName, isVegan, inventory)
        execute_query(db_connection, query, data)
        return ('Ingredient added!')

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


@webapp.route('/add_new_menuItem', methods=['POST','GET'])
def add_new_menuItem():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT menuItemName, cuisineID, price from menuItems'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('menuItem_add_new.html', menuItems = result)
    elif request.method == 'POST':
        print("Add new Menu Item!")
        menuItemName = request.form['menuItemName']
        cuisineID = request.form['cuisineID']
        price = request.form['price']

        query = 'INSERT INTO menuItems (menuItemName, cuisineID, price) VALUES (%s,%s,%s)'
        data = (menuItemName, cuisineID, price)
        execute_query(db_connection, query, data)
        return ('Menu Item added!')


@webapp.route('/add_new_cuisine', methods=['POST','GET'])
def add_new_cuisine():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT cuisineName from cuisines'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('cuisine_add_new.html', cuisines = result)
    elif request.method == 'POST':
        print("Add new Cuisine!")
        cuisineName = request.form['cuisineName']

        query = 'INSERT INTO cuisines (cuisineName) VALUES (%s)'
        data = (cuisineName,)
        execute_query(db_connection, query, data)
        return ('Cuisine added!')

@webapp.route('/add_new_restaurantSchedule', methods=['POST','GET'])
def add_new_restaurantSchedule():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT dayofWeek, cuisineID from restaurantSchedule'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('restaurantSchedule_add_new.html', restaurantSchedule = result)
    elif request.method == 'POST':
        print("Add new entry to Restaurant Schedule!")
        dayofWeek = request.form['dayofWeek']
        cuisineID = request.form['cuisineID']

        query = 'INSERT INTO restaurantSchedule (dayofWeek, cuisineID) VALUES (%s,%s)'
        data = (dayofWeek, cuisineID)
        execute_query(db_connection, query, data)
        return ('Entry added!')

@webapp.route('/add_new_chef', methods=['POST','GET'])
def add_new_chef():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT firstName, lastName, cuisineID from chefs'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('chef_add_new.html', chefs = result)
    elif request.method == 'POST':
        print("Add new Chef!")
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        cuisineID = request.form['cuisineID']

        query = 'INSERT INTO chefs (firstName, lastName, cuisineID) VALUES (%s,%s,%s)'
        data = (firstName, lastName, cuisineID)
        execute_query(db_connection, query, data)
        return ('Entry added!')


@webapp.route('/add_new_chefSchedule', methods=['POST','GET'])
def add_new_chefSchedule():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT * from restaurantSchedule'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('chefSchedule_add_new.html', chefSchedule = result)
    elif request.method == 'POST':
        print("Add new entry to Chef Schedule!")
        dayofWeek = request.form['dayofWeek']
        chefID = request.form['chefID']

        query = 'INSERT INTO chefSchedule (dayofWeek, chefID) VALUES (%s,%s)'
        data = (dayofWeek, chefID)
        execute_query(db_connection, query, data)
        return ('Entry added!')

@webapp.route('/')
def index():
    return render_template('index.html')

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

@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)



