from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *
import numpy as np
import pprint

class RegionModel(Model):
    def __init__(self, basic_trade_reward, member_trade_reward,
                vision, max_eff, eutax, weight, neighbor_influence, tax_influence):
        # set up arguments
        self.basic_trade_reward = basic_trade_reward
        self.member_trade_reward = member_trade_reward
        self.vision = vision
        self.treasury = 0
        self.eutax = eutax
        self.weight = weight
        self.total_hardship = 0
        self.neighbor_influence = neighbor_influence
        self.tax_influence = tax_influence
        self.total_wealth = 0
        self.member_wealth = 0
        self.other_wealth = 0
        self.total_eff = 0
        self.member_eff = 0
        self.other_eff = 0

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
            cooperativeness = random.uniform(-1, 1)#max(min(np.random.normal(0, 1), 1), -1)
            agent.cooperativeness = cooperativeness
            agent.strategy = 1 if cooperativeness > 0 else 2
            agent.wealth = 1
            agent.efficiency = max(random.random() * max_eff, 0.0000001)
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
        self.datacollector = DataCollector(
            {"collaborator_count": "collaborator_count",
            "defector_count":"defector_count",
            "av_coop":"av_coop",
            "other_wealth":"other_wealth",
            "total_wealth":"total_wealth",
            "member_wealth":"member_wealth",
            "other_eff":"other_eff",
            "total_eff":"total_eff",
            "member_eff":"member_eff"})

        self.datacollector.collect(self)

    def count_collaborators(self):
        C = 0
        for agent in self.agents:
            if agent.strategy == 1:
                C+=1
        return C

    def compute_wealth(self):
        self.member_wealth = 0
        self.other_wealth = 0
        self.total_wealth = 0
        for agent in self.agents:
            if agent.strategy == 1:
                self.member_wealth += agent.wealth
            else:
                self.other_wealth += agent.wealth
        self.total_wealth = self.member_wealth + self.other_wealth

        self.member_wealth = self.member_wealth / max(self.collaborator_count, 1)
        self.other_wealth = self.other_wealth / max(self.defector_count, 1)
        self.total_wealth = self.total_wealth / 320

    def compute_eff(self):
        self.member_eff = 0
        self.other_eff = 0
        self.total_eff = 0
        for agent in self.agents:
            if agent.strategy == 1:
                self.member_eff += agent.efficiency
            else:
                self.other_eff += agent.efficiency
        self.total_eff = self.member_eff + self.other_eff

        self.member_eff = self.member_eff / max(self.collaborator_count, 1)
        self.other_eff = self.other_eff / max(self.defector_count, 1)
        self.total_eff = self.total_eff / 320


    def collect_taxes(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        for agent in members:
            tax = agent.wealth * self.eutax
            agent.tax_payed = tax
            agent.wealth -= tax
            self.treasury += tax

    def distribute_benefits(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members:
            self.running = False
            return
        benefit = self.treasury / len(members)
        for agent in members:
            agent.wealth += benefit
            if benefit + agent.eu_bonus > agent.tax_payed:
                agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
            elif benefit  + agent.eu_bonus < agent.tax_payed:
                agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
                
        self.treasury = 0

    def compute_virtual_benefits(self):
        others = [agent for agent in self.agents if agent.strategy == 2]
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members or not others:
            self.running = False
            return
        for agent in others:
            virtual_tax_payed = agent.wealth * self.eutax
            virtual_treasury = self.treasury + virtual_tax_payed
            virtual_benefit = virtual_treasury / (len(members) + 1)
            if virtual_benefit + agent.fictional_bonus > virtual_tax_payed:
                agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
            elif virtual_benefit + agent.fictional_bonus < virtual_tax_payed:
                agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)

            


    # def distribute_taxes(self):

        # # Hardship
        # self.total_hardship = 0.000000001
        # traded_agents = [agent for agent in self.agents if agent.strategy == 1]
        # for agent in traded_agents:
        #     self.total_hardship += 1 - agent.cooperativeness
        #     # hardship is opposite to cooperativeness
        #     # lots of cooperativeness --> total hardship small
        
        # for agent in traded_agents:
        #     distributed_wealth =  (1 - agent.cooperativeness)/ self.total_hardship * self.treasury
        #     agent.wealth += distributed_wealth
        #     self.treasury -= distributed_wealth
        #     if distributed_wealth + agent.eu_bonus < agent.tax:
        #         agent.cooperativeness -= self.tax_influence
        #     else:
        #         agent.cooperativeness += self.tax_influence

        #     if agent.cooperativeness > 1:
        #         agent.cooperativeness = 1
        #     elif agent.cooperativeness < -1:
        #         agent.cooperativeness = -1
        # traded_agents = [agent for agent in self.agents if agent.strategy == 1]
        # for agent in traded_agents:
        #     # distribution = self.treasury / self.count_collaborators()
        #     # distribution = agent.tax 
        #     # agent.wealth += distribution
        #     # if distribution + agent.eu_bonus < agent.tax:
        #     # if distribution + agent.eu_bonus < agent.tax:
        #     if agent.eu_bonus < 0:
        #         agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
        #     elif agent.eu_bonus > 0:
        #         agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)

        # self.treasury = 0


    # def calculate_benefit(self):
    #     traded_agents = [agent for agent in self.agents if agent.strategy == 2]
    #     for agent in traded_agents:
    #         # distribution = (self.treasury + agent.wealth * self.eutax) / (self.count_collaborators() + 1)
    #         # distribution = agent.wealth * self.eutax
    #         # agent.wealth += distribution
    #         # if distribution + agent.fictional_bonus < distribution:
    #         if agent.fictional_bonus < 0:
    #             agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
    #         elif agent.fictional_bonus > 0:
    #             agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)


    #     # for agent in self.agents:
    #     #     #print(agent.NUTS_ID, agent.wealth)
    #     #     if agent.strategy == 2:
    #     #         tax_payment = agent.wealth * self.eutax
    #     #         fictional_total_hardship = self.total_hardship + (1 - agent.cooperativeness)
    #     #         try:
    #     #             tax_distribution = (1 - agent.cooperativeness)/ fictional_total_hardship * self.treasury
    #     #         except:
    #     #             tax_distribution = 0

    #     #         if tax_payment < tax_distribution + agent.fictional_bonus:
    #     #             agent.cooperativeness += self.tax_influence
    #     #         else:
    #     #             agent.cooperativeness -= self.tax_influence

    #     #         if agent.cooperativeness > 1:
    #     #             agent.cooperativeness = 1
    #     #         elif agent.cooperativeness < -1:
    #     #             agent.cooperativeness = -1                                
    #             #print(agent.NUTS_ID , tax_payment, agent.fictional_bonus, tax_distribution)


    def step(self):
        for agent in self.agents: agent.has_traded = False
        self.round += 1
        self.schedule.step()
        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        self.compute_wealth()
        self.compute_eff()
        #self.compute_union_payoff()
        self.av_coop = sum([agent.cooperativeness for agent in self.agents])/len(self.agents)
        
    
        # stop model if only one type of agents left
        # self.calculate_benefit()
        # self.distribute_taxes()

        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        if self.collaborator_count == 0 or self.defector_count == 0:
            self.running = False

        self.collect_taxes()

        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        if self.collaborator_count == 0 or self.defector_count == 0:
            self.running = False


        self.compute_virtual_benefits()


        self.collaborator_count = self.count_collaborators()
        self.defector_count = len(self.agents) - self.collaborator_count
        if self.collaborator_count == 0 or self.defector_count == 0:
            self.running = False



        self.distribute_benefits()




        
        #if self.collaborator_count == 0 or self.defector_count == 0:
            #self.running = False
        self.datacollector.collect(self)
