from flask import request, jsonify
from database import app, db, Reservation
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

@app.route('/reservations', methods=['POST'])
def create_reservation():
    try:       
        data = request.json
        room_type = data['room_type']
        start_date = data['start_date']
        end_date = data['end_date']
        customer_name = data['customer_name']

        soap_request = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
           <soapenv:Header/>
           <soapenv:Body>
              <checkAvailability>
                 <start_date>{start_date}</start_date>
                 <end_date>{end_date}</end_date>
                 <room_type>{room_type}</room_type>
              </checkAvailability>
           </soapenv:Body>
        </soapenv:Envelope>
        """
        soap_response = requests.post("http://localhost:8000/checkAvailability", data=soap_request, headers={"Content-Type": "text/xml"})

        print("SOAP Response Status Code:", soap_response.status_code)
        print("SOAP Response Text:", soap_response.text)

        if soap_response.status_code != 200 or not soap_response.text:
            return jsonify({"error": "SOAP service returned an invalid response"}), 500

        try:
            namespaces = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}
            root = ET.fromstring(soap_response.text)
            
            rooms = [
                room.find('RoomID').text 
                for room in root.findall(".//Room") 
                if room.find('RoomID') is not None
            ]
        except Exception as parse_error:
            print("Error parsing SOAP response:", parse_error)
            return jsonify({"error": "Failed to parse SOAP response"}), 500

        if not rooms:
            return jsonify({"error": "No rooms available"}), 400

        available_room = None
        for room_id in rooms:
            existing_reservation = Reservation.query.filter_by(
                room_number=room_id
            ).filter(
                Reservation.start_date <= end_date,
                Reservation.end_date >= start_date
            ).first()

            if not existing_reservation:
                available_room = int(room_id)
                break

        if not available_room:
            return jsonify({"error": "All rooms are reserved for the given dates"}), 400

        # Crear la reserva
        new_reservation = Reservation(
            room_number=available_room,
            customer_name=customer_name,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
            status="Confirmed"
        )
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({
            "message": "Reservation created successfully",
            "reservation_id": new_reservation.reservation_id,
            "room_number": available_room
        }), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/reservations/<int:id>', methods=['GET'])
def get_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    return jsonify({
        "reservation_id": reservation.reservation_id,
        "room_number": reservation.room_number,
        "customer_name": reservation.customer_name,
        "start_date": reservation.start_date.strftime("%Y-%m-%d"),
        "end_date": reservation.end_date.strftime("%Y-%m-%d"),
        "status": reservation.status
    }), 200


@app.route('/reservations/<int:id>', methods=['DELETE'])
def cancel_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation cancelled successfully"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
