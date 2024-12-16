CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_number INT NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL
);

INSERT INTO rooms (room_number, room_type, status)
VALUES
(101, 'Single', 'Available'),
(102, 'Double', 'Maintenance'),
(201, 'Suite', 'Available');
