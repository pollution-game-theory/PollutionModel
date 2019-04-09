import random
from resource import Resource
from country import Country

class Game:
    #value 1 = the monetary cost of the resource
    #value 2 = the amount of damage/pollution created by using the resource once
    #value 3 = the value to the countries (i.e. how much it fills their need)
    r1 = Resource(10,2,5)
    r2 = Resource(5,5,5)
    r3 = Resource(2,10,5)
    rx = [r1, r2, r3]
    total_pollution = 0
    gametime = 0
    #value 1 = budget, value 2 = need, value 3 = growth
    #the budget is the total money available for use in the country
    #the need is how much value they need per round (i.e. a country with a need of 200 would need 100 of a resource with the value 2 per round.
    #the growth is a steady value that gets added to the budget every round.
    developing = Country(1000, 200, 100)
    developed = Country(100000, 20000, 10000)
    
    def take_turn(self, country):
        rrc = random.choice(self.rx)
        x = country.need
        country.budget += country.growth
        while x > -1 and country.budget > 0:
            country.budget -= rrc.cost
            x -= rrc.value
            self.total_pollution += rrc.damage
        if x > 0:
            print("country has failed, no money left")
    
    def play_round(self):
        self.take_turn(self.developing)
        self.take_turn(self.developed)
        self.gametime += 1
x = Game()

while x.total_pollution < 1000000:
    x.play_round()
    print(x.total_pollution)
print(x.gametime)
print(x.developing.budget)
print(x.developed.budget)
