import requests
import csv
import time
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')

myPUUID = requests.get(
    f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Bitmapper?api_key={API_KEY}"
    ).json()['puuid']

def getMyMatches(num):
    numOfHundredMatches = num // 100
    numOfRemainingMatches = num % 100
    numOfQueriedHundredMatches = 0
    startIndex = 0
    matchIDList = []
    while numOfQueriedHundredMatches < numOfHundredMatches:
        url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{myPUUID}/ids?type=ranked&"
        f"start={startIndex}&count=100&api_key={API_KEY}")
        matchIDList = matchIDList + requests.get(url).json()
        numOfQueriedHundredMatches = numOfQueriedHundredMatches + 1
        startIndex = startIndex + 100
    if numOfRemainingMatches != 0:
        url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{myPUUID}/ids?type=ranked&"
        f"start={startIndex}&count={numOfRemainingMatches}&api_key={API_KEY}")
        matchIDList = matchIDList + requests.get(url).json()
    return matchIDList

def CSV_save(matchIDList):
    damageVals = [['matchID', 'allyTeamDmg', 'enemyTeamDmg', 'win']]
    first = True
    count = 0
    for matchID in matchIDList:
        if ((first == True) and count == 90) or ((first == False) and (count == 100)):
            time.sleep(120)
            first = False
            count = 0
        print(matchID)
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}"
        matchData = requests.get(url).json()
        try:
            participants = matchData['info']['participants']
        except:
            continue
        team1_Dmg = 0
        team2_Dmg = 0
        allyTeamDmg = 0
        enemyTeamDmg = 0
        myParticipantIndex = 0
        teamIndex = 0
        isWin = None
        for participantIndex in range(0, len(participants)):
            participantDmg = participants[participantIndex]['totalDamageDealt']
            if participantIndex <= 4:
                team1_Dmg = team1_Dmg + participantDmg
            elif participantIndex > 4:
                team2_Dmg = team2_Dmg + participantDmg
            if participants[participantIndex]['puuid'] == myPUUID:
                myParticipantIndex = participantIndex
        if myParticipantIndex <= 4:
            allyTeamDmg = team1_Dmg
            enemyTeamDmg = team2_Dmg
            teamIndex = 0
        elif myParticipantIndex > 4:
            allyTeamDmg = team2_Dmg
            enemyTeamDmg = team1_Dmg
            teamIndex = 1
        if (
            (matchData['info']['teams'][0]['win'] == True) and (teamIndex == 0)
            ) or (
            (matchData['info']['teams'][1]['win'] == True) and (teamIndex == 1)
            ):
            isWin = 1
        else:
            isWin = 0
        damageVals.append([matchID, allyTeamDmg, enemyTeamDmg, isWin])
        count = count + 1
    return damageVals

def main():
    damageVals = CSV_save(getMyMatches(680))
    with open('damageVals.csv', 'w', newline='') as damageValsFile:
        csvWriter = csv.writer(damageValsFile)
        for row in damageVals:
            csvWriter.writerow(row)

if __name__ == '__main__':
    main()
