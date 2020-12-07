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

    # try and except structure used for capturing errors and rendering an error page
    try:
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

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/ingredients')


@webapp.route('/menuItems', methods=['POST','GET'])
def browse_menuItems():
    db_connection = connect_to_database()

    # try and except structure used for capturing errors and rendering an error page
    try:
        # data validation: queries for existing list of ingredients for use in foreign key selection
        query = 'SELECT ingredientID, ingredientName FROM ingredients'
        ingredients = execute_query(db_connection, query).fetchall()
        print(ingredients)

        # data validation: queries for existing list of cuisines for use in foreign key selection
        query = 'SELECT cuisineID, cuisineName FROM cuisines'
        cuisines = execute_query(db_connection, query).fetchall()
        print(cuisines)

        # checks URL params for type = INSERT for adding a new ingredient and then executes query for adding new ingredient
        if request.args.get('type') == "insert":
            print("Add new menu item!")
            print(request.form)
            menuItemName = request.form['menuItemName']
            cuisineID = request.form['cuisineName']
            price = request.form['price']
            mainIngredient = request.form['ingredientName']

            query = 'INSERT INTO menuItems (menuItemName, cuisineID, price) VALUES (%s,%s,%s)'
            data = (menuItemName, cuisineID, price)
            execute_query(db_connection, query, data)
            print('Menu Item added!')

            query = 'SELECT menuItemID FROM menuItems where menuItemName = %s AND cuisineID = %s AND price = %s'
            menuItemID = execute_query(db_connection, query, data).fetchall()

            query = 'INSERT INTO menuItemIngredients (menuItemID, ingredientID) VALUES (%s,%s)'
            data = (menuItemID, mainIngredient)
            execute_query(db_connection, query, data)
            print('Menu Item Ingredient added!')

        # checks URL params for type = DELETE for deleting an existing ingredient and then executes query to DB
        elif request.args.get('type') == "delete":
            print("Deletes a menu item!")
            print("id = " + request.args.get('id'))
            query = 'DELETE FROM menuItems WHERE menuItemID = ' + request.args.get('id')
            execute_query(db_connection, query)
            print('Menu item deleted')

        # checks URL params for type = EDIT for updating an existing ingredient and then executes query to DB
        elif request.args.get('type') == "edit":
            print("Edit a menu item!")
            print(request.form)
            menuItemID = request.form['menuItemID']
            menuItemName = request.form['menuItemName']
            cuisineID = request.form['cuisineName']
            price = request.form['price']

            query = "UPDATE menuItems SET menuItemName = %s, cuisineID = %s, price = %s WHERE menuItemID = %s"
            data = (menuItemName, cuisineID, price, menuItemID)
            execute_query(db_connection, query, data)
            print('Menu Item Updated!')

        print("Fetching and rendering Menu Items web page")
        query = "SELECT menuItemID, menuItemName, menuItems.cuisineID, cuisines.cuisineName, price FROM menuItems LEFT JOIN cuisines ON cuisines.cuisineID = menuItems.cuisineID"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('menuItems.html', rows=result, cuisines=cuisines, ingredients=ingredients)

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/menuItems')


@webapp.route('/menuItemIngredients', methods=['POST','GET'])
def browse_menuItemIngredients():
    db_connection = connect_to_database()

    # data validation: queries for existing list of ingredients for use in foreign key selection
    query = 'SELECT ingredientID, ingredientName FROM ingredients'
    ingredients = execute_query(db_connection, query).fetchall()
    print(ingredients)

    # data validation: queries for existing list of menuItems for use in foreign key selection
    query = 'SELECT menuItemID, menuItemName FROM menuItems'
    menuItems = execute_query(db_connection, query).fetchall()
    print(menuItems)

    # checks URL params for type = INSERT for adding a new ingredient and then executes query for adding new ingredient
    if request.args.get('type') == "insert":
        print("Add new menu item ingredient combination!")
        print(request.form)
        menuItemID = request.form['menuItemID']
        ingredientID = request.form['ingredientID']

        query = 'INSERT INTO menuItemIngredients (menuItemID, ingredientID) VALUES (%s, %s)'
        data = (menuItemID, ingredientID)
        execute_query(db_connection, query, data)
        print('Menu Item Ingredient combo added!')

    # checks URL params for type = DELETE for deleting an existing ingredient and then executes query to DB
    elif request.args.get('type') == "delete":
        print("Deletes a menu item ingredient combo!")
        print("menuItemID = " + request.args.get('menuItemID'))
        print("ingredientID = " + request.args.get('ingredientID'))
        query = 'DELETE FROM menuItemIngredients WHERE menuItemID = ' + str(request.args.get('menuItemID')) + ' AND ingredientID = ' + str(request.args.get('ingredientID'))
        execute_query(db_connection, query)
        print('Menu item deleted')

    print("Fetching and rendering Menu Item Ingredients web page")
    query = "SELECT menuItemIngredients.menuItemID, menuItems.menuItemName, menuItemIngredients.ingredientID, ingredients.ingredientName, ingredients.inventory FROM menuItemIngredients INNER JOIN menuItems ON menuItemIngredients.menuItemID = menuItems.menuItemID INNER JOIN ingredients ON menuItemIngredients.ingredientID = ingredients.ingredientID"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('menuItemIngredients.html', rows=result, ingredients=ingredients, menuItems=menuItems)


