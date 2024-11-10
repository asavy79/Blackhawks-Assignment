import json
import sys


class RosterCapData:
    def __init__(self, jsonFileName, teamName):
        try:
            fileStream = open(jsonFileName, "r")
            self.fileStream = fileStream
            self.file = json.load(fileStream)
            self.roster = self.file['roster']
            self.forwards = self.roster['forwards']
            self.defense = self.roster['defense']
            self.goalies = self.roster['goalies']
            self.deadCap = self.file['deadCap']
            self.teamName = teamName

        except:
            print("Cannot read file")
            sys.exit(0)

    def getPositionCapHit(self, position, year):
        if position == "goalies":
            playerList = self.goalies
        elif position == "defense":
            playerList = self.defense
        elif position == "forwards":
            playerList = self.forwards
        else:
            print("Cannot read position")
            return
        capHit = 0
        for player in playerList:
            yearlyContracts = player['contracts'][0]['details']
            for seasonDetails in yearlyContracts:
                if seasonDetails['season'] == year:
                    capHitString = seasonDetails['capHit']
                    if capHitString:
                        capHit += int(seasonDetails['capHit']
                                      [1:].replace(',', ''))
                    break
        return capHit

    def getBuyoutCapHit(self, year):
        playerList = self.deadCap['buyoutHistory']
        capHit = 0
        for player in playerList:
            yearlyContracts = player['contracts'][0]['details']
            for seasonDetails in yearlyContracts:
                if seasonDetails['season'] == year:
                    if seasonDetails.get('buyout', ""):
                        capHitString = seasonDetails['buyout']['capHit']
                        if capHitString:
                            capHit += int(seasonDetails['buyout']['capHit']
                                          [1:].replace(',', ''))
                        break
        return capHit

    def getRetainedSalaryCapHit(self, year):
        playerList = self.deadCap['retainedSalary']
        capHit = 0
        for player in playerList:
            yearlyContracts = player['contracts'][0]['details']
            for seasonDetails in yearlyContracts:
                if seasonDetails['season'] == year:
                    capHitString = seasonDetails['retention'][self.teamName]
                    if capHitString:
                        capHit += int(seasonDetails['capHit']
                                      [1:].replace(',', ''))
                    break
        return capHit

    def getBuriedPenaltyCapHit(self, year):
        playerList = self.deadCap['buriedPenalty']
        capHit = 0
        for player in playerList:
            yearlyContracts = player['contracts'][0]['details']
            for seasonDetails in yearlyContracts:
                if seasonDetails['season'] == year:
                    capHitString = seasonDetails['capHit']
                    if capHitString:
                        capHit += int(seasonDetails['capHit']
                                      [1:].replace(',', ''))
                    break
        return capHit

    def getRosterCapHit(self, year):
        goalieCapHit = self.getPositionCapHit("goalies", year)
        forwardCapHit = self.getPositionCapHit("forwards", year)
        defenseCapHit = self.getPositionCapHit("defense", year)
        total = goalieCapHit + forwardCapHit + defenseCapHit

        return {
            "goalies": goalieCapHit,
            "forwards": forwardCapHit,
            "defense": defenseCapHit,
            "total": total, }

    def displayRosterCapHit(self, year):
        breakdown = self.getRosterCapHit(year)

        print("Roster Cap Hit Breakdown by Position:")
        print(f"Goalies: ${breakdown['goalies']:,}")
        print(f"Forwards: ${breakdown['forwards']:,}")
        print(f"Defense: ${breakdown['defense']:,}")
        print(f"Total: ${breakdown['total']:,}")

    def getDeadCapHit(self, year):
        buriedPenaltyCapHit = self.getBuriedPenaltyCapHit(year)
        retainedSalaryCapHit = self.getRetainedSalaryCapHit(year)
        buyoutCapHit = self.getBuyoutCapHit(year)
        total = buriedPenaltyCapHit + retainedSalaryCapHit + buyoutCapHit

        return {
            "buriedPenalty": buriedPenaltyCapHit,
            "retainedSalary": retainedSalaryCapHit,
            "buyout": buyoutCapHit,
            "total": total,
        }

    def displayDeadCapHit(self, year):
        breakdown = self.getDeadCapHit(year)

        print(f"Dead Cap Hit Breakdown: ")
        print(f"Buried Penalty: ${breakdown['buriedPenalty']:,}")
        print(f"Retained Salary: ${breakdown['retainedSalary']:,}")
        print(f"Buy Out: ${breakdown['buyout']:,}")
        print(f"Total: ${breakdown['total']:,}")

    def getCapSpace(self, year):
        upperLimit = self.file['teamSummary']['upperLimit']
        carryOver = self.file['teamSummary']['carryover']

        rosterCapHit = self.getRosterCapHit(year)['total']
        deadCapHit = self.getDeadCapHit(year)['total']

        total = upperLimit - (carryOver + rosterCapHit + deadCapHit)

        return total

    def __del__(self):
        self.fileStream.close()


FlyersRoster = RosterCapData("capdata.json", "Philadelphia Flyers")

FlyersRoster.displayRosterCapHit("2024-25")
print("")
FlyersRoster.displayDeadCapHit("2024-25")
print("")
total = FlyersRoster.getCapSpace("2024-25")
print(f"Total Cap Space: ${total:,}")
