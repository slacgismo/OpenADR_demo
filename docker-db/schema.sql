DROP DATABASE IF EXISTS `openADR`;
CREATE DATABASE `openADR`;
USE `openADR`;

DROP TABLE IF EXISTS `meter`;

CREATE TABLE `meter` (
  `meter_id` VARCHAR(100) NOT NULL primary key,
  `ven_id` INT NOT NULL,
  `measurement` VARCHAR(45) NOT NULL,
  `value` REAL NOT NULL,
  `time` DATETIME NOT NULL,
  `device_id` VARCHAR(45) NOT NULL,
);

