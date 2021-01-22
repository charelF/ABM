from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import RegionModel
from mesa_geo.visualization.MapModule import MapModule
from utilities import get_color
import numpy as np
from colormap import rgb2hex

# class InfoElement(TextElement):
#     """
#     Display a text count of how many happy agents there are.
#     """

#     def __init__(self):
#         pass

#     def render(self, model):
#         # return "Member Efficiency: ""temp" "Average agression " + str("%.2f" % model.average_agressiveness)


model_params = {
    "international_trade" : UserSettableParameter(
        "checkbox", "International_Trade", value=True
    ),
    "efficiency_stdev": UserSettableParameter(
        "slider", "STDev of efficiency (mean = 1)", 0.1, 0, 3, 0.01
    ),
    "eu_tax": UserSettableParameter(
        "slider", "EU Tax (percentage of wealth)", 0.1, 0, 1, 0.001
    ),
    "neighbor_influence": UserSettableParameter(
        "slider", "Neighbor Influence (step size)", 0, 0, 0.2, 0.01
    ),
    "tax_influence": UserSettableParameter(
        "slider", "Tax/Benefit influence (step size)", 0.1, 0, 0.2, 0.01
    ),
    "member_trade_multiplier": UserSettableParameter(
    "slider", "Member trade advantage (multiplier of wealth)", 1.1, 0.5, 3, 0.01
    ),
    "randomness": UserSettableParameter(
    "slider", "randomness (step size)", 0, 0, 0.2, 0.01
    ),
    "benefit_distribution": UserSettableParameter(
    "slider", "Benefit distribution (multiplier of tax payed)", 1, 0.8, 1.2, 0.001
    ),
}


def schelling_draw(agent):
    # https://mesa.readthedocs.io/en/stable/_modules/visualization/modules/CanvasGridVisualization.html
    """
    Portrayal Method for canvas
    """
    portrayal = dict()
    # if hasattr(agent, 'country'):
    #     portrayal["color"] = rgb2hex(int(agent.country.agressiveness * 255), 0, 0)
    # else:
    #     portrayal["color"] = 'white'
    if agent.strategy == 1:
        portrayal["color"] = "RoyalBlue"
    else:
        portrayal["color"] = "Tomato"
    # portrayal["text"] = round(agent.cooperativeness, 2)
    # portrayal["text_color"] = "White"
    return portrayal

# happy_element = HappyElement()
map_element = MapModule(schelling_draw, [57, 12], 3, 400, 800)
type_chart = ChartModule([{"Label": 'other_count', "Color": "Tomato"},
                          {"Label": 'member_count', "Color": "RoyalBlue"}], 200, 500)
payoff_chart = ChartModule([{"Label": 'average_cooperativeness', "Color": "Gold"}], 200, 500)
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
    RegionModel, [map_element, type_chart, wealth_chart,eff_chart, payoff_chart], "Warring nations", model_params
)
server.launch()
