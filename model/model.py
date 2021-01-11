from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *
import numpy as np

class SchellingModel(Model):
    """Model class for the Schelling segregation model."""

    def __init__(self, interaction_chance, alliance_reward, war_reward, alliance_war_reward):

        self.countries = {}

        # Paramas
        self.interaction_chance = interaction_chance
        self.alliance_reward = alliance_reward
        self.war_reward = war_reward
        self.alliance_war_reward = alliance_war_reward

        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()

        self.test = 0
        self.datacollector = DataCollector({"test": "test"})

        self.running = True
        # Set up the grid with patches for every NUTS region
        AC = AgentCreator(SchellingAgent, {"model": self})
        agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(agents)
        ###
        for agent in agents:
            self.schedule.add(agent)
            agent.wealth = agent.SHAPE_AREA
            agent.country = agent.NUTS_ID[0:2]
            color = "#" + str(hex(np.random.randint(0, 0xFFFFFF))).upper()[2:2+6]
            if agent.country not in self.countries.keys():
                self.countries[agent.country] = {
                    "aggressiveness": random.random(),
                    "constituing_regions": 1,
                    "color": color,
                    "wealth": 1,
                    "rep": 0.5,
                }

            else:
                self.countries[agent.country]["constituing_regions"] += 1
                self.countries[agent.country]["wealth"] += 1
        self.country_sizes = np.zeros(len(self.countries))
        self.average = int(np.mean(self.country_sizes))

    def step(self):
        """Run one step of the model.

        If All agents are happy, halt the model.
        """
        self.schedule.step()
        '''
        for k in self.countries:
            self.countries[k]["wealth"] += self.countries[k]["constituing_regions"] * 0.2
        '''
        self.average = int(np.mean(self.country_sizes))
        for i, key in enumerate(self.countries):
            #print(self.countries[key])
            self.country_sizes[i] = self.countries[key]['constituing_regions']