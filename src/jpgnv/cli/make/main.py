import altair as alt
import matplotlib.pyplot as plt
from cyclopts import App
from loguru import logger
from utils4plans.logconfig import logset

from plyze.examples.casedata import ex
from plyze.qoi.data.outputs import get_surface_qois
from plyze.plots.altair_helpers import AltairRenderers
from plyze.plots.theme import default_theme

app = App()


def keep():
    default_theme()
    logger.debug("")
    plt.plot()


### ----- DATA --------
@app.command()
def get():
    res = get_surface_qois(*ex)


### ------- END COMMANDS ---------


def main():
    AltairRenderers.set_renderer()
    alt.theme.enable("default_theme")
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
