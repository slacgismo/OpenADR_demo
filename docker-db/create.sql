-- DROP DATABASE IF EXISTS `openADR`;
-- CREATE DATABASE `openADR`;
-- USE `openADR`;


DROP DATABASE IF EXISTS `openADR`;
CREATE DATABASE `openADR`;
USE `openADR`;

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
  `OrderTime` datetime,
  `Item` varchar(100) NOT NULL
);