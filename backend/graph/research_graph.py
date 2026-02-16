from langgraph.graph import StateGraph
from agents.section1 import run as section1_run
from agents.section2 import run as section2_run
from agents.section3 import run as section3_run
from agents.section4 import run as section4_run
from agents.section5 import run as section5_run
from agents.editor import run as editor_run

def build():
    g = StateGraph(dict)

    g.add_node("s1", section1.run)
    g.add_node("s2", section2.run)
    g.add_node("s3", section3.run)
    g.add_node("s4", section4.run)
    g.add_node("s5", section5.run)
    g.add_node("editor", editor.run)

    g.set_entry_point("s1")
    g.add_parallel_edges("s1", ["s2", "s3", "s4"])
    g.add_edge("s2", "s5")
    g.add_edge("s3", "s5")
    g.add_edge("s4", "s5")
    g.add_edge("s5", "editor")

    return g.compile()
