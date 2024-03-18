CREATE TABLE Users (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(20) UNIQUE NOT NULL,
    Password_Hash VARCHAR(20) NOT NULL
);
/**The auto increment is just for the time being and add FOREIGN KEY (User_ID) REFERENCES Users(User_ID)**/
CREATE TABLE Ratings (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Top_Score INT,
    Number_Wins INT,
    Number_Loses INT
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

/**The auto increment primary key is just for the time being and add FOREIGN KEY (User_ID) REFERENCES Users(User_ID)**/
CREATE TABLE Leaderboard (
    Leaderboard_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT,
    Top_Score INT,
    Number_Wins INT,
    Number_Loses INT,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Top_Score) REFERENCES Ratings(Top_Score),
    FOREIGN KEY (Number_Wins) REFERENCES Ratings(Number_Wins),
    FOREIGN KEY (Number_Loses) REFERENCES Ratings(Number_Loses)
);



