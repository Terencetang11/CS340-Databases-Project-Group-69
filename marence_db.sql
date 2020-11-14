CREATE TABLE `ingredients` (
	`ingredientID` INT(11) AUTO_INCREMENT PRIMARY KEY,
	`ingredientName` VARCHAR(255) NOT NULL,
	`isVegan` BOOLEAN NOT NULL,
	`inventory` INT(11)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `cuisines` (
	`cuisineID` INT(11) AUTO_INCREMENT PRIMARY KEY,
	`cuisineName` VARCHAR(255) NOT NULL
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `menuItems` (
	`menuItemID` INT(11) AUTO_INCREMENT PRIMARY KEY,
	`menuItemName` VARCHAR(255) NOT NULL,
	`cuisineID` INT(11) NOT NULL,
	`price` DECIMAL(10,2) NOT NULL,
	CONSTRAINT `cuisineID_ibfk_1` FOREIGN KEY (`cuisineID`) REFERENCES `cuisines` (`cuisineID`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `menuItemIngredients` (
	`menuItemID` INT(11) NOT NULL DEFAULT '0',
	`ingredientID` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`menuItemID`, `ingredientID`),
	CONSTRAINT `menuItemIngredients_ibfk_1` FOREIGN KEY (`menuItemID`) REFERENCES `menuItems` (`menuItemID`),
	CONSTRAINT `menuItemIngredients_ibfk_2` FOREIGN KEY (`ingredientID`) REFERENCES `ingredients` (`ingredientID`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chefs` (
	`chefID` INT(11) AUTO_INCREMENT PRIMARY KEY,
	`firstName` VARCHAR(255) NOT NULL,
	`lastName` VARCHAR(255) NOT NULL,
	`cuisineID` INT(11) NOT NULL DEFAULT '0',
	CONSTRAINT `chefs_ibfk_1` FOREIGN KEY (`cuisineID`) REFERENCES `cuisines` (`cuisineID`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `restaurantSchedule` (
	`dayofWeek` VARCHAR(255) NOT NULL PRIMARY KEY,
	`cuisineID` INT(11) NOT NULL DEFAULT '0',
	CONSTRAINT `restaurantSchedule_ibfk_1` FOREIGN KEY (`cuisineID`) REFERENCES `cuisines` (`cuisineID`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chefSchedule` (
	`dayofWeek` VARCHAR(255) NOT NULL DEFAULT '0',
	`chefID` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`dayofWeek`, `chefID`),
	CONSTRAINT `chefSchedule_ibfk_1` FOREIGN KEY (`dayofWeek`) REFERENCES `restaurantSchedule` (`dayofWeek`),
	CONSTRAINT `chefSchedule_ibfk_2` FOREIGN KEY (`chefID`) REFERENCES `chefs` (`chefID`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `ingredients` (ingredientName, isVegan, inventory) VALUES ('Carrots', TRUE, '100');
INSERT INTO `ingredients` (ingredientName, isVegan, inventory) VALUES ('Chicken Thighs', FALSE, '73');
INSERT INTO `ingredients` (ingredientName, isVegan, inventory) VALUES ('Eggs', FALSE, '89');
INSERT INTO `cuisines` (cuisineName) VALUES ('Italian');
INSERT INTO `cuisines` (cuisineName) VALUES ('South Asian');
INSERT INTO `cuisines` (cuisineName) VALUES (`Southern`);
INSERT INTO 'menuItems' (menuItemName, cuisineID, price) VALUES ('Ribeye Steak', '3', '14.99');
INSERT INTO 'menuItems' (menuItemName, cuisineID, price) VALUES ('Chicken Makhani', '2', '11.99');
INSERT INTO 'menuItems' (menuItemName, cuisineID, price) VALUES ('Chicken Cacciatore', '1', '17.99');
INSERT INTO 'chefs' (firstName, lastName, cuisineID) VALUES ('John', 'Doe', '2');
INSERT INTO 'chefs' (firstName, lastName, cuisineID) VALUES ('Jane', 'Doe', '3');
INSERT INTO 'chefs' (firstName, lastName, cuisineID) VALUES ('Mary', 'Smith', '1');
INSERT INTO 'chefs' (firstName, lastName, cuisineID) VALUES ('John', 'Doe', '2');