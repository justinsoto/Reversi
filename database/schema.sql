CREATE TABLE Users (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(20) UNIQUE NOT NULL,
    Password_Hash VARCHAR(20) NOT NULL,
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

CREATE TABLE Leaderboard (
    Leaderboard_ID INT PRIMARY KEY AUTO_INCREMENT,
    User_ID INT,
    Top_Score INT,
    Game_ID INT UNIQUE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Game_ID) REFERENCES Games(Game_ID)
);



