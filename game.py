import random
from resource import Resource
from country import Country

class Game:
    #resource variables
    #value 1 = the monetary cost of the resource
    #value 2 = the amount of damage/pollution created by using the resource once
    #value 3 = the value to the countries (i.e. how much it fills their need)
    #value 4 = the crisis risk

    #country variables
    #value 1 = budget, value 2 = need, value 3 = growth
    #the budget is the total money available for use in the country
    #the need is how much value they need per round (i.e. a country with a need of 200 would need 100 of a resource with the value 2 per round.
    #the growth is a steady value that gets added to the budget every round.
    def __init__ (self,
                  r1 = Resource(10,2,5,0),
                  r2 = Resource(5,5,5,4),
                  r3 = Resource(2,10,5,12),
                 Agents = [Country(1000, 200, 100),Country(100000, 20000, 10000)]):
        self.rl = [r1, r2, r3]
        self.total_pollution = 0
        self.total_risk = 0
        self.catastrophes = 0
        self.gametime = 0
        self.developing = Agents[0]
        self.developed = Agents[1]
    
    def take_turn(self, country):
        rrc = random.choice(self.rl)
        x = country.need
        country.budget += country.growth
        
        self.total_risk += rrc.crisisRisk
        if random.randint(0,100)< self.total_risk:
            self.total_pollution +=40
            self.total_risk += -10
            self.catastrophes += 1
            
        while x > -1 and country.budget > 0:
            country.budget -= rrc.cost
            x -= rrc.value
            self.total_pollution += rrc.damage
        if x > 0:
            print("")
            print("country has failed, no money left")
    
    def play_round(self):
        self.take_turn(self.developing)
        self.take_turn(self.developed)
        self.gametime += 1
x = Game()

while x.total_pollution < 1000000:
    x.play_round()
    print(["Total Pollution: ", x.total_pollution])
    print(["Length of Game: ", x.gametime])
    print(["Player1 budget: ", x.developing.budget])
    print(["Player2 budget: ",x.developed.budget])
    print(["Total Pollution: ", x.total_pollution])
    print(["Total Risk: ",x.total_risk])
    print(["Total Catastrophes :", x.catastrophes])
    print("")

