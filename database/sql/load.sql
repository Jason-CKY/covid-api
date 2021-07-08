COPY Reports(Province_State, Country_Region, Date, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Incident_Rate, Case_Fatality_Ratio)
FROM '/data/final.csv' 
DELIMITER ',' 
CSV HEADER;