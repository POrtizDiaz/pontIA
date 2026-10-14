CREATE TABLE bookings.flight_incidents (
    incident_id serial PRIMARY KEY,
    flight_id integer NOT NULL REFERENCES bookings.flights (flight_id) ON DELETE CASCADE,
    incident_type varchar(50) NOT NULL,
    severity varchar(20) NOT NULL,
    CONSTRAINT chk_incident_severity CHECK (
      severity IN ('Low', 'Medium', 'High', 'Critical')
    )
);
INSERT INTO bookings.flight_incidents (flight_id, incident_type, severity)
VALUES (1234, 'Engine Check', 'High');


CREATE TABLE if not exists bookings.aircraft_maintance(
    maintance_id SERIAL PRIMARY KEY,
    aircraft_code bpchar(3) NOT NULL REFERENCES bookings.airplanes_data (airplane_code)
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
    maintance_type VARCHAR(50) NOT NULL,
    status varchar(20) NOT NULL,
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    cost NUMERIC(10,2) NOT NULL,
    CONSTRAINT chk_status CHECK (
      status IN ('Scheduled', 'In_Progress', 'Completed', 'Cancelled')
    ),
    CONSTRAINT chk_cost CHECK (
      (cost >= 0)
    )
)

INSERT INTO bookings.aircraft_maintance (aircraft_code, maintance_type, status, cost)
VALUES ('773', 'Turbine Overhaul', 'In_progress', 150000),
       ('319', 'Avionics Check', 'Scheduled', 4500)

UPDATE TABLE bookings.aircraft_maintance
SET cost 
WHERE status = 'In_Progress';




