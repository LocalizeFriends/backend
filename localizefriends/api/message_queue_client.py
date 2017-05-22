import zmq

def send_fcm_message(fcm_ids, message):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:5555")
    socket.send_json({
        'operation': 'send_fcm_message',
        'arguments': {
            'fcm_ids': fcm_ids,
            'message': message
        }
    })
    socket.close(100) # wait at most 100 ms to send message
