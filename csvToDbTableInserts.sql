-- Olympic Swimming History Table
CREATE TABLE olympicSwimmingResults_1912_2020 (
    id INT PRIMARY KEY,
    Location VARCHAR(50) NOT NULL,
    YearInt INT NOT NULL,
    Distance VARCHAR(50) NOT NULL,
    Stroke VARCHAR(50) NOT NULL,
    Relay INT NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Team CHAR(3) NOT NULL,
    Athlete VARCHAR(100) NOT NULL,
    Results VARCHAR(50) NOT NULL,
    Rank INT NOT NULL
);

-- Example insertions of values from csv file
INSERT INTO olympicSwimmingResults_1912_2020 VALUES(1, "Tokyo", 2020, "100m", "Backstroke", 0, "Men", "ROC", "Evgeny Rylov", "51.98", 1);
INSERT INTO olympicSwimmingResults_1912_2020 VALUES(2, "Tokyo", 2020, "100m", "Backstroke", 0, "Men", "ROC", "Kliment Kolesnikov", "52", 2);
INSERT INTO olympicSwimmingResults_1912_2020 VALUES(3, "Tokyo", 2020, "100m", "Backstroke", 0, "Men", "USA", "Ryan Murphy", "52.19", 3);
INSERT INTO olympicSwimmingResults_1912_2020 VALUES(4, "Tokyo", 2020, "100m", "Backstroke", 0, "Men", "ITA", "Thomas Ceccon", "52.3", 4);
INSERT INTO olympicSwimmingResults_1912_2020 VALUES(5, "Tokyo", 2020, "100m", "Backstroke", 0, "Men", "CHN", "Jiayu Xu", "52.51", 4);

-- -- Get the column types and corresponding data types
-- SELECT COLUMN_NAME, DATA_TYPE
--     FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_NAME = "olympicSwimmingResults_1912_2020";
