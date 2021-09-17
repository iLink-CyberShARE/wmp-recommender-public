-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema user_db
-- -----------------------------------------------------
-- Sample user database to use for recommender system token generation and authorization levels. This is just a sample, better to connect to your own database or user handling endpoints.

-- -----------------------------------------------------
-- Schema user_db
--
-- Sample user database to use for recommender system token generation and authorization levels. This is just a sample, better to connect to your own database or user handling endpoints.
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `user_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `user_db` ;

-- -----------------------------------------------------
-- Table `user_db`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user_db`.`USER` (
  `uid` INT NOT NULL AUTO_INCREMENT,
  `uemail` VARCHAR(200) NOT NULL COMMENT 'unique email address',
  `upassword` VARCHAR(300) NOT NULL COMMENT 'encrypted password, recommender system uses sha1 hash, better hash function recommended for production environments',
  `is_guest` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'flag to check if the user is guest, this flag is not currently used for recommender endpoint access.',
  `is_contentmanager` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'flasg to check if the user is a content manager, used for endpoint authorization on model training and crud operations',
  PRIMARY KEY (`uid`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Data for table `user_db`.`USER`
-- -----------------------------------------------------
START TRANSACTION;
USE `user_db`;
INSERT INTO `user_db`.`USER` (`uid`, `uemail`, `upassword`, `is_guest`, `is_contentmanager`) VALUES (1, 'manager@email.com', 'f5a2962fc5cfacd53d2ba4755bd02cf5bd46bd27', 0, 1);
INSERT INTO `user_db`.`USER` (`uid`, `uemail`, `upassword`, `is_guest`, `is_contentmanager`) VALUES (2, 'uiaccess@email.com', '4c935cf3aec50c0a7295052db3274bc9eb3da88f', 1, 0);

COMMIT;

