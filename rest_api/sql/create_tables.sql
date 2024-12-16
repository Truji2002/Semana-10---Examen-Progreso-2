CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    room_number INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL
);

INSERT INTO reservations (room_number, customer_name, start_date, end_date, status)
VALUES
(1, 'John Doe', '2024-12-20', '2024-12-22', 'Confirmed');
