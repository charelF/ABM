from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import SchellingModel
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
        return "Average agression " + str("%.2f" % model.average_agressiveness)

model_params = {
    "tax": UserSettableParameter(
        "slider", "Tax rate", 0.2, 0.00, 1.0, 0.05
    ),
    "trade_reward" : UserSettableParameter(
        "slider", "Trading reward", 4, 0, 10, 0.5
    ),
    "deficit_reward" : UserSettableParameter(
        "slider", "War reward", 4, 0, 10, 0.5
    ),
}


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = dict()
    if hasattr(agent, 'country'):
        portrayal["color"] = rgb2hex(int(agent.country.agressiveness * 255), 0, 0)
    else:
        portrayal["color"] = 'white'
    return portrayal

happy_element = HappyElement()
map_element = MapModule(schelling_draw, [52, 12], 3, 500, 700)
happy_chart = ChartModule([{"Label": 'average', "Color": "Black"}])
server = ModularServer(
    SchellingModel, [map_element, happy_element, happy_chart], "Warring nations", model_params
)
server.launch()
