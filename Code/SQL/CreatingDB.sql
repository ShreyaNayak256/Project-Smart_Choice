CREATE DATABASE SmartChoice;
Show Databases;
Use SmartChoice;
Create TABLE IF NOT EXISTS ‘Smart_choice’ (‘ID’ varchar(15) NOT NULL, ‘Title’ varchar(100) NOT NULL, ‘Type’ varchar(10) NOT NULL, ‘Description’ varchar(100) NOT NULL, ‘Release_year’ int NOT NULL, ‘Genres’ varchar(300) NOT NULL, ‘Imdb_Score’ float(3) NOT NULL, ‘Streaming_Platform’ varchar(100) NOT NULL);
Show Tables;
Create Table Namenode(
        Node_Id int auto_increment,
        Parent_Id int,
        Name varchar (500) UNIQUE not null, 
        Part varchar (100),
        PRIMARY KEY (Node_Id));
Create Table Part_Directory(
        D_Id INT AUTO_INCREMENT, 
        Parent_Id INT, 
        D_Name VARCHAR(255) UNIQUE, 
        PRIMARY KEY (D_Id));
