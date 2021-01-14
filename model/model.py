from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *
import numpy as np
import pprint

# TODO: see if we can reimplement countries somehow, maybe the way they are
# code is commented out since countries are not implemented right now
# class Nation(dict, GeoAgent):

#     def __init__(self, NUTS_ID):
#         self.identifier = NUTS_ID
#         # self.strat = 2
#         self.areas = []
#         self.size = 1
#         self.interacted = False
#         self.traded = True
#         self.agressiveness = random.random()
#         self.color = "#" + str(hex(np.random.randint(0, 0xFFFFFF))).upper()[2:2+6]
#         self.wealth = 10
#         self.trades = 0
#         dict.__init__(self)

class RegionModel(Model):
    def __init__(self, basic_trade_reward, member_trade_reward,
                 union_payoff, union_payoff_sensitivity, neighbor_influence,
                 vision, union_payoff_history_max_length):

        # set up arguments
        self.basic_trade_reward = basic_trade_reward
        self.member_trade_reward = member_trade_reward
        self.union_payoff = union_payoff
        self.union_payoff_sensitivity = union_payoff_sensitivity
        self.neighbor_influence = neighbor_influence
        self.union_payoff_history = []
        self.union_payoff_history_max_length = union_payoff_history_max_length
        self.vision = vision

        # set up other parameters
        self.round = 0
        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()
        self.running = True

        # set up grid
        AC = AgentCreator(RegionAgent, {"model": self})
        self.agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(self.agents)
        
        # set up agents
        for agent in self.agents:
            self.schedule.add(agent)
            cooperativeness = max(min(np.random.normal(0, 1), 1), -1)
            agent.cooperativeness = cooperativeness
            agent.strategy = 1 if cooperativeness > 0 else 2
            agent.wealth = 10
            # country_id = agent.NUTS_ID[0:2]
            # if country_id not in [country.identifier for country in self.countries]:
            #     new_nation = Nation(country_id)
            #     self.countries.append(new_nation)
            #     agent.country = new_nation
            # else:
            #     for country in self.countries:
            #         if country.identifier == country_id:
            #             country.areas.append(agent)
            #             country.size += 1
            #             agent.country = country
        
        # set up datacollector
        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        self.datacollector = DataCollector({"collaborator_count": "collaborator_count", "defector_count":"defector_count", "union_payoff":"union_payoff"})
        self.datacollector.collect(self)

    def count_collaborators(self):
        C = 0
        for agent in self.agents:
            if agent.strategy == 1:
                C+=1
        return C

    def compute_union_payoff(self):
        # TODO: needs to be changed improved, such that we see actually a minority being able to takeover again
        ratio = self.collaborator_count/len(self.agents)  # is in [0, 1]
        new_pay_off = self.union_payoff_sensitivity * (0.5-ratio)

        if len(self.union_payoff_history) >= self.union_payoff_history_max_length:
            self.union_payoff_history.pop(0)
        self.union_payoff_history.append(new_pay_off)
        self.union_payoff = sum(self.union_payoff_history)/self.union_payoff_history_max_length

    def step(self):
        self.round += 1
        self.schedule.step()
        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        self.compute_union_payoff()
        self.datacollector.collect(self)

        # stop model if only one type of agents left
        if self.collaborator_count == 0 or self.defector_count == 0:
            self.running = False