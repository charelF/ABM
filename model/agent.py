from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
import numpy as np
from utilities import *

class SchellingAgent(GeoAgent):

    def __init__(self, unique_id, model, shape, agent_type=None):
        """Create a new Schelling agent.

        Args:
            unique_id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(unique_id, model, shape)
        self.atype = agent_type
        '''
        self.setup()
    
    def setup(self):
        self.wealth = None
        self.country = None
        self.alliance = None
        self.aggressiveness = None
        self.rep = 0
    '''

    def fall(self):
        self.model.countries[self.country]["constituing_regions"] -= 1
        self.country = None

    def take(self, neighbour):
        print(self.country)
        neighbour.country = self.country
        print(self.country)
        self.model.countries[self.country]["wealth"] -= 1
        self.model.countries[self.country]["constituing_regions"] += 1
        new = self.model.countries[self.country]["rep"] - 0.01
        self.model.countries[self.country]["rep"] -= max(new, 0)

    def step(self):
        """Advance agent one step."""
        if self.country == None:
            return
        if self.model.countries[self.country]["wealth"] < 0:
            self.fall()
            return

        # New code
        neighbors = self.model.grid.get_neighbors(self)

        # Implement that nation loses nation with 0 resources                
        for neighbour in neighbors:
            if neighbour.country == None:
                self.take(neighbour)
                break

            if neighbour.country != self.country:
                if random.random() < self.model.interaction_chance:
                    self.get_interaction(neighbour)
                    break
    
    def get_interaction(self, neighbour):
        """
        Given a neighbouring area, decides what kind
        of interaction takes place.
        """
        # Iterate over class object

        aggress_self = False
        aggress_other = False

        # Still need to incorporate reputation somehow
        if self.country != None and neighbour.country != None:
            if random.random() < self.model.countries[self.country]["aggressiveness"] - self.model.countries[neighbour.country]["rep"]:
                aggress_self = True
            if random.random() < self.model.countries[neighbour.country]["aggressiveness"] - self.model.countries[self.country]["rep"]:
                aggress_other = True
            
            self.update_nations(neighbour, aggress_self, aggress_other)

    def update_nations(self, nation_2, agress_1, agress_2):
        """
        Given 2 nations and their tactics updates the attributes
        of those nations.
        """
        # Rep between -1 and 1
        if agress_1:
            new = self.model.countries[self.country]["rep"] - 0.01
            self.model.countries[self.country]["rep"] = max(new, 0)
        else:
            new = self.model.countries[self.country]["rep"] + 0.01
            self.model.countries[self.country]["rep"] = min(new, 1)
        if agress_2:
            new = self.model.countries[nation_2.country]["rep"] - 0.01
            self.model.countries[nation_2.country]["rep"] = max(new, 0)
        else:
            new = self.model.countries[nation_2.country]["rep"] + 0.01
            self.model.countries[nation_2.country]["rep"] = min(new, 1)     

        if agress_1 and agress_2:
            self.model.countries[self.country]["wealth"] -= self.model.war_reward
            self.model.countries[nation_2.country]["wealth"] -= self.model.war_reward
        elif agress_1 and not agress_2:
            self.model.countries[self.country]["wealth"] += self.model.alliance_war_reward
            self.model.countries[nation_2.country]["wealth"] -= self.model.alliance_war_reward
        elif not agress_1 and agress_2:
            self.model.countries[self.country]["wealth"] -= self.model.alliance_war_reward
            self.model.countries[nation_2.country]["wealth"] += self.model.alliance_war_reward
        else:
            self.model.countries[self.country]["wealth"] += self.model.alliance_reward
            self.model.countries[nation_2.country]["wealth"] += self.model.alliance_reward        

        if self.model.countries[self.country]["wealth"] < 0:
            self.fall()
        if self.model.countries[nation_2.country]["wealth"] < 0:
            nation_2.fall()
        

    def __repr__(self):
        return "Agent " + str(self.unique_id)