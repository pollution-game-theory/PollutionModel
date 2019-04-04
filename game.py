from resource import Resource

class Game:
    #value 1 = the cost, value 2 = the damage/pollution, value 3 = the value to the countries (i.e. how much it fills their need)
    r1 = Resource(10,2,5)
    r2 = Resource(5,5,5)
    r3 = Resource(2,10,5) 
    totalpollution = 0
    gametime = 0
    #value 1 = budget, value 2 = need, value 3 = growth
    developing = Country(1000, 200, 100)
    developed = Country(100000, 20000, 10000)
    
