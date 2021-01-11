from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
from simulate_battle import *
import random


class SchellingAgent(GeoAgent):
    def __init__(
        self, unique_id, model, shape, agent_type=None, wealth=0, army=0,
    ):
        """Create a new Schelling agent.

        Args:
            unique_id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(unique_id, model, shape)
        self.atype = agent_type
        self.wealth = wealth
        self.army = army

    # def transfer_troops(self):
    #     available_troops = self.model.armies[self.atype][1:]

    #     # for region_id in available_troops:
    #     troops = self.agents
    #     print(troops)

    def step(self):
        """Advance agent one step."""

        neighbors = self.model.grid.get_neighbors(self)
        recources = 0

        for ag in self.model.grid.agents:
            if ag.atype == self.atype:
                recources += 1

        self.income = recources
        self.upkeep = self.army * 0.5

        self.change = self.income - self.upkeep

        self.wealth += self.change

        self.happiness = 1 / recources

        self.hostility = (self.happiness - self.model.min_happy) / (
            self.model.max_happy - self.model.min_happy
        )

        if self.wealth < 0:
            self.army -= 1

        elif self.wealth > 0 and self.change > 0.5:
            self.army += 1

        if neighbors:
            # self.transfer_troops()
            for neighbor in neighbors:
                if 1 < self.army > neighbor.army and self.atype != neighbor.atype:
                    outcome = battle(self.army - 1, neighbor.army)

                    # Battle won
                    if outcome > 0:
                        neighbor.atype = self.atype
                        neighbor.army = outcome
                        self.army = 1

                    else:
                        self.army = 1
                        neighbor.army = -outcome

    def __repr__(self):
        return "Agent " + str(self.unique_id)
