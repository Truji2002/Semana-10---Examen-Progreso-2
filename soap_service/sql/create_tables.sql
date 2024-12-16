CREATE TABLE availability (
    room_id SERIAL PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    available_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL
);

INSERT INTO availability (room_type, available_date, status)
VALUES
('Single', '2024-12-20', 'Available'),
('Double', '2024-12-21', 'Available'),
('Suite', '2024-12-22', 'Maintenance');