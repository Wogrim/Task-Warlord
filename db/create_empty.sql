-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema task_warlord_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `task_warlord_schema` ;

-- -----------------------------------------------------
-- Schema task_warlord_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `task_warlord_schema` DEFAULT CHARACTER SET utf8 ;
USE `task_warlord_schema` ;

-- -----------------------------------------------------
-- Table `task_warlord_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(100) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `task_warlord_schema`.`projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`projects` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `owner_user_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_projects_users1_idx` (`owner_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_projects_users1`
    FOREIGN KEY (`owner_user_id`)
    REFERENCES `task_warlord_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `task_warlord_schema`.`versions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`versions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NULL,
  `project_id` INT NOT NULL,
  `end_date` DATE NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_versions_projects_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `fk_versions_projects`
    FOREIGN KEY (`project_id`)
    REFERENCES `task_warlord_schema`.`projects` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `task_warlord_schema`.`users_participate_projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`users_participate_projects` (
  `project_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`project_id`, `user_id`),
  INDEX `fk_projects_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_projects_has_users_projects1_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `fk_projects_has_users_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `task_warlord_schema`.`projects` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_projects_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `task_warlord_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `task_warlord_schema`.`task_groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`task_groups` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `version_id` INT NOT NULL,
  `start_date` DATE NULL,
  `end_date` DATE NULL,
  `progress` TINYINT NULL,
  `color` CHAR(7) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_task_groups_versions1_idx` (`version_id` ASC) VISIBLE,
  CONSTRAINT `fk_task_groups_versions1`
    FOREIGN KEY (`version_id`)
    REFERENCES `task_warlord_schema`.`versions` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `task_warlord_schema`.`tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `task_group_id` INT NOT NULL,
  `priority` TINYINT NULL,
  `assigned_user_id` INT NOT NULL,
  `status` TINYINT NULL,
  `progress` TINYINT NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tasks_task_groups1_idx` (`task_group_id` ASC) VISIBLE,
  INDEX `fk_tasks_users1_idx` (`assigned_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_tasks_task_groups1`
    FOREIGN KEY (`task_group_id`)
    REFERENCES `task_warlord_schema`.`task_groups` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tasks_users1`
    FOREIGN KEY (`assigned_user_id`)
    REFERENCES `task_warlord_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `task_warlord_schema`.`projects_invite_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_warlord_schema`.`projects_invite_users` (
  `project_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`project_id`, `user_id`),
  INDEX `fk_projects_has_users_users2_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_projects_has_users_projects2_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `fk_projects_has_users_projects2`
    FOREIGN KEY (`project_id`)
    REFERENCES `task_warlord_schema`.`projects` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_projects_has_users_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `task_warlord_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
