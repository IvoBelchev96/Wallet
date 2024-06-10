# SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
# SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
# SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

# -- -----------------------------------------------------
# -- Schema mydb
# -- -----------------------------------------------------
# -- -----------------------------------------------------
# -- Schema virtual_wallet_schema
# -- -----------------------------------------------------

# -- -----------------------------------------------------
# -- Schema virtual_wallet_schema
# -- -----------------------------------------------------
# CREATE SCHEMA IF NOT EXISTS `virtual_wallet_schema` ;
# USE `virtual_wallet_schema` ;

# -- -----------------------------------------------------
# -- Table `virtual_wallet_schema`.`users`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `virtual_wallet_schema`.`users` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `username` VARCHAR(30) NOT NULL,
#   `password` TEXT NOT NULL,
#   `email` VARCHAR(120) NOT NULL,
#   `phone_number` VARCHAR(10) NOT NULL,
#   `is_admin` TINYINT(4) NOT NULL DEFAULT 0,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
#   UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
#   UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
#   UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC) VISIBLE)
# ENGINE = InnoDB;


# -- -----------------------------------------------------
# -- Table `virtual_wallet_schema`.`cards`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `virtual_wallet_schema`.`cards` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `type` ENUM('credit', 'debit') NOT NULL,
#   `user_id` INT(11) NOT NULL,
#   `expiration_date` DATE NOT NULL,
#   `cvv` INT(11) NOT NULL,
#   `number` VARCHAR(16) NOT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
#   UNIQUE INDEX `number_UNIQUE` (`number` ASC) VISIBLE,
#   INDEX `fk_cards_users_idx` (`user_id` ASC) VISIBLE,
#   CONSTRAINT `fk_cards_users`
#     FOREIGN KEY (`user_id`)
#     REFERENCES `virtual_wallet_schema`.`users` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB;


# -- -----------------------------------------------------
# -- Table `virtual_wallet_schema`.`contacts`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `virtual_wallet_schema`.`contacts` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `contact_name_id` INT(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
#   INDEX `fk_contacts_users1_idx` (`contact_name_id` ASC) VISIBLE,
#   CONSTRAINT `fk_contacts_users1`
#     FOREIGN KEY (`contact_name_id`)
#     REFERENCES `virtual_wallet_schema`.`users` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB;


# -- -----------------------------------------------------
# -- Table `virtual_wallet_schema`.`transactions`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `virtual_wallet_schema`.`transactions` (
#   `id` INT(11) NOT NULL AUTO_INCREMENT,
#   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
#   `amount` FLOAT NOT NULL,
#   `sender_id` INT(11) NOT NULL,
#   `receiver_id` INT(11) NOT NULL,
#   `status` ENUM('pending', 'successful', 'failed', 'sender_confirmed', 'receiver_confirmed') NOT NULL DEFAULT 'pending',
#   `category` VARCHAR(45) NOT NULL DEFAULT 'other',
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
#   INDEX `fk_transactions_users1_idx` (`sender_id` ASC) VISIBLE,
#   INDEX `fk_transactions_users2_idx` (`receiver_id` ASC) VISIBLE,
#   CONSTRAINT `fk_transactions_users1`
#     FOREIGN KEY (`sender_id`)
#     REFERENCES `virtual_wallet_schema`.`users` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_transactions_users2`
#     FOREIGN KEY (`receiver_id`)
#     REFERENCES `virtual_wallet_schema`.`users` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB;