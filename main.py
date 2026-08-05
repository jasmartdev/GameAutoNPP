import time
import json
import re
import requests
import threading
import health_check_server
import utils_game
from account import Account

if __name__ == '__main__':
    health_thread = threading.Thread(target=health_check_server.run_health_check_server, daemon=True)
    health_thread.start()
    #NPP
    account1 = Account(authorization='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF5ZXJJZCI6IjA2MGUxNjNiLWJhZmMtNDNmNS1iNmI2LWEzNjY1ZTFkZTAxOCIsImlhdCI6MTc4NTkzNTM4MiwiZXhwIjoxNzkzNzExMzgyfQ.4h0hnwF6tRa0DyBnbPhquQGhaaQXXYH7Qc7_C1YqUAg', id='060e163b-bafc-43f5-b6b6-a3665e1de018')
    game_headers = account1.get_headers()
    current_missionId = 1
    current_monstersKilled = 1000
    current_sleep_time = 80
    is_test_monsters = True
    is_complete_mission = False
    #Challenge
    monsters_killed_array = [319, 404, 440, 341]
    current_worldId = 1
    challengen_state = 0 #0: chua kiem tra, 1: da kiem tra, 2: da bat dau
    start_challegen_time = 0
    while True:
        account1.set_start_mission_body(current_missionId)
        response = requests.post(
            url=account1.get_start_mission_url(), 
            headers=game_headers, 
            data=account1.get_start_mission_body()
        )
        try:
            data = response.json()
        except Exception as e:
            print(e)
            continue
        #utils_game.my_print(data)
        data_error = data.get('error')
        if data_error:
            if 'Cannot replay completed mission' in data_error:
                numbers = re.findall(r"\d+", data_error)
                current_missionId = int(numbers[1] if len(numbers) >  1 else None)
                continue
            else:
                time.sleep(current_sleep_time * 2)
        if is_test_monsters:
            account1.set_complete_mission_body(current_missionId, False, 1000)
        else:
            time.sleep(current_sleep_time)
            if is_complete_mission:
                account1.set_complete_mission_body(current_missionId, True, current_monstersKilled + 1)
            else:
                account1.set_complete_mission_body(current_missionId, False, current_monstersKilled)
        response = requests.post(
            url=account1.get_complete_mission_url(), 
            headers=game_headers, 
            data=account1.get_complete_mission_body()
        )
        try:
            data = response.json()
        except Exception as e:
            print(e)
            continue
        #utils_game.my_print(data)
        data_error = data.get('error')
        if data_error:
            if data.get('code') == 'SERVER_ERROR':
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
            elif data.get('goldLimit') and data.get('goldLimit').get('earnedAfter') == data.get('goldLimit').get('cap') and current_missionId < 30:
                is_complete_mission = True
            #Challenge
            if challengen_state == 0:
                if data.get('player') and data.get('player').get('challengeCurrentWorld'):
                    current_worldId = data.get('player').get('challengeCurrentWorld')
                    if data.get('player').get('challengeTickets') == 0:
                        challengen_state = 1
                    else:
                        challengen_state = 2
                        account1.set_start_challenge_body(current_worldId)
                        try:
                            utils_game.my_print_response(requests.post(
                                url=account1.get_start_challenge_url(), 
                                headers=game_headers, 
                                data=account1.get_start_challenge_body()
                            ))
                        except Exception as e:
                            print(e)
                            continue
                        start_challegen_time = time.time()
            elif challengen_state == 2:
                if time.time() - start_challegen_time > 300:
                    account1.set_complete_challenge_body(current_worldId, True, monsters_killed_array[current_worldId%4])
                    try:
                        utils_game.my_print_response(requests.post(
                            url=account1.get_complete_challenge_url(), 
                            headers=game_headers, 
                            data=account1.get_complete_challenge_body()
                        ))
                    except Exception as e:
                        print(e)
                        continue
                    challengen_state = 0
            #Forge
            if data.get('player'):
                forgeSlots = data.get('player').get('forgeSlots')
                #utils_game.my_print(forgeSlots)
                if forgeSlots:
                    i = 0
                    for forgeSlot in forgeSlots:
                        #utils_game.my_print(forgeSlot)
                        if forgeSlot:
                            try:
                                current_timestamp = time.time() * 1000
                                if current_timestamp > forgeSlot.get('startTime') + forgeSlot.get('craftTimeMs'):
                                    account1.set_forge_claim_body(i)
                                    utils_game.my_print_response(requests.post(
                                        url=account1.get_forge_claim_url(), 
                                        headers=game_headers, 
                                        data=account1.get_forge_claim_body()
                                    ))
                                    time.sleep(2)
                                    utils_game.my_print_response(requests.post(
                                        url=account1.get_forge_craft_url(), 
                                        headers=game_headers
                                    ))
                            except Exception as e:
                                print(e)
                                continue
                        else:
                            try:
                                utils_game.my_print_response(requests.post(
                                    url=account1.get_forge_craft_url(), 
                                    headers=game_headers
                                ))
                            except Exception as e:
                                print(e)
                                continue
                        i = i + 1
