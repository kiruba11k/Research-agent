from langgraph.graph import StateGraph

from agents.section1 import run as section1_run
from agents.section2 import run as section2_run
from agents.section3 import run as section3_run
from agents.section4 import run as section4_run
from agents.section5 import run as section5_run
from agents.editor import run as editor_run


def build():

    g = StateGraph(dict)

    g.add_node("section1", section1_run)
    g.add_node("section2", section2_run)
    g.add_node("section3", section3_run)
    g.add_node("section4", section4_run)
    g.add_node("section5", section5_run)
    g.add_node("editor", editor_run)

    g.set_entry_point("section1")

    g.add_edge("section1", "section2")
    g.add_edge("section2", "section3")
    g.add_edge("section3", "section4")
    g.add_edge("section4", "section5")
    g.add_edge("section5", "editor")

    return g.compile()
