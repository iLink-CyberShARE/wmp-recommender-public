-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema swim-recommender
--
-- Database model for SWIM recommender system.
-- 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `swim-recommender`;
USE `swim-recommender` ;

-- -----------------------------------------------------
-- Table `category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL COMMENT 'Name of the category group.',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `model`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `model` (
  `id` VARCHAR(60) NOT NULL,
  `name` VARCHAR(300) NOT NULL COMMENT 'label for the model',
  `context_iri` VARCHAR(300) NULL COMMENT 'json-ld uri to provide semantics on json outputs',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `model_id` VARCHAR(60) NOT NULL,
  `category_id` INT NOT NULL,
  `guid` VARCHAR(60) NOT NULL COMMENT 'global unique identifer',
  `name` VARCHAR(100) NOT NULL COMMENT 'name of the item',
  INDEX `fk_output_category1_idx` (`category_id` ASC),
  INDEX `fk_output_model1_idx` (`model_id` ASC),
  UNIQUE INDEX `guid_UNIQUE` (`guid` ASC),
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_output_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_output_model1`
    FOREIGN KEY (`model_id`)
    REFERENCES `model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL COMMENT 'label of the user group',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `explicit_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `explicit_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  `rank_value` INT(1) NOT NULL COMMENT 'value from 1 to 5 that was explicitly assigned by a user.',
  `user_id` INT NULL COMMENT 'direct user identifier.',
  `timestamp` TIMESTAMP NOT NULL COMMENT 'timestamp of when the item was ranked',
  `run_id` VARCHAR(60) NULL COMMENT 'unique identifier for the scientific model run (SWIM framework dependent)',
  PRIMARY KEY (`id`),
  INDEX `fk_explicit_log_item1_idx` (`item_id` ASC),
  INDEX `fk_explicit_log_role1_idx` (`role_id` ASC),
  CONSTRAINT `fk_explicit_log_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_explicit_log_role1`
    FOREIGN KEY (`role_id`)
    REFERENCES `role` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `implicit_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `implicit_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT NOT NULL COMMENT 'foreign key of item',
  `role_id` INT NOT NULL COMMENT 'foreign key of role',
  `user_id` INT NULL COMMENT 'direct user identifier',
  `timestamp` TIMESTAMP NOT NULL COMMENT 'timestamp of when the interaction was logged',
  `run_id` VARCHAR(60) NULL COMMENT 'identifier of the scientific model execution (SWIM dependent)',
  PRIMARY KEY (`id`),
  INDEX `fk_nav_log_role1_idx` (`role_id` ASC),
  INDEX `fk_implicit_log_item1_idx` (`item_id` ASC),
  CONSTRAINT `fk_nav_log_role1`
    FOREIGN KEY (`role_id`)
    REFERENCES `role` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_implicit_log_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `training`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `training` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `model_id` VARCHAR(60) NOT NULL,
  `status` VARCHAR(45) NOT NULL COMMENT 'can be: success, fail, not trained',
  `message` VARCHAR(200) NULL COMMENT 'details about the training status',
  `last_trained` DATETIME NULL COMMENT 'last time the model was trained',
  `num_users` INT NOT NULL DEFAULT 0 COMMENT 'number of users on the sparce input matrix',
  `num_items` INT NOT NULL DEFAULT 0 COMMENT 'number of items on the sparce input matrix',
  `model_file` VARCHAR(200) NULL COMMENT 'name of the generated model file',
  `implicit` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'flag if implicit data was used for training i.e. implicit_log table data',
  `explicit` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'flag if explicit data was used for training i.e. explicit_log table data',
  `content` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'flag if content based traing is used i.e. use of keyword tables for items and roles',
  `test_percent` FLOAT NULL COMMENT 'Percent of disjoint test data from overall interactions ',
  `learning_rate` VARCHAR(60) NULL COMMENT 'Learning rate value ',
  `epochs` INT(11) NULL COMMENT 'Data iterations ',
  `loss` VARCHAR(60) NULL COMMENT 'Name of loss function used ',
  `user_alpha` FLOAT NULL COMMENT 'L2 penalty on user features ',
  `item_alpha` FLOAT NULL COMMENT 'L2 penalty on item features ',
  PRIMARY KEY (`id`),
  INDEX `fk_training_status_model1_idx` (`model_id` ASC),
  CONSTRAINT `fk_training_status_model1`
    FOREIGN KEY (`model_id`)
    REFERENCES `model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hush`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hush` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `value` VARCHAR(200) NOT NULL COMMENT 'secret key used for encryption of json web token',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `item_keyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `item_keyword` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `keyword` VARCHAR(100) NOT NULL COMMENT 'keyword related to item',
  `item_id` INT NOT NULL COMMENT 'item foreign key',
  `weight` INT NULL COMMENT 'optional weight value as integer',
  PRIMARY KEY (`id`),
  INDEX `fk_item_keyword_item1_idx` (`item_id` ASC),
  CONSTRAINT `fk_item_keyword_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `role_keyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `role_keyword` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `role_id` INT NOT NULL COMMENT 'role foreign key',
  `keyword` VARCHAR(100) NOT NULL COMMENT 'keyword related to role',
  `weight` INT NULL COMMENT 'optional weight value as integer',
  PRIMARY KEY (`id`),
  INDEX `fk_role_keyword_role1_idx` (`role_id` ASC),
  CONSTRAINT `fk_role_keyword_role1`
    FOREIGN KEY (`role_id`)
    REFERENCES `role` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

