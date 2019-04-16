class Country:
    #country variables
    #value 1 = budget, value 2 = need, value 3 = growth
    #the budget is the total money available for use in the country
    #the need is how much value they need per round (i.e. a country with a need of 200 would need 100 of a resource with the value 2 per round.
    #the growth is a steady value that gets added to the budget every round.
    def __init__(self, budget, need, growth):
        self.budget = budget
        self.need = need
        self.growth = growth
