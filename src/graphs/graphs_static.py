
from src.graphs.static.simple import GraphsSimple
from src.graphs.static.spectral import GraphsSpectral
from src.graphs.static.time import GraphsTime
from src.graphs.static.model import GraphsModel

PLOT_SIZE_SINGLE = (8, 4)
PLOT_SIZE_DOUBLE = (8, 6)
PLOT_SIZE_RECT = (8, 8)


class Graphs:
    """ Collective class for methods that plot static graphs.
    """
    simple: GraphsSimple = GraphsSimple()
    spectral: GraphsSpectral = GraphsSpectral()
    time: GraphsTime = GraphsTime()
    models: GraphsModel = GraphsModel()
