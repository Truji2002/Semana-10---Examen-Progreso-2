from flask import Flask, request, Response
from database import app, db
from flask_sqlalchemy import SQLAlchemy

class Availability(db.Model):
    __tablename__ = 'availability'
    room_id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(50))
    available_date = db.Column(db.Date)
    status = db.Column(db.String(20))

@app.route('/checkAvailability', methods=['POST'])
def soap_service():
    try:
        request_data = request.data.decode('utf-8')

        start_date = extract_tag(request_data, 'start_date')
        end_date = extract_tag(request_data, 'end_date')
        room_type = extract_tag(request_data, 'room_type')

        results = Availability.query.filter(
            Availability.room_type == room_type,
            Availability.available_date >= start_date,
            Availability.available_date <= end_date
        ).all()

        rooms_xml = ''.join(
            f"<Room><RoomID>{room.room_id}</RoomID><Status>{room.status}</Status></Room>"
            for room in results
        )
        response_xml = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <checkAvailabilityResponse>
                    {rooms_xml if rooms_xml else '<Message>No rooms available</Message>'}
                </checkAvailabilityResponse>
            </soap:Body>
        </soap:Envelope>
        """

        return Response(response_xml, content_type='text/xml')
    except Exception as e:
        print("Error:", e)
        return Response("<soap:Fault>Error processing request</soap:Fault>", content_type='text/xml')

def extract_tag(xml, tag):
    start = xml.find(f"<{tag}>") + len(f"<{tag}>")
    end = xml.find(f"</{tag}>")
    return xml[start:end]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
