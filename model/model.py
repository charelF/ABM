from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *


class RegionModel(Model):
    """---"""

    def __init__(self):

        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()

        self.happy = 0
        self.datacollector = DataCollector({"happy": "happy"})

        self.running = True

        # Set up the grid with patches for every NUTS region
        AC = AgentCreator(RegionAgent, {"model": self})
        agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(agents)

        # Set up agents
        # for agent in agents:
        #     if random.random() < self.density:
        #         if random.random() < self.minority_pc:
        #             agent.atype = 1
        #         else:
        #             agent.atype = 0
        #         
        for agent in agents:
            self.schedule.add(agent)

    def step(self):
        """Run one step of the model.

        If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        # self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
