from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import RegionModel
from mesa_geo.visualization.MapModule import MapModule
from utilities import get_color
import numpy as np
from colormap import rgb2hex

# class HappyElement(TextElement):
#     """
#     Display a text count of how many happy agents there are.
#     """

#     def __init__(self):
#         pass

#     def render(self, model):
#         return "temp" #"Average agression " + str("%.2f" % model.average_agressiveness)


model_params = {
    "basic_trade_reward" : UserSettableParameter(
        "slider", "Basic trading reward", 0, 0, 1, 0.001
    ),
    "member_trade_reward" : UserSettableParameter(
        "slider", "Member trading reward", 0, 0, 1, 0.001
    ),
    "vision" : UserSettableParameter(
        "slider", "Vision", 1, 0, 1, 0.1
    ),
    "max_eff": UserSettableParameter(
        "slider", "Maximum efficiency", 0, 0, 2, 0.001
    ),
    "eutax": UserSettableParameter(
        "slider", "Tax of EU per round", 0, 0, 1, 0.001
    ),
    "weight": UserSettableParameter(
        "slider", "Decision stochasticity", 0, 0, 1, 0.05
    ),
    "neighbor_influence": UserSettableParameter(
        "slider", "neighbor_influence", 0, 0, 0.2, 0.001
    ),
    "tax_influence": UserSettableParameter(
        "slider", "tax_influence", 0, 0, 0.2, 0.001
    ),
}


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = dict()
    # if hasattr(agent, 'country'):
    #     portrayal["color"] = rgb2hex(int(agent.country.agressiveness * 255), 0, 0)
    # else:
    #     portrayal["color"] = 'white'
    if agent.strategy == 1:
        portrayal["color"] = "Blue"
    else:
        portrayal["color"] = "Red"
    return portrayal

# happy_element = HappyElement()
map_element = MapModule(schelling_draw, [57, 12], 3, 400, 800)
type_chart = ChartModule([{"Label": 'defector_count', "Color": "Red"},
                          {"Label": 'collaborator_count', "Color": "Blue"}], 200, 500)
payoff_chart = ChartModule([{"Label": 'av_coop', "Color": "Green"}], 200, 500)
wealth_chart = ChartModule([
    {"Label": 'other_wealth', "Color": "Red"},
    {"Label": 'total_wealth', "Color": "Yellow"},
    {"Label": 'member_wealth', "Color": "Blue"},
], 200, 500)
server = ModularServer(
    RegionModel, [map_element, type_chart, wealth_chart, payoff_chart], "Warring nations", model_params
)
server.launch()
