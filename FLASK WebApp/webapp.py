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
# completed
def browse_ingredients():
    db_connection = connect_to_database()

    # checks URL params for type = INSERT for adding a new ingredient and then executes query for adding new ingredient
    if request.args.get('type') == "insert":
        print("Add new ingredient!")
        print(request.form)
        ingredientName = request.form['ingredientName']
        isVegan = request.form['isVegan']
        inventory = request.form['inventory']

        query = 'INSERT INTO ingredients (ingredientName, isVegan, inventory) VALUES (%s,%s,%s)'
        data = (ingredientName, isVegan, inventory)
        execute_query(db_connection, query, data)
        print('Ingredient added!')

    # checks URL params for type = DELETE for deleting an existing ingredient and then executes query to DB
    elif request.args.get('type') == "delete":
        print("Deletes an ingredient!")
        print("id = " + request.args.get('id'))
        query = 'DELETE FROM ingredients WHERE ingredientID = ' + request.args.get('id')
        execute_query(db_connection, query)
        print('Ingredient deleted')

    # checks URL params for type = EDIT for updating an existing ingredient and then executes query to DB
    elif request.args.get('type') == "edit":
        print("Edit an ingredient!")
        print(request.form)
        ingredientID = request.form['ingredientID']
        ingredientName = request.form['ingredientName']
        isVegan = request.form['isVegan']
        inventory = request.form['inventory']

        query = "UPDATE ingredients SET ingredientName = %s, isVegan = %s, inventory = %s WHERE ingredientID = %s"
        data = (ingredientName, isVegan, inventory, ingredientID)
        execute_query(db_connection, query, data)
        print('Ingredient Updated!')

    # renders ingredients form with latest results from query
    print("Fetching and rendering ingredients web page")
    query = "SELECT ingredientID, ingredientName, isVegan, inventory FROM ingredients"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('ingredients.html', rows=result)


@webapp.route('/menuItems')
def browse_menuItems():
    print("Fetching and rendering Menu Items web page")
    db_connection = connect_to_database()
    query = "SELECT menuItemID, menuItemName, menuItems.cuisineID, cuisines.cuisineName, price FROM menuItems LEFT JOIN cuisines ON cuisines.cuisineID = menuItems.cuisineID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('menuItems.html', rows=result)


@webapp.route('/cuisines', methods=['POST','GET'])
# completed
def browse_cuisines():
    db_connection = connect_to_database()

    # checks URL params for type = INSERT for adding a new item and then executes query for adding new item
    if request.args.get('type') == "insert":
        print("Add new Cuisine!")
        print(request.form)
        cuisineName = request.form['cuisineName']

        query = 'INSERT INTO cuisines (cuisineName) VALUES (%s)'
        data = (cuisineName,)
        execute_query(db_connection, query, data)
        print('Cuisine added!')

    # checks URL params for type = DELETE for deleting an existing item and then executes query to DB
    elif request.args.get('type') == "delete":
        print("Deletes a cuisine!")
        print("id = " + request.args.get('id'))
        query = 'DELETE FROM cuisines WHERE cuisineID = ' + request.args.get('id')
        execute_query(db_connection, query)
        print('Cuisine deleted')

    # checks URL params for type = EDIT for updating an existing item and then executes query to DB
    elif request.args.get('type') == "edit":
        print("Edit a cuisine!")
        print(request.form)
        cuisineID = request.form['cuisineID']
        cuisineName = request.form['cuisineName']

        query = "UPDATE cuisines SET cuisineName = %s WHERE cuisineID = %s"
        data = (cuisineName, cuisineID)
        execute_query(db_connection, query, data)
        print('Cuisine Updated!')

    print("Fetching and rendering Cuisines web page")
    query = "SELECT cuisineID, cuisineName FROM cuisines"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('cuisines.html', rows=result)


@webapp.route('/restaurantSchedule')
def browse_restuarantSchedule():
    print("Fetching and rendering Restaurant Schedule web page")
    db_connection = connect_to_database()
    query = "SELECT dayofWeek, restaurantSchedule.cuisineID, cuisines.cuisineName FROM restaurantSchedule LEFT JOIN cuisines ON cuisines.cuisineID = restaurantSchedule.cuisineID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('restaurantSchedule.html', rows=result)


