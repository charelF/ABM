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
                vision, max_eff, eu_tax, weight, consumption, volatile):
        # set up arguments
        self.basic_trade_reward = basic_trade_reward
        self.member_trade_reward = member_trade_reward
        self.vision = vision
        self.treasury = 0
        self.eu_tax = eu_tax
        self.weight = weight
        self.total_hardship = 0
        self.consumption = consumption
        self.volatile = volatile

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
            agent.wealth = 1
            agent.efficiency = 1 + (max_eff - 1) * random.random()
            agent.tax = 0
            agent.eu_bonus = 0
            agent.fictional_bonus = 0
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
        self.datacollector = DataCollector({"collaborator_count": "collaborator_count", "defector_count":"defector_count", "av_coop":"av_coop"})

        self.datacollector.collect(self)

    def count_collaborators(self):
        C = 0
        for agent in self.agents:
            agent.eu_bonus = 0
            agent.fictional_bonus = 0
            if agent.strategy == 1:
                C+=1
        return C

    def distribute_taxes(self):

        # Hardship
        self.total_hardship = 0
        traded_agents = [agent for agent in self.agents if agent.strategy == 1]
        for agent in traded_agents:
            self.total_hardship += 1 - agent.cooperativeness
        
        for agent in traded_agents:
            distributed_wealth =  (1 - agent.cooperativeness)/ self.total_hardship * self.treasury
            agent.wealth += distributed_wealth
            self.treasury -= distributed_wealth
            if distributed_wealth + agent.eu_bonus < agent.tax:
                agent.cooperativeness -= self.volatile
            else:
                agent.cooperativeness += self.volatile

            if agent.cooperativeness > 1:
                agent.cooperativeness = 1
            elif agent.cooperativeness < -1:
                agent.cooperativeness = -1

    def calculate_benefit(self):
        for agent in self.agents:
            #print(agent.NUTS_ID, agent.wealth)
            if agent.strategy == 2:
                tax_payment = agent.wealth * self.eu_tax
                fictional_total_hardship = self.total_hardship + (1 - agent.cooperativeness)
                try:
                    tax_distribution = (1 - agent.cooperativeness)/ fictional_total_hardship * self.treasury
                except:
                    tax_distribution = 0

                if tax_payment < tax_distribution + agent.fictional_bonus:
                    agent.cooperativeness += self.volatile
                else:
                    agent.cooperativeness -= self.volatile

                if agent.cooperativeness > 1:
                    agent.cooperativeness = 1
                elif agent.cooperativeness < -1:
                    agent.cooperativeness = -1                                
                #print(agent.NUTS_ID , tax_payment, agent.fictional_bonus, tax_distribution)


    def step(self):
        self.round += 1
        self.schedule.step()
        self.defector_count = len(self.agents) - self.collaborator_count
        #self.compute_union_payoff()
        self.av_coop = sum([agent.cooperativeness for agent in self.agents])/len(self.agents)
        self.datacollector.collect(self)
    
        # stop model if only one type of agents left
        self.calculate_benefit()
        self.distribute_taxes()
        self.collaborator_count = self.count_collaborators()
        #if self.collaborator_count == 0 or self.defector_count == 0:
            #self.running = False
