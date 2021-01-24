from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *
import numpy as np

class RegionModel(Model):
    def __init__(self, international_trade, efficiency_stdev, eu_tax, neighbor_influence,
                tax_influence, member_trade_multiplier, benefit_distribution):

        self.international_trade = international_trade
        self.efficiency_stdev = efficiency_stdev
        self.eu_tax = eu_tax
        self.neighbor_influence = neighbor_influence
        self.tax_influence = tax_influence
        self.member_trade_multiplier = member_trade_multiplier
        # self.randomness = randomness
        self.benefit_distribution = benefit_distribution

        # initialise other attributes
        self.member_count = 0
        self.other_count = 0
        self.treasury = 0
        self.total_wealth = 0
        self.member_wealth = 0
        self.other_wealth = 0
        self.total_eff = 0
        self.member_eff = 0
        self.other_eff = 0
        self.round = 0
        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()
        self.running = True
        self.gini_coefficient = 0
        self.average_cooperativeness = 0
        self.stdev_agent_cooperativeness = 0

        # set up grid
        AC = AgentCreator(RegionAgent, {"model": self})
        self.agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(self.agents)

        # set up agents
        for agent in self.agents:
            self.schedule.add(agent)
            cooperativeness = random.uniform(-1, 1)
            agent.cooperativeness = cooperativeness
            agent.strategy = 1 if cooperativeness > 0 else 2
            agent.wealth = random.gauss(mu=10, sigma=2)
            agent.efficiency = abs(random.gauss(mu=1.5, sigma=self.efficiency_stdev))
            agent.tax = 0
            agent.trade_bonus = 0
        
        # set up datacollector
        self.datacollector = DataCollector({
            "member_count": "member_count",
            "other_count":"other_count",
            "average_cooperativeness":"average_cooperativeness",
            "other_wealth":"other_wealth",
            "total_wealth":"total_wealth",
            "member_wealth":"member_wealth",
            "other_eff":"other_eff",
            "total_eff":"total_eff",
            "member_eff":"member_eff",
            "gini_coefficient":"gini_coefficient",
            "stdev_agent_cooperativeness":"stdev_agent_cooperativeness",
        }
        ,{"agent_cooperativeness": lambda a: a.cooperativeness})
        self.compute_statistics()
        self.datacollector.collect(self)



    def compute_statistics(self):
        # only used for datacollector

        self.member_count = 0
        self.other_count = 0

        self.member_wealth = 0
        self.other_wealth = 0
        self.total_wealth = 0

        self.member_eff = 0
        self.other_eff = 0
        self.total_eff = 0

        total_cooperativeness = 0
        list_cooperativeness = []

        self.mean_agent_cooperativeness = 0
        self.stdev_agent_cooperativeness = 0

        wealths = np.zeros((320))

        for i, agent in enumerate(self.agents):
            # wealths[i] = agent.wealth
            total_cooperativeness += agent.cooperativeness
            list_cooperativeness.append(agent.cooperativeness)

            if agent.strategy == 1:
                wealths[i] = agent.wealth
                self.member_wealth += agent.wealth
                self.member_eff += agent.efficiency
                self.member_count += 1
            else:
                self.other_wealth += agent.wealth
                self.other_eff += agent.efficiency
                self.other_count += 1

        self.average_cooperativeness = total_cooperativeness / 320

        self.total_wealth = self.member_wealth + self.other_wealth
        self.member_wealth = self.member_wealth / max(self.member_count, 1)
        self.other_wealth = self.other_wealth / max(self.other_count, 1)
        self.total_wealth = self.total_wealth / 320

        self.total_eff = self.member_eff + self.other_eff
        self.member_eff = self.member_eff / max(self.member_count, 1)
        self.other_eff = self.other_eff / max(self.other_count, 1)
        self.total_eff = self.total_eff / 320

        self.gini_coefficient = 0
        total = 0
        for wealth_i in wealths:
            for wealth_j in wealths:
                total += abs(wealth_i - wealth_j)
        
        # self.gini_coefficient = total / (320**2 * np.mean(wealths))
        self.gini_coefficient = total / (self.member_count**2 * np.mean(wealths))

        self.stdev_agent_cooperativeness = float(np.std(list_cooperativeness))



    def collect_taxes(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members:
            self.running = False
            return

        for agent in members:
            tax = agent.wealth * self.eu_tax
            agent.tax_payed = tax
            agent.wealth -= tax
            self.treasury += tax



    def distribute_benefits(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members:
            self.running = False
            return

        benefits_total = sum([self.benefit_distribution * agent.tax_payed for agent in members])
        difference = self.treasury - benefits_total
        difference_per_capita = difference / len(members)

        for agent in members:
            agent_benefit = (self.benefit_distribution * agent.tax_payed) + difference_per_capita
            agent.wealth += agent_benefit
            self.treasury -= agent_benefit

            if agent.wealth <= 1:  # to avoid negative wealth (since we take log(wealth))
                agent.wealth = 10

            if agent_benefit + agent.trade_bonus > agent.tax_payed:
                agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
            elif agent_benefit  + agent.trade_bonus < agent.tax_payed:
                agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)

        self.treasury = 0



    def compute_virtual_benefits(self):
        others = [agent for agent in self.agents if agent.strategy == 2]
        members = [agent for agent in self.agents if agent.strategy == 1]

        if not members or not others:
            self.running = False
            return

        benefits_total = sum([self.benefit_distribution * agent.tax_payed for agent in members])

        for agent in others:
            virtual_tax_payed = agent.wealth * self.eu_tax
            virtual_treasury = self.treasury + virtual_tax_payed
            virtual_benefits_total = benefits_total + (self.benefit_distribution * virtual_tax_payed)
            virtual_difference = virtual_treasury - virtual_benefits_total
            virtual_difference_per_capita = virtual_difference / (len(members) + 1)
            virtual_benefit = (self.benefit_distribution * virtual_tax_payed) + virtual_difference_per_capita

            if virtual_benefit + agent.trade_bonus > virtual_tax_payed:
                agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
            elif virtual_benefit + agent.trade_bonus < virtual_tax_payed:
                agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)



    def step(self):
        for agent in self.agents: agent.has_traded = False
        self.round += 1
        self.schedule.step()  # step agents
        # self.compute_statistics()
        self.collect_taxes()
        self.compute_virtual_benefits()  # has to be executed before distribute_benefits since it uses self.treasury()
        self.distribute_benefits()
        self.compute_statistics()
        self.datacollector.collect(self)
