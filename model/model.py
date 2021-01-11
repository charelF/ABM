from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *


class SchellingModel(Model):
    """Model class for the Schelling segregation model."""

    def __init__(self):

        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()
        self.min_happy = -100
        self.max_happy = 100
        self.armies = {
            "FR": [59],
            "UK": [58],
            "TR": [48],
            "IT": [47],
            "DE": [46],
            "ES": [30],
            "PL": [29],
            "NO": [19],
            "CH": [19],
            "SE": [19],
            "EL": [19],
            "CZ": [18],
            "NL": [17],
            "RO": [16],
            "DK": [13],
            "HU": [12],
            "SK": [12],
            "FI": [12],
            "PT": [12],
            "BG": [11],
            "AT": [10],
            "HR": [10],
            "BE": [10],
            "LT": [7],
            "LI": [7],
            "CY": [6],
            "IE": [5],
            "SI": [5],
            "LV": [5],
            "EE": [4],
            "LU": [4],
            "ME": [3],
            "MK": [3],
            "MT": [2],
            "IS": [1],
        }

        self.happy = 0
        self.datacollector = DataCollector({"happy": "happy"})

        self.running = True

        # Set up the grid with patches for every NUTS region
        AC = AgentCreator(SchellingAgent, {"model": self})
        agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(agents)

        # Set up agents
        for agent in agents:
            agent.atype = agent.NUTS_ID[:2]
            self.armies[agent.atype].append(id(self))
            agent.army = self.armies[agent.atype][0]
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
