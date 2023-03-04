CREATE OR REPLACE DATABASE local_db;

USE local_db;

CREATE TABLE geoloaded (
    longitude varchar(50) NOT NULL,
    latitude varchar(50) NOT NULL,
    load_date datetime
);

CREATE TABLE geoprocessed (
    longitude varchar(50) NOT NULL,
    latitude varchar(50) NOT NULL,
    postalcode varchar(50) NOT NULL,
    load_date datetime
);