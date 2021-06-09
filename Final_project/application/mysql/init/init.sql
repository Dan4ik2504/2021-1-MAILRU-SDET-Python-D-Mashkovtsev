CREATE USER 'test_qa' IDENTIFIED BY 'qa_test';
GRANT ALL PRIVILEGES ON * . * TO 'test_qa';
FLUSH PRIVILEGES;

USE `myapp_db`;
CREATE TABLE `test_users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(16) DEFAULT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(64) NOT NULL,
    `access` smallint DEFAULT NULL,
    `active` smallint DEFAULT NULL,
    `start_active_time` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `ix_test_users_username` (`username`)
);

CREATE DATABASE `vk_api_db`;
USE `vk_api_db`;
CREATE TABLE `vk_id_table` (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `username` varchar(16) DEFAULT NULL,
    `vk_id` text DEFAULT NULL
);