@webapp.route('/cuisines', methods=['POST','GET'])
# completed
def browse_cuisines():
    db_connection = connect_to_database()

    # try and except structure used for capturing errors and rendering an error page
    try:
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

            # deletes relevant chef schedules where restaurant schedule cuisine is now NULL
            query = "SELECT dayofWeek FROM restaurantSchedule WHERE cuisineID IS NULL"
            days = execute_query(db_connection, query).fetchall()
            print(days)
            for day in days:
                query = 'DELETE FROM chefSchedule WHERE dayofWeek = "' + day[0] + '"'
                execute_query(db_connection, query)
            print('Chef Schedule updated')

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

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/cuisines')


@webapp.route('/restaurantSchedule', methods=['POST','GET'])
def browse_restuarantSchedule():
    db_connection = connect_to_database()

    # try and except structure used for capturing errors and rendering an error page
    try:
        # data validation: queries for existing list of cuisines for use in foreign key selection
        query = 'SELECT cuisineName FROM cuisines'
        cuisines = execute_query(db_connection, query).fetchall()
        print(cuisines)

        # grabs cuisine ID for given cuisine name input
        if request.method == "POST":
            query = 'SELECT cuisineID FROM cuisines WHERE cuisineName = "' + str(request.form['cuisineName']) + '"'
            cuisineID = execute_query(db_connection, query).fetchall()[0]

        # checks URL params for type = INSERT for adding a new restaurantschedule and then executes query to DB
        if request.args.get('type') == "insert":
            print("Add new RestaurantSchedule!")
            print(request.form)
            dayOfWeek = request.form['dayOfWeek']

            query = 'INSERT INTO restaurantSchedule (dayofWeek, cuisineID) VALUES (%s,%s)'
            data = (dayOfWeek, cuisineID)
            execute_query(db_connection, query, data)
            print('RestaurantSchedule added!')

        # checks URL params for type = DELETE for deleting an existing restaurantschedule and then executes query to DB
        elif request.args.get('type') == "delete":
            print("Deletes a RestaurantSchedule entry!")
            print("id = " + request.args.get('id'))
            query = 'DELETE FROM restaurantSchedule WHERE dayofWeek = "' + request.args.get('id') + '"'
            execute_query(db_connection, query)
            print('RestaurantSchedule deleted')

        # checks URL params for type = EDIT for updating an existing RestaurantSchedule and then executes query to DB
        elif request.args.get('type') == "edit":
            print("Edit a RestaurantSchedule!")
            print(request.form)
            dayOfWeek = request.form['dayOfWeek']

            query = "UPDATE restaurantSchedule SET cuisineID = %s  WHERE dayofWeek = %s"
            data = (cuisineID, dayOfWeek)
            execute_query(db_connection, query, data)
            print('RestaurantSchedule Updated!')

            query = 'DELETE FROM chefSchedule WHERE dayofWeek = "' + dayOfWeek + '"'
            execute_query(db_connection, query)
            print('ChefSchedule Updated!')

        print("Fetching and rendering Restaurant Schedule web page")
        query = "SELECT dayofWeek, restaurantSchedule.cuisineID, cuisines.cuisineName FROM restaurantSchedule LEFT JOIN cuisines ON cuisines.cuisineID = restaurantSchedule.cuisineID ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('restaurantSchedule.html', rows=result, cuisines=cuisines)

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/restaurantSchedule')


@webapp.route('/chefs', methods=['POST','GET'])
# completed
def browse_chefs():
    db_connection = connect_to_database()

    # try and except structure used for capturing errors and rendering an error page
    try:
        # data validation: queries for existing list of cuisines for use in foreign key selection
        query = 'SELECT cuisineName FROM cuisines'
        cuisines = execute_query(db_connection, query).fetchall()
        print(cuisines)

        # grabs cuisine ID for given cuisine name input
        if request.method == "POST":
            query = 'SELECT cuisineID FROM cuisines WHERE cuisineName = "' + str(request.form['cuisineName']) + '"'
            cuisineID = execute_query(db_connection, query).fetchall()[0]

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

            query = 'DELETE FROM chefSchedule WHERE chefID = "' + chefID + '"'
            execute_query(db_connection, query)
            print('ChefSchedule Updated!')

        print("Fetching and rendering Chefs web page")
        query = "SELECT chefID, firstName, lastName, chefs.cuisineID, cuisines.cuisineName FROM chefs LEFT JOIN cuisines ON cuisines.cuisineID = chefs.cuisineID"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('chefs.html', rows=result, cuisines=cuisines)

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/chefs')


