class Resource:
    #resource variables
    #value 1 = the monetary cost of the resource
    #value 2 = the amount of damage/pollution created by using the resource once
    #value 3 = the value to the countries (i.e. how much it fills their need)
    #value 4 = the crisis risk
    #value 5 = unlock variable: some resources have a high initial cost and low subsequent cost. unlock of 1 means that there is an initial cost
    #value 6 = unlock cost (not used right now, so everything is set to 0).
    def __init__(self, cost, damage, value, crisisrisk, unlock, unlockcost):
        self.cost = cost
        self.damage = damage
        self.value = value
        self.crisisRisk = crisisrisk
        self.unlock = unlock
        self.unlockcost = unlockcost
