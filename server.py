from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import RegionModel
from mesa_geo.visualization.MapModule import MapModule
import numpy as np

model_params = {
    "international_trade" : UserSettableParameter(
        "checkbox", "International_Trade", value=True
    ),
    "efficiency_stdev": UserSettableParameter(
        "slider", "STDev of efficiency (mean = 1)", 0.1, 0, 2, 0.01
    ),
    "eu_tax": UserSettableParameter(
        "slider", "EU Tax (percentage of wealth)", 0.1, 0, 1, 0.001
    ),
    "neighbor_influence": UserSettableParameter(
        "slider", "Neighbor Influence (step size)", 0, 0., 0.2, 0.01
    ),
    "tax_influence": UserSettableParameter(
        "slider", "Tax/Benefit influence (step size)", 0.1, 0, 0.2, 0.01
    ),
    "member_trade_multiplier": UserSettableParameter(
    "slider", "Member trade advantage (multiplier of wealth)", 1.1, 0.5, 3, 0.01
    ),
    "benefit_distribution": UserSettableParameter(
    "slider", "Benefit distribution (multiplier of tax payed)", 1, 0.8, 1.2, 0.001
    ),
}

def schelling_draw(agent):
    portrayal = dict()
    if agent.strategy == 1:
        portrayal["color"] = "RoyalBlue"
    else:
        portrayal["color"] = "Tomato"
    return portrayal

map_element = MapModule(schelling_draw, [57, 12], 3, 400, 800)

type_chart = ChartModule([{"Label": 'other_count', "Color": "Tomato"},
                          {"Label": 'member_count', "Color": "RoyalBlue"}], 200, 500)

payoff_chart = ChartModule([{"Label": 'average_cooperativeness', "Color": "Gold"}], 200, 500)

gini_chart = ChartModule([{"Label": 'gini_coefficient', "Color": "Green"}], 200, 500)

wealth_chart = ChartModule([
    {"Label": 'other_wealth', "Color": "Tomato"},
    {"Label": 'total_wealth', "Color": "Gold"},
    {"Label": 'member_wealth', "Color": "RoyalBlue"},
], 200, 500)

eff_chart = ChartModule([
    {"Label": 'other_eff', "Color": "Tomato"},
    {"Label": 'total_eff', "Color": "Gold"},
    {"Label": 'member_eff', "Color": "RoyalBlue"},
], 200, 500)

server = ModularServer(
    RegionModel, [map_element, type_chart, gini_chart, wealth_chart,eff_chart, payoff_chart], "ABM", model_params
)

server.launch()
