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
    #JSMD
    # account1 = Account(authorization='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF5ZXJJZCI6ImQ0ZTVjYzc0LWU4ZTEtNDFmNC05MmQ2LTE0NTBhNTk2ZTRhZSIsImlhdCI6MTc4NTI0NzQ4NSwiZXhwIjoxNzkzMDIzNDg1fQ.okSBjmZkK4RUYOUXs0mU2pWBhB6kIEKPQeE4VXEaBFc', id='d4e5cc74-e8e1-41f4-92d6-1450a596e4ae')
    #NPP
    account1 = Account(authorization='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF5ZXJJZCI6IjA2MGUxNjNiLWJhZmMtNDNmNS1iNmI2LWEzNjY1ZTFkZTAxOCIsImlhdCI6MTc4NTk4OTU5NiwiZXhwIjoxNzkzNzY1NTk2fQ.yETe9k36GOjI9MytKJOPmBY_opb4-AzWVrbPeD1hILo', id='060e163b-bafc-43f5-b6b6-a3665e1de018')
    game_headers = account1.get_headers()
    current_missionId = 1
    current_monstersKilled = 1000
    current_sleep_time = 80
    is_test_monsters = True
    is_complete_mission = False
    challengen_monsters_killed_array = [319, 404, 440, 341]
    current_worldId = 1
    challengen_state = 1 #0: chua kiem tra, 1: da kiem tra, 2: da bat dau
    start_challegen_time = 0
    goldecave_monsters_killed_array = [194, 110, 149, 184, 50]
    current_level = 1
    goldecave_state = 0 #0: chua kiem tra, 1: da kiem tra, 2: da bat dau
    start_goldecave_time = 0
    response = requests.post(
        url=account1.get_rewards_url(),
        headers=game_headers
    )
    try:
        data = response.json()
    except Exception as e:
        print(e)
    utils_game.my_print(data)
    if data.get('success'):
        if data.get('player') and data.get('player').get('currentMission'):
            current_missionId = data.get('player').get('currentMission')
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
        utils_game.my_print(data)
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
        utils_game.my_print(data)
        data_error = data.get('error')
        if data_error:
            if data.get('code') == 'SERVER_ERROR':
                current_sleep_time = current_sleep_time + 20
            elif 'Invalid monstersKilled' in data_error:
                current_monstersKilled = int(data.get('error').split('-')[1]) - 1
                current_sleep_time = current_monstersKilled*0.7
                is_test_monsters =  False
        elif data.get('success'):
            if is_complete_mission:
                is_test_monsters = True
                is_complete_mission = False
                current_missionId = current_missionId + 1
            elif data.get('goldLimit') and data.get('goldLimit').get('earnedAfter') == data.get('goldLimit').get('cap') and current_missionId < 240:
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
                        start_challegen_time = time.time()
            elif challengen_state == 2:
                if time.time() - start_challegen_time > 300:
                    account1.set_complete_challenge_body(current_worldId, True, challengen_monsters_killed_array[current_worldId%4])
                    try:
                        utils_game.my_print_response(requests.post(
                            url=account1.get_complete_challenge_url(), 
                            headers=game_headers, 
                            data=account1.get_complete_challenge_body()
                        ))
                    except Exception as e:
                        print(e)
                    challengen_state = 0
            #GoldeCave
            if goldecave_state == 0:
                if data.get('player') and data.get('player').get('goldMineCurrentLevel'):
                    current_level = data.get('player').get('goldMineCurrentLevel')
                    if data.get('player').get('goldMineTickets') == 0 and data.get('player').get('goldMineAdUsedThisCycle') == False:
                        goldecave_state = 1
                    else:
                        goldecave_state = 2
                        if data.get('player').get('goldMineTickets') != 0:
                            account1.set_start_goldecave_body(False)
                        else:
                            account1.set_start_goldecave_body(True)
                        try:
                            utils_game.my_print_response(requests.post(
                                url=account1.get_start_goldecave_url(), 
                                headers=game_headers, 
                                data=account1.get_start_goldecave_body()
                            ))
                        except Exception as e:
                            print(e)
                        start_goldecave_time = time.time()
            elif goldecave_state == 2:
                if time.time() - start_goldecave_time > 300:
                    account1.set_complete_goldecave_body(current_level, True, goldecave_monsters_killed_array[current_level%5])
                    try:
                        utils_game.my_print_response(requests.post(
                            url=account1.get_complete_goldecave_url(), 
                            headers=game_headers, 
                            data=account1.get_complete_goldecave_body()
                        ))
                    except Exception as e:
                        print(e)
                    goldecave_state = 0
            #Forge
            if data.get('player'):
                forgeSlots = data.get('player').get('forgeSlots')
                if forgeSlots:
                    i = 0
                    for forgeSlot in forgeSlots:
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
                        else:
                            try:
                                utils_game.my_print_response(requests.post(
                                    url=account1.get_forge_craft_url(), 
                                    headers=game_headers
                                ))
                            except Exception as e:
                                print(e)
                        i = i + 1
