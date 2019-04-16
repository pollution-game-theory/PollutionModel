import random
import Country
import Resource
import Taxman

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
    def __init__(self):
        self.r1 = Resource("Coal",40,50,50,1,1,0)
        self.r2 = Resource("Wind/Solar",90,0,30,0,1,0)
        self.r3 = Resource("Nuclear",70,25,40,2,1,0)
        self.rl = [self.r1, self.r2, self.r3]
        self.total_pollution = 0
        self.total_risk = 0
        self.catastrophes = 0
        self.gametime = 0
        self.countries =[Country(25000, 1100, 1000),Country(10000, 300, 200)]
        self.Taxman = Taxman()
        self.threshold = 100000
        self.global_collapse = False
        self.country_collapse = False
        self.currentResPrices = self.get_r_prices()
    
    def get_r_prices(self):
        def pd(n, d):
            return (n / d) if d else n
        r_prices = []
        for r in self.rl:
            r_prices.append(round(pd(r.value, r.cost), 3))
        return r_prices
    
    def take_turn(self, country, supply, fullsupplycost1, fullsupplycost2, fullsupplycost3):
        self.supply = supply
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
        if random.randint(0,100)< self.total_risk:
            self.total_pollution +=10000
            self.total_risk += -10
            self.catastrophes += 1
            
        while x > -1 and country.budget > 0:
            self.r1.cost = fullsupplycost1 * ((1000 -(.5*self.supply[0]))/500)* (random.randint(9,12)/10)
            self.r2.cost = fullsupplycost2 * ((1000 -(.5*self.supply[1]))/500)* (random.randint(9,12)/10)
            self.r3.cost = fullsupplycost3 * ((1000 -(.5*self.supply[2]))/500)* (random.randint(9,12)/10)
            self.rl = [self.r1, self.r2, self.r3]
            self.currentResPrices = self.get_r_prices()
            rrc = self.rl[self.currentResPrices.index(max(self.currentResPrices))]
            self.supply[self.currentResPrices.index(max(self.currentResPrices))] -= 1
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
                    self.r2.cost = 90
                self.Taxman.interventionInProgress = False
        
        fullsupplycost1,fullsupplycost2,fullsupplycost3 = self.r1.cost* (random.randint(9,12)/10),self.r2.cost* (random.randint(9,12)/10),self.r3.cost * (random.randint(9,12)/10)   
        self.supply = [1000,1000,1000]
            
        for country in self.countries:
            self.take_turn(country,self.supply,fullsupplycost1,fullsupplycost2,fullsupplycost3)
        
        self.r1.cost,self.r2.cost,self.r3.cost = fullsupplycost1* (random.randint(9,12)/10),fullsupplycost2* (random.randint(9,12)/10),fullsupplycost3* (random.randint(9,12)/10)
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
