from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *
import numpy as np
import pprint

class Nation(dict, GeoAgent):

    def __init__(self, NUTS_ID):
        self.identifier = NUTS_ID
        # self.strat = 2
        self.areas = []
        self.size = 1
        self.interacted = False
        self.traded = True
        self.agressiveness = random.random()
        self.color = "#" + str(hex(np.random.randint(0, 0xFFFFFF))).upper()[2:2+6]
        self.wealth = 10
        self.trades = 0
        dict.__init__(self)

class RegionModel(Model):
    """Model class for the Region segregation model."""

    def __init__(self, basic_trade_reward, member_trade_reward, union_payoff):

        self.countries = []
        self.basic_trade_reward = basic_trade_reward
        self.member_trade_reward = member_trade_reward
        # self.defect_reward = defect_reward
        # Params
        self.union_payoff = union_payoff
        self.round = 0
        # self.average_agressiveness = 0

        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()

        self.running = True
        # Set up the grid with patches for every NUTS region
        AC = AgentCreator(RegionAgent, {"model": self})
        self.agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(self.agents)
        ###
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
        '''
        countries_with_neighbors = []
        for country in self.countries:
            has_neighs = False
            for area in country.areas:
                neighs = self.grid.get_neighbors(area)
                for neigh in neighs:
                    if neigh.country.identifier != area.country.identifier:
                        has_neighs = True
            if has_neighs:
                countries_with_neighbors.append(country)

        self.countries = countries_with_neighbors
        print(self.countries)
        '''
        # self.agents = agents

        # print(countries)

        # datacollectdict = {""}

        self.datacollector = DataCollector({"test": "test"})
        self.datacollector.collect(self)

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
        """Run one step of the model.

        If All agents are happy, halt the model.
        """
        self.round += 1
        self.schedule.step()
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
        