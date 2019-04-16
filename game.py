import random
from country import Country
from resource import Resource
from taxman import Taxman

class Game:
    #resource variables
    #value 1 = the monetary cost of the resource
    #value 2 = the amount of damage/pollution created by using the resource once
    #value 3 = the value to the countries (i.e. how much it fills their need)
    #value 4 = the crisis risk
    #value 5 = unlock variable: some resources have a high initial cost and low subsequent cost. unlock of 1 means that there is an initial cost
    #value 6 = unlock cost (not used right now, so everything is set to 0).

    #country variables
    #value 1 = budget, value 2 = need, value 3 = growth
    #the budget is the total money available for use in the country
    #the need is how much value they need per round (i.e. a country with a need of 200 would need 100 of a resource with the value 2 per round.
    #the growth is a steady value that gets added to the budget every round.
    
    def __init__(self,
                  r1 = Resource(40,40,60,4,1,0), #coal
                  r2 = Resource(80,10,40,0,1,0), #solar
                  r3 = Resource(60,20,80,10,1,0),#nuclear
                  Agents = [Country(100000, 8000, 10000),Country(1000000, 80000, 100000)], #developing, developed
                  Taxman = Taxman(),
                  total_pollution = 0,
                  total_risk = 0,
                  catastrophes = 0,
                  gametime = 0,
                  global_collapse = False,
                  country_collapse = False,
                  threshold = 1000000):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.rl = [r1, r2, r3]
        self.names = ["Coal" ,"Wind/Solar", "Nuclear"]
        self.total_pollution = total_pollution
        self.total_risk = total_risk
        self.catastrophes = catastrophes
        self.gametime = gametime
        self.developing = Agents[0]
        self.developed = Agents[1]
        self.Taxman = Taxman
        self.threshold = threshold
        self.global_collapse = global_collapse
        self.country_collapse = country_collapse
        self.currentResPrices = [self.r1.value/(self.r1.cost + .01),self.r2.value/(self.r2.cost+.01),self.r3.value/(self.r3.cost+.01)]
    
    def take_turn(self, country):
        self.country = country
        self.currentResPrices = [self.r1.value/(self.r1.cost),self.r2.value/(self.r2.cost+.01),self.r3.value/(self.r3.cost+.01)]
        #rrc now stands for round-resource-choice
        rrc = self.rl[self.currentResPrices.index(max(self.currentResPrices))]
        if rrc.unlock == 1:
            if rrc.unlockcost > self.country.budget:
                print ("country can't pay for this resource")
                return
            self.country.budget -= rrc.unlockcost
            rrc.unlock = 0
        x = self.country.need
        self.country.budget += self.country.growth
        
        self.total_risk += rrc.crisisRisk
        if random.randint(0,200)< self.total_risk:
            self.total_pollution +=5000
            self.total_risk += -10
            self.catastrophes += 1
            
        while x > -1 and self.country.budget > 0:
            self.country.budget -= rrc.cost
            x -= rrc.value
            self.total_pollution += rrc.damage
        if x > 0:
            self.country_collapse = True
        if self.total_pollution >= self.threshold:
            self.global_collapse = True
    
    def play_round(self):
        if self.total_pollution >= self.Taxman.interventionThreshold:
            if self.Taxman.interventionInProgress == False:
                self.Taxman.interventionTally += 1
                self.Taxman.interventionInProgress = True
            if self.Taxman.interventionStage < self.Taxman.interventionLength and self.Taxman.interventionStage % self.Taxman.interventionFrequency == 0:
                self.r1.cost += self.Taxman.interventionIntensity * 5
                self.r2.cost -= self.Taxman.interventionIntensity * 5
                if self.r2.cost == 0:
                    self.r2.cost = 10
                self.Taxman.interventionStage += 1
            elif self.Taxman.interventionStage < self.Taxman.interventionLength:
                self.Taxman.interventionStage += 1
            else:
                self.Taxman.interventionStage = 0
                self.Taxman.interventionThreshold = self.total_pollution + self.Taxman.thresholdIncreaseRate
                if self.Taxman.reset == True:
                    self.r1.cost = 40
                    self.r2.cost = 80
                self.Taxman.interventionInProgress = False
            
                
        self.take_turn(self.developing)
        self.take_turn(self.developed)
        self.gametime += 1

    def fix_pollution(self, cost):
        self.total_pollution -= cost*100
        
    def playgame(self):
        
        while self.global_collapse == False and self.country_collapse == False:
            self.play_round()
            print(["Current Resource Price: " + str(self.currentResPrices)])
            print(["Length of Game: " + str(self.gametime)])
            print(["Total Interventions: " + str(self.Taxman.interventionTally)])
            print(["Player1 budget: " + str(self.developing.budget)])
            print(["Player2 budget: "+ str(self.developed.budget)])
            print(["Total Global Pollution: " + str(self.total_pollution) + "/" + str(self.threshold)])
            print(["Current Total Global Risk: "+ str(self.total_risk)])
            print(["Total Global Crises :"+ str(self.catastrophes)])
            print("")
        if self.country_collapse == True:
            print("")
            print("Game Over: Country Collapse due to Insufficient Funds!")
        if self.global_collapse == True:
            print("")
            print("Game Over: Global Collapse!")

x = Game()
x.playgame()
