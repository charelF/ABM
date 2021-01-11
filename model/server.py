from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import SchellingModel
from mesa_geo.visualization.MapModule import MapModule
from utilities import get_color
import numpy as np

class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Average country size " + str(model.average)

model_params = {
    "interaction_chance": UserSettableParameter(
        "slider", "Interaction Chance", 0.2, 0.00, 1.0, 0.05
    ),
    "alliance_reward" : UserSettableParameter(
        "slider", "Trading reward", 4, 0, 10, 0.5
    ),
    "war_reward" : UserSettableParameter(
        "slider", "War reward", 4, 0, 10, 0.5
    ),
    "alliance_war_reward" : UserSettableParameter(
        "slider", "Winner/loser win/loss", 5, 0, 10, 0.5
    ),
}


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = dict()
    if agent.country != None:
        portrayal["color"] = agent.model.countries[agent.country]["color"]
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
