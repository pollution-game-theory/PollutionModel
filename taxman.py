class Taxman:
    def __init__(self, interventionThreshold = 10000, interventionIntensity=2, interventionFrequency=2, interventionLength= 8, thresholdIncreaseRate = 10000, reset = False):
        self.interventionThreshold = interventionThreshold #pollution level that initiates intervention
        self.interventionIntensity = interventionIntensity #scale of 1-3 how much to tweak prices
        self.interventionFrequency = interventionFrequency #the ratio of rounds-since-the-start-of-intervention: # of tweaks to the prices
        self.interventionLength = interventionLength #how many rounds the intervention lasts
        self.thresholdIncreaseRate = thresholdIncreaseRate # how to update the threshold after the intervention
        self.reset = reset # whether the prices reset at the end of the intervention
        self.interventionStage = 0 # of rounds since the intervention began
        self.interventionInProgress = False
        self.interventionTally = 0 # of interventions this Taxman has performed

