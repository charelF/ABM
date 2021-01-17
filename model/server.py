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
    # "basic_trade_reward" : UserSettableParameter(
    #     "slider", "Basic trading reward", 0, 0, 0.02, 0.001
    # ),
    # "member_trade_reward" : UserSettableParameter(
    #     "slider", "Member trading reward", 0, 0, 0.02, 0.001
    # ),
    "international_trade" : UserSettableParameter(
        "checkbox", "International_Trade", value=True
    ),
    "max_eff": UserSettableParameter(
        "slider", "Maximum efficiency", 0, 0, 0.1, 0.001
    ),
    "eutax": UserSettableParameter(
        "slider", "Tax of EU per round", 0, 0, 1, 0.01
    ),
    "neighbor_influence": UserSettableParameter(
        "slider", "neighbor_influence", 0, 0, 0.2, 0.01
    ),
    "tax_influence": UserSettableParameter(
        "slider", "tax_influence", 0, 0, 0.2, 0.01
    ),
    "member_trade_multiplier": UserSettableParameter(
    "slider", "member_trade_multiplier", 1, 0, 20, 0.5
    ),
    "randomness": UserSettableParameter(
    "slider", "randomness", 0, 0, 1, 0.001231441
    ),
    "eu_strategy": UserSettableParameter(
    'choice', 'Eu strategy', value='default',
        choices=['default', 'capitalist', 'socialist', 'hardship'])
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
