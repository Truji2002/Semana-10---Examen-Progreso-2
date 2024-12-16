from flask import request, jsonify
from database import app, db, Room

@app.route('/rooms', methods=['POST'])
def create_room():
    try:
        data = request.json
        room_number = data['room_number']
        room_type = data['room_type']
        status = data['status']

        if Room.query.filter_by(room_number=room_number).first():
            return jsonify({"error": "Room already exists"}), 400

        # Crear una nueva habitación
        new_room = Room(
            room_number=room_number,
            room_type=room_type,
            status=status
        )
        db.session.add(new_room)
        db.session.commit()

        return jsonify({"message": "Room created successfully", "room": new_room.to_dict()}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500
    



@app.route('/rooms/<int:room_id>', methods=['PATCH'])
def update_room_status(room_id):
    try:
        data = request.json
        new_status = data.get('status')

        # Verificar si la habitación existe
        room = Room.query.get(room_id)
        if not room:
            return jsonify({"error": "Room not found"}), 404

        # Actualizar el estado
        room.status = new_status
        db.session.commit()

        return jsonify({"message": "Room status updated successfully", "room": room.to_dict()}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


# Ejecutar el servidor
if __name__ == '__main__':
    app.run(port=5001, debug=True)
