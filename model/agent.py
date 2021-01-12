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

    def trade(self, neighbor):
        self.country.wealth     += self.model.trade_reward
        neighbor.country.wealth +=  self.model.trade_reward

    def deficit(self, neighbor, deficit):
        """
        deficit indicates who deficits: 1 is neighbour
        -1 is self.
        """
        self.country.wealth     -= deficit * self.model.deficit_reward
        neighbor.country.wealth += deficit * self.model.deficit_reward                

    def both_deficit(self, neighbor):

        self.country.wealth     -= self.model.deficit_reward
        neighbor.country.wealth -= self.model.deficit_reward  

    def choose_interaction(self):
        """
        Chooses an interaction True means trade
        and False means deficit
        """
        if self.country.strat == 1:
            if self.country.attacked:
                return True
            else:
                return False
        elif self.country.strat == 2:
            if random.random() < self.country.aggressiveness:
                return True    
            else:
                return False


    def step(self):
        """Advance agent one step."""

        # See if country has interacted
        if self.country.interacted:
            return
        # New code
        try:
            neighbor = random.choice(self.model.grid.get_neighbors(self))
            neighbor.country.interacted = True
                            
            if neighbor.country == self.country:
                self.trade(neighbor)
                self.country.traded = True
            else:
                self.country.traded = self.choose_interaction()
                neighbor.country.traded = neighbor.choose_interaction()

                # Update nation params
                if self.country.trade:
                    self.country.trades += 1
                if neighbor.country.trade:
                    neighbor.country.trades += 1
                
                # Interaction
                if self.country.trade and neighbor.country.trade:
                    self.trade(neighbor)
                    self.country.attacked = False
                    self.neighbour.attacked = False
                # Read doc of deficit to understand 1, -1 args.
                elif self.country.trade and not neighbor.country.trade:
                    self.country.attacked = True
                    self.neighbour.attacked = False
                    self.deficit(neighbor, 1)
                elif self.country.trade and not neighbor.country.trade:
                    self.country.attacked = False
                    self.neighbour.attacked = True
                    self.deficit(neighbor, -1)
                else:
                    self.country.attacked = True
                    self.neighbour.attacked = True
                    self.both_deficit(neighbor)
        except:
            # When country has no neighbors
            self.country.traded = False

    def __repr__(self):
        return "Agent " + str(self.unique_id)