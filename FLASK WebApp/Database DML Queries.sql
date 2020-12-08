----- Index Table -----

-- SELECT statement for Weekly Schedule
SELECT restaurantSchedule.dayofWeek, 
cuisines.cuisineName, 
(GROUP_CONCAT(CONCAT_WS(' ', chefs.firstName, chefs.lastName) SEPARATOR ', ')) 
FROM restaurantSchedule 
INNER JOIN cuisines on restaurantSchedule.cuisineID = cuisines.cuisineID 
INNER JOIN chefs on cuisines.cuisineID = chefs.cuisineID 
GROUP BY restaurantSchedule.dayofWeek 
ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

-- SELECT statement for search entry for Weekly Schedule
SELECT restaurantSchedule.dayofWeek, 
CONCAT_WS(' ', chefs.firstName, chefs.lastName) 
FROM restaurantSchedule 
INNER JOIN cuisines on restaurantSchedule.cuisineID = cuisines.cuisineID 
INNER JOIN chefs ON cuisines.cuisineID = chefs.cuisineID 
WHERE chefs.firstName = (%s) AND chefs.lastName = (%s)


----- Ingredients Table -----

-- SELECT statement
SELECT ingredientID, 
ingredientName, 
isVegan, 
inventory 
FROM ingredients

-- INSERT statement
INSERT INTO ingredients (ingredientName, isVegan, inventory)
VALUES (%s,%s,%s)

-- UPDATE statement
UPDATE ingredients 
SET ingredientName = %s, isVegan = %s, inventory = %s 
WHERE ingredientID = %s

-- DELETE statement
DELETE FROM ingredients 
WHERE ingredientID = %



----- Menu Items Table -----

-- SELECT statement
SELECT menuItemID, 
menuItemName, 
menuItems.cuisineID, 
cuisines.cuisineName, 
price 
FROM menuItems 
LEFT JOIN cuisines ON cuisines.cuisineID = menuItems.cuisineID 

-- INSERT statement
-- Step 1: Inserting into Menu Item Table
INSERT INTO menuItems (menuItemName, cuisineID, price) 
VALUES (%s,%s,%s)
-- Step 2: Selecting new Menu Item for Inserting into Menu Item Ingredients Table
SELECT menuItemID 
FROM menuItems 
where menuItemName = %s AND cuisineID = %s AND price = %s
-- Step 3: Inserting query result into Menu Item Ingredients Table
INSERT INTO menuItemIngredients (menuItemID, ingredientID) 
VALUES (%s,%s)

-- UPDATE statement
UPDATE menuItems 
SET menuItemName = %s, 
cuisineID = %s, 
price = %s 
WHERE menuItemID = %s

-- DELETE statement
DELETE FROM menuItems 
WHERE menuItemID = %s


----- Menu Item Ingredients -----

-- SELECT statement
SELECT menuItemIngredients.menuItemID, 
menuItems.menuItemName, 
menuItemIngredients.ingredientID, 
ingredients.ingredientName, 
ingredients.inventory 
FROM menuItemIngredients 
INNER JOIN menuItems ON menuItemIngredients.menuItemID = menuItems.menuItemID 
INNER JOIN ingredients ON menuItemIngredients.ingredientID = ingredients.ingredientID

-- INSERT statement
INSERT INTO menuItemIngredients (menuItemID, ingredientID) 
VALUES (%s, %s)

-- DELETE statement
DELETE FROM menuItemIngredients 
WHERE menuItemID = %s 
AND ingredientID = %s


----- Cuisines -----

-- SELECT statement
SELECT cuisineID, cuisineName 
FROM cuisines

-- INSERT statement
INSERT INTO cuisines (cuisineName) 
VALUES (%s)

-- UPDATE statement
UPDATE cuisines 
SET cuisineName = %s 
WHERE cuisineID = %s

-- DELETE statement
DELETE FROM cuisines 
WHERE cuisineID = %s


----- Restaurant Schedule -----

-- SELECT statement
SELECT dayofWeek, 
restaurantSchedule.cuisineID, 
cuisines.cuisineName 
FROM restaurantSchedule 
LEFT JOIN cuisines ON cuisines.cuisineID = restaurantSchedule.cuisineID 
ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

-- INSERT statement
INSERT INTO restaurantSchedule (dayofWeek, cuisineID) 
VALUES (%s,%s)

-- UPDATE statement
UPDATE restaurantSchedule 
SET cuisineID = %s  
WHERE dayofWeek = %s

-- DELETE statement
DELETE FROM chefSchedule 
WHERE dayofWeek = %s


----- Chefs -----

-- SELECT statement
SELECT chefID, firstName, lastName, 
chefs.cuisineID, cuisines.cuisineName 
FROM chefs 
LEFT JOIN cuisines ON cuisines.cuisineID = chefs.cuisineID

-- INSERT statement
INSERT INTO chefs (firstName, lastName, cuisineID) 
VALUES (%s,%s,%s)

-- UPDATE statement
UPDATE chefs 
SET firstName = %s, lastName = %s, cuisineID = %s 
WHERE chefID = %s

-- DELETE statement
DELETE FROM chefs 
WHERE chefID = %s


----- Chefs Schedule -----

-- SELECT statement
SELECT dayofWeek, chefSchedule.chefID, chefs.firstName, chefs.lastName 
FROM chefSchedule 
LEFT JOIN chefs ON chefs.chefID = chefSchedule.chefID 
ORDER BY FIELD(dayofWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

-- INSERT statement
INSERT INTO chefSchedule (dayofWeek, chefID) 
VALUES (%s,%s)

-- DELETE statement
DELETE FROM chefSchedule 
WHERE dayofWeek = %s 
AND chefID = %s