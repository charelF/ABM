from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random

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

    def attack(self):
        neighbours = self.model.grid.get_neighbors(self)
        target = random.choice(neighbours)
        if self.wealth > target.wealth:
            # attack succesful
            target.country = self.country
    
    def trade(self):
        neighbours = self.model.grid.get_neighbors(self)
        target = random.choice(neighbours)
        self.wealth += 0.2 * self.wealth
        target.wealth += 0.2 * target.wealth
        
    def step(self):
        if random.random() > 0.5:
            self.attack()
        else:
            self.trade()

    def __repr__(self):
        return "Agent {} | {}".format(self.unique_id, self.NUTS_ID)