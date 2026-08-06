import json

class Account:

    def __init__(self, authorization, id):
        self.authorization = authorization
        self.id = id
        self.headers = {'sec-ch-ua-platform': '"Windows"', 'authorization': '', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36', 'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"', 'content-type': 'application/json', 'sec-ch-ua-mobile': '?0', 'accept': '*/*', 'origin': 'https://wall-wars.game-files.crazygames.com', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://wall-wars.game-files.crazygames.com/', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9', 'priority': 'u=1, i'}
        self.start_mission_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/start-mission'
        self.start_mission_body = b'{"missionId":1}'
        self.complete_mission_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/complete-mission'
        self.complete_mission_body = b'{"missionId":1,"victory":false,"monstersKilled":1000,"antiCheat":{"version":1,"team":[1,11,4,5,12],"waves":[]}}'
        self.start_challenge_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/challenge/start'
        self.start_challenge_body = b'{"worldId":1}'
        self.complete_challenge_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/challenge/complete'
        self.complete_challenge_body = b'{"worldId":1,"victory":true,"wavesCompleted":10,"monstersKilled":1000,"battleEvents":[],"antiCheat":{"version":1,"team":[1,11,4,5,12],"waves":[]}}'
        self.start_goldecave_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/goldMine/complete'
        self.start_goldecave_body = b'{"viaAd":true}'
        self.complete_goldecave_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/goldMine/complete'
        self.complete_goldecave_body = b'{"level":1,"victory":true,"wavesCompleted":5,"monstersKilled":110,"battleEvents":[]}'
        self.forge_claim_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/forge/claim'
        self.forge_claim_body = b'{"slotIndex":1}'
        self.forge_craft_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/forge/craft'
        self.rewards_url = 'https://defense-wall-production.up.railway.app/api/player/{0}/idle/open-rewards'
        self.headers['authorization']=authorization
        self.start_mission_url = self.start_mission_url.format(self.id)
        self.complete_mission_url = self.complete_mission_url.format(self.id)
        self.start_challenge_url = self.start_challenge_url.format(self.id)
        self.complete_challenge_url = self.complete_challenge_url.format(self.id)
        self.forge_claim_url = self.forge_claim_url.format(self.id)
        self.forge_craft_url = self.forge_craft_url.format(self.id)
        self.rewards_url = self.rewards_url.format(self.id)

    def get_headers(self):
        return self.headers
    def get_start_mission_url(self):
        return self.start_mission_url
    def set_start_mission_body(self, missionId):
        json_data = json.loads(self.start_mission_body.decode('utf-8'))
        json_data['missionId'] = missionId
        self.start_mission_body = json.dumps(json_data).encode('utf-8')
    def get_start_mission_body(self):
        return self.start_mission_body
    def get_complete_mission_url(self):
        return self.complete_mission_url
    def set_complete_mission_body(self, missionId, victory, monstersKilled):
        json_data = json.loads(self.complete_mission_body.decode('utf-8'))
        json_data['missionId'] = missionId
        json_data['victory'] = victory
        json_data['monstersKilled'] = monstersKilled
        self.complete_mission_body = json.dumps(json_data).encode('utf-8')
    def get_complete_mission_body(self):
        return self.complete_mission_body
    def get_start_challenge_url(self):
        return self.start_challenge_url
    def set_start_challenge_body(self, worldId):
        json_data = json.loads(self.start_challenge_body.decode('utf-8'))
        json_data['worldId'] = worldId
        self.start_challenge_body = json.dumps(json_data).encode('utf-8')
    def get_start_challenge_body(self):
        return self.start_challenge_body
    def get_complete_challenge_url(self):
        return self.complete_challenge_url
    def set_complete_challenge_body(self, worldId, victory, monstersKilled):
        json_data = json.loads(self.complete_challenge_body.decode('utf-8'))
        json_data['worldId'] = worldId
        json_data['victory'] = victory
        json_data['monstersKilled'] = monstersKilled
        self.complete_challenge_body = json.dumps(json_data).encode('utf-8')
    def get_complete_challenge_body(self):
        return self.complete_challenge_body
    def get_start_goldecave_url(self):
        return self.start_goldecave_url
    def set_start_goldecave_body(self, viaAd):
        json_data = json.loads(self.start_goldecave_body.decode('utf-8'))
        json_data['viaAd'] = viaAd
        self.start_goldecave_body = json.dumps(json_data).encode('utf-8')
    def get_start_goldecave_body(self):
        return self.start_goldecave_body
    def get_complete_goldecave_url(self):
        return self.complete_goldecave_url
    def set_complete_goldecave_body(self, level, victory, monstersKilled):
        json_data = json.loads(self.complete_goldecave_body.decode('utf-8'))
        json_data['level'] = level
        json_data['victory'] = victory
        json_data['monstersKilled'] = monstersKilled
        self.complete_goldecave_body = json.dumps(json_data).encode('utf-8')
    def get_complete_goldecave_body(self):
        return self.complete_goldecave_body
    def get_forge_claim_url(self):
        return self.forge_claim_url
    def set_forge_claim_body(self, slotIndex):
        json_data = json.loads(self.forge_claim_body.decode('utf-8'))
        json_data['slotIndex'] = slotIndex
        self.forge_claim_body = json.dumps(json_data).encode('utf-8')
    def get_forge_claim_body(self):
        return self.forge_claim_body
    def get_forge_craft_url(self):
        return self.forge_craft_url
    def get_rewards_url(self):
        return self.rewards_url
