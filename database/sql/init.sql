CREATE TABLE Reports(
  ReportID BIGSERIAL not null,
  Province_State varchar(255),
  Country_Region varchar(255) not null,
  Date date not null,
  Last_Update TIMESTAMP,
  Lat double precision,
  Long_ double precision,
  Confirmed int,
  Deaths int,
  Recovered int,
  Active int,
  Incident_Rate double precision,
  Case_Fatality_Ratio double precision,
  primary key(ReportID)
);

CREATE INDEX idx_country ON Reports(Country_Region);
CREATE INDEX idx_date ON Reports(Date);
CREATE INDEX idx_state ON Reports(Province_State);
