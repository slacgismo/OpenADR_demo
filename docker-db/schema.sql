

DROP DATABASE IF EXISTS `openADR`;
CREATE DATABASE `openADR`;
USE `openADR`;

DROP TABLE IF EXISTS `measurements`;
CREATE TABLE `measurements` (
  `data_id` INT primary key,
  `meter_id` INT NOT NULL,
  `ven_id` INT NOT NULL,
  `measurement` VARCHAR(100) NOT NULL,
  `value` REAL NOT NULL,
  `time` DATETIME NOT NULL,
  `device_id` INT NOT NULL
);

