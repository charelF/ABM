from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import RegionModel
from mesa_geo.visualization.MapModule import MapModule
from utilities import get_color
import numpy as np
from colormap import rgb2hex

class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "temp" #"Average agression " + str("%.2f" % model.average_agressiveness)

model_params = {
    "union_payoff": UserSettableParameter(
        "slider", "Union Payoff", 0, -1.0, 1.0, 0.05
    ),
    "basic_trade_reward" : UserSettableParameter(
        "slider", "Basic trading reward", 4, 0, 10, 0.5
    ),
    "member_trade_reward" : UserSettableParameter(
        "slider", "Member trading reward", 3, 0, 10, 0.5
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

happy_element = HappyElement()
map_element = MapModule(schelling_draw, [52, 12], 3, 500, 700)
happy_chart = ChartModule([{"Label": 'average', "Color": "Black"}])
server = ModularServer(
    RegionModel, [map_element, happy_element, happy_chart], "Warring nations", model_params
)
server.launch()
