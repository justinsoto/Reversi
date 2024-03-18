CREATE TABLE Users (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(20) UNIQUE NOT NULL,
    Password_Hash VARCHAR(20) NOT NULL
);
/**The auto increment is just for the time being and add FOREIGN KEY (User_ID) REFERENCES Users(User_ID)**/
CREATE TABLE Ratings (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Top_Score INT,
    Number_Wins INT DEFAULT 0,
    Number_Loses INT DEFAULT 0,
    Number_Ties INT DEFAULT 0,
    ELO_Rating INT DEFAULT 1000
);

CREATE TABLE Games (
    Game_ID INT PRIMARY KEY AUTO_INCREMENT,
    Player1_ID INT,
    Player2_ID INT,
    Winner_ID INT,
    Game_State VARCHAR(2000),
    FOREIGN KEY (Player1_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Player2_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Winner_ID) REFERENCES Users(User_ID)
);





