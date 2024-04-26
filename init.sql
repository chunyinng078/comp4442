DROP DATABASE IF EXISTS project_db;
CREATE DATABASE project_db;

USE project_db;

CREATE TABLE Driving_Record_A (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id VARCHAR(255) NOT NULL ,
    CarPlateNumber VARCHAR(255) NOT NULL,
    Date VARCHAR(255) NOT NULL,
    Hour INT NOT NULL,
    TotalNeturalSlideTime DOUBLE NOT NULL,
    CountOfOverSpeed INT NOT NULL,
    TotalOfOverSpeedTime DOUBLE NOT NULL,
    CountOfFatigueDriving INT NOT NULL
);

CREATE TABLE Driving_Record_B (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id VARCHAR(255) NOT NULL ,
    CarPlateNumber VARCHAR(255) NOT NULL,
    ctime bigint(20) NOT NULL ,
    Speed DOUBLE NOT NULL,
    Overspeed BOOLEAN NOT NULL
);