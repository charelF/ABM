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
                 vision):

        # set up arguments
        self.basic_trade_reward = basic_trade_reward
        self.member_trade_reward = member_trade_reward
        self.union_payoff = union_payoff
        self.union_payoff_sensitivity = union_payoff_sensitivity
        self.neighbor_influence = neighbor_influence
        self.union_payoff_history = []
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
        # '''
        # countries_with_neighbors = []
        # for country in self.countries:
        #     has_neighs = False
        #     for area in country.areas:
        #         neighs = self.grid.get_neighbors(area)
        #         for neigh in neighs:
        #             if neigh.country.identifier != area.country.identifier:
        #                 has_neighs = True
        #     if has_neighs:
        #         countries_with_neighbors.append(country)

        # self.countries = countries_with_neighbors
        # print(self.countries)
        # '''
        # self.agents = agents

        # print(countries)

        # datacollectdict = {""}

        # set up datacollector
        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        self.datacollector = DataCollector({"collaborator_count": "collaborator_count", "defector_count":"defector_count", "union_payoff":"union_payoff"})
        self.datacollector.collect(self)

    def count_collaborators(self):
        C = 0
        D = 0
        for agent in self.agents:
            if agent.strategy == 1:
                C+=1
            else:
                D+=1
        return C

    def compute_union_payoff(self):
        # self.union_payoff = (0.5 - self.count_collaborators()[0]/len(self.agents))
        ### ALEX
        new_pay_off = (self.union_payoff_sensitivity*(0.5-(self.collaborator_count/len(self.agents))))
        if len(self.union_payoff_history) >= 5:
            self.union_payoff_history.pop(0)
        self.union_payoff_history.append(new_pay_off)
        self.union_payoff = sum(self.union_payoff_history)/5

    # def change_strategy(self):
    #     """
    #     Given the countries, picks the worst country
    #     and changes strategy to empirical strategy 
    #     of best country e.g. best did 10 trades and
    #     1 defect -> agressiveness 1 / 11
    #     """
    #     # Decide who is doing worst/best based on wealth
    #     if self.round % 10 == 0:
    #         # Number of countries that change strategy
    #         k = 3
            
    #         worst_indices = np.argpartition([country.wealth for country in self.countries], k)[:k]
    #         best_index = np.argmax([country.wealth for country in self.countries])

    #         # Replace k worst countries
    #         for index in worst_indices:
    #             print(str(self.countries[index].identifier) +' changed from ' + str(self.countries[index].agressiveness) +' to ' + str((self.round - self.countries[best_index].trades) / self.round))
    #             self.countries[index].agressiveness = (self.round - self.countries[best_index].trades) / self.round
                
    # def tax_and_redistribute(self):

    #     treasury = 0
    #     total_wealth = 0

    #     for country in self.countries:
    #         # Take taxes
    #         if country.wealth > 0:
    #             tax = country.wealth * self.tax
    #             country.wealth -= tax
    #             treasury += tax 
    #             total_wealth += country.wealth
    #     print(total_wealth)
        
    #     # Count countries that traded and divide among 50% of them
    #     trading_countries = [country for country in self.countries if country.traded]
    #     entitled_countries = len(trading_countries)//2
    #     worst_indices = np.argpartition([country.wealth for country in trading_countries], entitled_countries)[:entitled_countries]
    #     for index in worst_indices:
    #         trading_countries[index].wealth += treasury / entitled_countries


    def step(self):
        self.round += 1
        self.schedule.step()
        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        self.compute_union_payoff()
        # if self.tax != 0:
        #     self.tax_and_redistribute()

        # self.change_strategy()

        # self.traded = 0
        # self.average_agressiveness = np.mean([country.agressiveness for country in self.countries])
        # for i, country in enumerate(self.countries):
        #     country.interacted = False
        #     if country.traded == True:
        #         country.trades += 1

        self.datacollector.collect(self)

        if self.collaborator_count == 0 or self.defector_count == 0:
            self.running = False