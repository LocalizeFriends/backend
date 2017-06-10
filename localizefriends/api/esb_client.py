import requests

ESB_ADDR = 'http://localizefriendsesb.ct8.pl/'

def send_fcm_message(fcm_ids, message):
    res = requests.post(ESB_ADDR + 'fcm_message', json={
        'fcm_ids': fcm_ids,
        'message': message
    })
