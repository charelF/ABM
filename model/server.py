from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import SchellingModel
from mesa_geo.visualization.MapModule import MapModule
import random


class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)


# model_params = {
#     "density": UserSettableParameter("slider", "Agent density", 0.6, 0.1, 1.0, 0.1),
#     "minority_pc": UserSettableParameter(
#         "slider", "Fraction minority", 0.2, 0.00, 1.0, 0.05
#     ),
# }

colours = {}


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = dict()

    r = lambda: random.randint(0, 255)
    color = "#%02X%02X%02X" % (r(), r(), r())

    if agent.atype not in colours:
        portrayal["color"] = color
        colours[agent.atype] = color
    else:
        portrayal["color"] = colours[agent.atype]

    return portrayal


happy_element = HappyElement()
map_element = MapModule(schelling_draw, [52, 12], 4, 500, 500)

happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])
server = ModularServer(
    SchellingModel, [map_element, happy_element, happy_chart], "Schelling"
)
server.launch()
