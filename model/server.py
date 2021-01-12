from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import RegionModel
from mesa_geo.visualization.MapModule import MapModule
import numpy as np


class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(np.random.randint(0, 10))


model_params = {
    "density": UserSettableParameter("slider", "Agent density", 0.6, 0.1, 1.0, 0.1),
    "minority_pc": UserSettableParameter(
        "slider", "Fraction minority", 0.2, 0.00, 1.0, 0.05
    ),
}


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = dict()
    portrayal["color"] = agent.model.countries[agent.country]["color"]
    return portrayal


happy_element = HappyElement()
map_element = MapModule(schelling_draw, [52, 12], 4, 500, 500)
happy_chart = ChartModule([{"Label": "avgwealth", "Color": "Green"}, {"Label": "test", "Color": "Black"}])
server = ModularServer(
    RegionModel, [map_element, happy_element, happy_chart], "Regions", model_params
)
server.launch()
