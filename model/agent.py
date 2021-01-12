from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random

class Test(dict):
    hey = 4

    def __init__(self):
        dict.__init__(self, hey=self.hey)

class RegionAgent(GeoAgent):

    def __init__(self, unique_id, model, shape):
        """Create a new Region agent.

        Args:
            unique_id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """

        super().__init__(unique_id, model, shape)
        self.wealth = None
        self.country = None
        self.alliance = None
        self.aggressiveness = None
        self.test = None

    def attack(self):
        neighbours = self.model.grid.get_neighbors(self)
        if neighbours:
            target = random.choice(neighbours)
            if self.wealth > target.wealth:
                # attack succesful
                target.country = self.country
                self.model.countries[self.country]["constituing_regions"] += 1
                self.model.countries[target.country]["constituing_regions"] -= 1
    
    def trade(self):
        neighbours = self.model.grid.get_neighbors(self)
        if neighbours:
            target = random.choice(neighbours)
            self.wealth += random.random() * self.model.countries[self.country]["constituing_regions"]
            target.wealth += random.random()  * target.model.countries[self.country]["constituing_regions"]
        
    def step(self):
        if random.random() < self.model.countries[self.country]["aggressiveness"]:
            self.attack()
        else:
            self.trade()

    def __repr__(self):
        return "Agent {} | {}".format(self.unique_id, self.NUTS_ID)