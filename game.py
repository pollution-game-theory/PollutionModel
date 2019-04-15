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
    #value 6 = unlock cost.

    #country variables
    #value 1 = budget, value 2 = need, value 3 = growth
    #the budget is the total money available for use in the country
    #the need is how much value they need per round (i.e. a country with a need of 200 would need 100 of a resource with the value 2 per round.
    #the growth is a steady value that gets added to the budget every round.
    
    #r1 = coal
    #r2 = electricity
    #r3 = nuclear
    def __init__(self,
                  r1 = Resource("Coal",40,40,60,4,1,0),
                  r2 = Resource("Wind/Solar",80,10,40,0,1,0),
                  r3 = Resource("Nuclear",60,20,80,10,1,0),
                  countries = [Country(100000, 8000, 10000),Country(1000000, 80000, 100000)],
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
        self.total_pollution = total_pollution
        self.total_risk = total_risk
        self.catastrophes = catastrophes
        self.gametime = gametime
        self.countries = countries
        self.Taxman = Taxman
        self.threshold = threshold
        self.global_collapse = global_collapse
        self.country_collapse = country_collapse
        self.currentResPrices = self.get_r_prices()
    
    def get_r_prices(self):
        def pd(n, d):
            return n / d if d else n
        r_prices = []
        for r in self.rl:
            r_prices.append(round(pd(r.value, r.cost), 3))
        return r_prices
    
    def take_turn(self, country):
        self.currentResPrices = self.get_r_prices()
        #rrc now stands for round-resource-choice
        rrc = self.rl[self.currentResPrices.index(max(self.currentResPrices))]
        if rrc.unlock == 1:
            if rrc.unlockcost > country.budget:
                print ("country can't pay for this resource")
                return
            country.budget -= rrc.unlockcost
            rrc.unlock = 0
        x = country.need
        country.budget += country.growth
        
        self.total_risk += rrc.crisisRisk
        if random.randint(0,200)< self.total_risk:
            self.total_pollution +=5000
            self.total_risk += -10
            self.catastrophes += 1
            
        while x > -1 and country.budget > 0:
            country.budget -= rrc.cost
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
            
        for country in self.countries:
            self.take_turn(country)
        
        self.gametime += 1

    def fix_pollution(self, cost):
        self.total_pollution -= cost*100
        
    def playgame(self):
        
        while self.global_collapse == False and self.country_collapse == False:
            self.play_round()
            print("Current Resource Prices:", end = " ")
            for i in range(0, len(self.rl)):
                print(self.rl[i].name, self.currentResPrices[i], end = " ")
            print("")
            print("Length of Game:", self.gametime)
            print("Total Interventions:", self.Taxman.interventionTally)
            for i in range(0, len(self.countries)):
                print("Player", i, "budget:", self.countries[i].budget)
            print("Total Global Pollution:", self.total_pollution, "/", self.threshold)
            print("Current Total Global Risk:", self.total_risk)
            print("Total Global Crises:", self.catastrophes)
            print("")
        if self.country_collapse == True:
            print("")
            print("Game Over: Country Collapse due to Insufficient Funds!")
        if self.global_collapse == True:
            print("")
            print("Game Over: Global Collapse!")

x = Game()
x.playgame()
