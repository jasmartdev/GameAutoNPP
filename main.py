import time
import json
import requests
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

mission_headers = {'sec-ch-ua-platform': '"Windows"', 'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF5ZXJJZCI6IjEyYmNmOTk0LWUwZmMtNGNkNi05MmI1LWE0YjAzYTE1YTJlNiIsImlhdCI6MTc4NDY0MzEzOCwiZXhwIjoxNzkyNDE5MTM4fQ.9G2rOtWmRXgLrHUEgs5eM6N3bdRH5wrbvWrgb1QqsMM', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36', 'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"', 'content-type': 'application/json', 'sec-ch-ua-mobile': '?0', 'accept': '*/*', 'origin': 'https://wall-wars.game-files.crazygames.com', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://wall-wars.game-files.crazygames.com/', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9', 'priority': 'u=1, i'}

mission_start_mission_url = 'https://defense-wall-production.up.railway.app/api/player/12bcf994-e0fc-4cd6-92b5-a4b03a15a2e6/start-mission'
mission_start_mission_body = b'{"missionId":150}'

mission_complete_mission_url = 'https://defense-wall-production.up.railway.app/api/player/12bcf994-e0fc-4cd6-92b5-a4b03a15a2e6/complete-mission'
mission_complete_mission_body = b'{"missionId":150,"victory":false,"monstersKilled":500,"antiCheat":{"version":1,"team":[1,11,4,5,12],"waves":[]}}'

def run_health_check_server():
    # Back4app uses HTTP, so bind to standard HTTP logic on the requested port
    server_address = ('0.0.0.0', 443)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Health check server running on port 443...")
    httpd.serve_forever()

if __name__ == '__main__':
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    current_missionId = 159
    current_monstersKilled = 193
    current_sleep_time = 80
    is_test_monsters = True
    is_complete_mission = False
    while True:
        start_mission_body = mission_start_mission_body
        json_data = json.loads(start_mission_body.decode('utf-8'))
        json_data['missionId'] = current_missionId
        start_mission_body = json.dumps(json_data).encode('utf-8')
        response = requests.post(
        url=mission_start_mission_url, 
        headers=mission_headers, 
        data=start_mission_body
        )
        data = response.json()
        data_error = data.get('error')
        if data_error and 'Cannot replay completed mission' in data_error:
            data_error = data_error[:-11]
            data_error = data_error[58:]
            current_missionId = int(data_error.strip())
            continue
        complete_mission_body = mission_complete_mission_body
        json_data = json.loads(complete_mission_body.decode('utf-8'))
        json_data['missionId'] = current_missionId
        if is_test_monsters:
            json_data['monstersKilled'] = 1000
        else:
            time.sleep(current_sleep_time)
            if is_complete_mission:
                json_data['victory'] = True
                json_data['monstersKilled'] = current_monstersKilled + 1
            else:
                json_data['monstersKilled'] = current_monstersKilled
        complete_mission_body = json.dumps(json_data).encode('utf-8')
        response = requests.post(
        url=mission_complete_mission_url, 
        headers=mission_headers, 
        data=complete_mission_body
        )
        data = response.json()
        data_error = data.get('error')
        if data_error:
            if data.get('code') == 'SERVER_ERROR':
                print('SERVER_ERROR')
                current_sleep_time = current_sleep_time + 20
            elif 'Invalid monstersKilled' in data_error:
                current_monstersKilled = int(data.get('error').split('-')[1]) - 1
                current_sleep_time = current_monstersKilled*0.5
                is_test_monsters =  False
        elif data.get('success'):
            if is_complete_mission:
                is_test_monsters = True
                is_complete_mission = False
                current_missionId = current_missionId + 1
            elif data.get('rewardsApplied') and data.get('rewardsApplied').get('totalGold') == 0:
                is_complete_mission = True
