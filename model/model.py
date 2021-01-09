from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *


class RegionModel(Model):

    def __init__(self, density, minority_pc):

        self.countries = {}

        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()

        self.test = 0
        self.datacollector = DataCollector({"test": "test"})

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
            agent.wealth = agent.SHAPE_AREA
            agent.country = agent.NUTS_ID[0:2]
            if agent.country not in self.countries.keys():
                self.countries[agent.country] = random.random()
            agent.aggressiveness = self.countries[agent.country]


    def step(self):
        print("i run")
        """Run one step of the model.

        If All agents are happy, halt the model.
        """
        self.test = 0  # Reset counter of happy agents
        self.schedule.step()
        # self.datacollector.collect(self)

        # if self.test == self.schedule.get_agent_count():
        #     self.running = False