@webapp.route('/chefs', methods=['POST','GET'])
# completed
def browse_chefs():
    db_connection = connect_to_database()

    # data validation to ensure that a valid foreign key is input (cuisineID in this case)
    if request.method == "POST":
        query = 'SELECT cuisineID FROM cuisines WHERE cuisineName = "' + str(request.form['cuisineName']) + '"'
        results = execute_query(db_connection, query).fetchall()

        if len(results) != 0:
            print('Cuisine exists!')
            cuisineID = results[0]
        else:
            print('Cuisine does not exists!')
            result = ('/chefs',)
            return render_template('cuisine_error.html', rows=result)
    try:
        # data validation: queries for existing list of cuisines for use in foreign key selection
        query = 'SELECT cuisineName FROM cuisines'
        cuisines = execute_query(db_connection, query).fetchall()
        print(cuisines)

        # checks URL params for type = INSERT for adding a new chef and then executes query to DB
        if request.args.get('type') == "insert":
            print("Add new Chef!")
            print(request.form)
            chefFName = request.form['chefFirstName']
            chefLName = request.form['chefLastName']

            query = 'INSERT INTO chefs (firstName, lastName, cuisineID) VALUES (%s,%s,%s)'
            data = (chefFName, chefLName, cuisineID)
            execute_query(db_connection, query, data)
            print('Chef added!')

        # checks URL params for type = DELETE for deleting an existing chef and then executes query to DB
        elif request.args.get('type') == "delete":
            print("Deletes a Chef!")
            print("id = " + request.args.get('id'))
            query = 'DELETE FROM chefs WHERE chefID = ' + request.args.get('id')
            execute_query(db_connection, query)
            print('Chef deleted')

        # checks URL params for type = EDIT for updating an existing chef and then executes query to DB
        elif request.args.get('type') == "edit":
            print("Edit a Chef!")
            print(request.form)
            chefID = request.form['chefID']
            chefFName = request.form['chefFirstName']
            chefLName = request.form['chefLastName']

            query = "UPDATE chefs SET firstName = %s, lastName = %s, cuisineID = %s WHERE chefID = %s"
            data = (chefFName, chefLName, cuisineID, chefID)
            execute_query(db_connection, query, data)
            print('Chef Updated!')

        print("Fetching and rendering Chefs web page")
        query = "SELECT chefID, firstName, lastName, chefs.cuisineID, cuisines.cuisineName FROM chefs LEFT JOIN cuisines ON cuisines.cuisineID = chefs.cuisineID"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('chefs.html', rows=result, cuisines=cuisines)
    
    except:
        print('Cuisine does not exists!')
        result = ('/chefs',)
        return render_template('cuisine_error.html', rows=result)

@webapp.route('/chefSchedule')
def browse_chefSchedule():
    print("Fetching and rendering Chef Schedule web page")
    db_connection = connect_to_database()
    query = "SELECT dayofWeek, chefSchedule.chefID, chefs.firstName, chefs.lastName FROM chefSchedule LEFT JOIN chefs ON chefs.chefID = chefSchedule.chefID ORDER BY chefSchedule.chefID ASC"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('chefSchedule.html', rows=result)


@webapp.route('/menuItemIngredients')
def browse_menuItemIngredients():
    print("Fetching and rendering Menu Item Ingredients web page")
    db_connection = connect_to_database()
    query = "SELECT menuItemIngredients.menuItemID, menuItems.menuItemName, menuItemIngredients.ingredientID, ingredients.ingredientName, ingredients.inventory FROM menuItemIngredients INNER JOIN menuItems ON menuItemIngredients.menuItemID = menuItems.menuItemID INNER JOIN ingredients ON menuItemIngredients.ingredientID = ingredients.ingredientID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('menuItemIngredients.html', rows=result)


@webapp.route('/add_new_menuItemIngredient', methods=['POST','GET'])
def add_new_menuItemIngredient():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT menuItemID, ingredientID from menuItemIngredients'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('menuItemIngredient_add_new.html', menuItemIngredients = result)
    elif request.method == 'POST':
        print("Add new Menu Item Ingredient!")
        menuItemID = request.form['menuItemID']
        ingredientID = request.form['ingredientID']

        query = 'INSERT INTO menuItemIngredients (menuItemID, ingredientID) VALUES (%s,%s)'
        data = (menuItemID, ingredientID)
        execute_query(db_connection, query, data)
        return ('Menu Item Ingredient added!')


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
    query = "SELECT * from chefs"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)



