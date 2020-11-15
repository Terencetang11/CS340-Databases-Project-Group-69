----- Index Table -----
-- SELECT statement for restaurant schedule
SELECT dayofWeek,
cuisines.cuisineName
FROM restaurantSchedule
LEFT JOIN cuisines on cuisines.cuisineID = restaurantSchedule.cuisineID
WHERE dayofWeek = {{dayFilter}}
AND cuisineName = {{cuisineFilter}}

-- SELECT statement for chefs on schedule
SELECT restaurantSchedule.dayofWeek,
chefs.firstName,
chefs.lastName
FROM restaurantSchedule
LEFT JOIN chefSchedule ON chefSchedule.dayofWeek = restaurantSchedule.dayofWeek
LEFT JOIN chefs ON chefs.chefID = chefSchedule.chefID

-- need to write application layer code to display multiple chefs inline



----- Ingredients Table -----
	-- SELECT statement
SELECT * FROM ingredients
WHERE isVegan = {{veganFilter}}
AND inventory = {{outofStock}}


-- INSERT statement
INSERT INTO ingredients (ingredientName, isVegan, inventory)
VALUES ({{ingredientName}}, {{isVegan}}, {{inventoryAmt}})


-- UPDATE statement
UPDATE ingredients
SET ingredientName = {{ingredientNameUpdate}}
	, isVegan = {{isVeganUpdate}}
	, inventory = {{inventoryUpdate}}
WHERE ingredientID = {{ingredientID}}


-- DELETE statement
-- 2-step process: first delete relevant MenuItems
DELETE FROM menuItems 
WHERE menuItemID in (
	SELECT menuItemID
	FROM menuItemIngredients
	WHERE ingredientID = {{ingredientID}}
	)

-- 2-step process: then delete Ingredients
DELETE FROM ingredients WHERE ingredientID = {{ingredientID}}


----- Menu Items Table -----
-- SELECT statement
SELECT menuItemID
, menuItemName
, menuItems.cuisineID
, cuisines.cuisineName
, price
FROM menuItems
LEFT JOIN cuisines ON cuisines.cuisineID = menuItems.cuisineID
WHERE cuisines.cuisineID = (SELECT cuisines.cuisineID FROM cuisines WHERE cuisineName = {{cuisineFilter}})


-- INSERT statement
-- 2-step process: insert menu items into menuItems table
INSERT INTO menuItems (menuItemName, cuisineID, price)
VALUES (
	{{menuItemName}} 
	, (SELECT cuisines.cuisineID FROM cuisines WHERE cuisines.cuisineName = {{cuisineName}})
	, {{price}}
	)

-- 2-step process: insert into menuItemIngredients table based on ingredients used
INSERT INTO menuItemIngredients (menuItemID, ingredientID)
VALUES (
	(SELECT menuItems.menuItemID FROM menuItems WHERE menuItems.menuItemName = {{menuItemName}})
	, (SELECT ingredients.ingredientID FROM ingredients WHERE ingredients.ingredientName = {{ingredientName}})
	)


-- UPDATE statement
UPDATE menuItems
SET menuItemName = {{menuItemNameUpdate}}
	, cuisineID = (SELECT cuisines.cuisineid FROM cuisines WHERE cuisines.cuisineName = {{cuisineNameUpdate}})
	, price = {{priceUpdate}}
WHERE menuItemID = {{menuItemID}}


-- DELETE statement
DELETE FROM menuItems WHERE menuItemID = {{menuItemID}}


----- Cuisines Table -----
-- SELECT statement
SELECT * FROM cuisines

-- INSERT statement
INSERT INTO cuisines (cuisineName)
VALUES ({{cuisineName}})

-- UPDATE statement
UPDATE cuisines 
SET cuisineName = {{cuisineNameUpdate}}
WHERE cuisineID = {{cuisineID}}

-- DELETE statement
DELETE FROM cuisines WHERE cuisineID = {{cuisineID}}