@webapp.route('/chefSchedule', methods=['POST','GET'])
def browse_chefSchedule():
    db_connection = connect_to_database()

    # try and except structure used for capturing errors and rendering an error page
    try:
        # data validation: queries for existing list of cuisines for use in foreign key selection
        query = "SELECT * FROM restaurantSchedule ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')"
        restaurantSchedule = execute_query(db_connection, query).fetchall()
        print(restaurantSchedule)

        # data validation: queries for existing list of chefs for use in foreign key selection
        query = 'SELECT * FROM chefs'
        chefs = execute_query(db_connection, query).fetchall()
        print(chefs)

        # checks URL params for type = INSERT for adding a new chefSchedule and then executes query to DB
        if request.args.get('type') == "insert":
            print("Add new ChefSchedule!")
            print(request.form)
            dayOfWeek = request.form['dayOfWeek']
            chefID = request.form['chefID']
            print(chefID)

            query = 'INSERT INTO chefSchedule (dayofWeek, chefID) VALUES (%s,%s)'
            data = (dayOfWeek, chefID)
            execute_query(db_connection, query, data)
            print('ChefSchedule added!')

        # checks URL params for type = DELETE for deleting an existing chefSchedule and then executes query to DB
        elif request.args.get('type') == "delete":
            print("Deletes a ChefSchedule entry!")
            print("dayofWeek = " + request.args.get('dayofWeek'))
            print("chefID = " + request.args.get('chefID'))
            query = 'DELETE FROM chefSchedule WHERE dayofWeek = "' + request.args.get('dayofWeek') + '" AND chefID = "' + request.args.get('chefID') + '"'
            execute_query(db_connection, query)
            print('RestaurantSchedule deleted')

        print("Fetching and rendering Chef Schedule web page")
        query = "SELECT dayofWeek, chefSchedule.chefID, chefs.firstName, chefs.lastName FROM chefSchedule LEFT JOIN chefs ON chefs.chefID = chefSchedule.chefID ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('chefSchedule.html', rows=result, restaurantSchedule=restaurantSchedule, chefs=chefs)

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/chefSchedule')


@webapp.route('/', methods=['POST','GET'])
def index():
    db_connection = connect_to_database()

    # try and except structure used for capturing errors and rendering an error page
    try:
        if request.args.get('type') == 'reset':
            with open('DDL_Queries.txt', 'r') as file:
                data = file.read().replace('\n', '')

            query = ''
            for char in data:
                if char == ';':
                    data = data[1:]
                    execute_query(db_connection, query)
                    query = ''
                else:
                    query += char
                    data = data[1:]
            print('Database has been reset')

        print("Fetching and rendering Index web page")
        query = "SELECT restaurantSchedule.dayofWeek, cuisines.cuisineName, (GROUP_CONCAT(CONCAT_WS(' ', chefs.firstName, chefs.lastName) SEPARATOR ', ')) FROM restaurantSchedule INNER JOIN cuisines on restaurantSchedule.cuisineID = cuisines.cuisineID INNER JOIN chefs on cuisines.cuisineID = chefs.cuisineID GROUP BY restaurantSchedule.dayofWeek ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('index.html', rows=result)

    except:
        print('Error has occurred!')
        return render_template('error.html', prev='/')


@webapp.route('/index_search', methods=['GET', 'POST'])
def index_search():
    print("Searching user query")
    db_connection = connect_to_database()
    if request.method =='GET':
        return render_template('index_search.html')
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        print(firstName, lastName)
        query="SELECT restaurantSchedule.dayofWeek, CONCAT_WS(' ', chefs.firstName, chefs.lastName) FROM restaurantSchedule INNER JOIN cuisines on restaurantSchedule.cuisineID = cuisines.cuisineID INNER JOIN chefs ON cuisines.cuisineID = chefs.cuisineID WHERE chefs.firstName = (%s) AND chefs.lastName = (%s)"
        data = (firstName, lastName)
        result = execute_query(db_connection, query, data).fetchall()
        return render_template('index_search.html', rows=result)

@webapp.route('/ingredients_search', methods=['GET', 'POST'])
def ingredients_search():
    print("Searching user query")
    db_connection = connect_to_database()
    if request.method =='GET':
        return render_template('ingredients_search.html')
    if request.method == 'POST':
        ingredientName = request.form['ingredientName']
        inventory = request.form['inventory']
        print(ingredientName, inventory)

        # Checking for what parameters User entered and creating query accordingly
        if ingredientName != '' and inventory != '':
            data = (ingredientName, inventory)
            query = "SELECT * FROM ingredients WHERE ingredients.ingredientName = (%s) AND ingredients.inventory = (%s)"
            result = execute_query(db_connection, query, data).fetchall()
        elif ingredientName == '' and inventory != '':
            data = inventory,
            query = "SELECT * FROM ingredients WHERE ingredients.inventory = %s"
            result = execute_query(db_connection, query, data).fetchall()
        elif ingredientName != '' and inventory == '':
            data = ingredientName,
            query = "SELECT * FROM ingredients WHERE ingredients.ingredientName = %s"
            result = execute_query(db_connection, query, data).fetchall()
        else:
            query = "SELECT * FROM ingredients"
            result = execute_query(db_connection, query).fetchall()
        return render_template('ingredients_search.html', rows=result)


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



