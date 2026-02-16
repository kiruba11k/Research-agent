from langgraph.graph import StateGraph, END
from agents import section1, section2, section3, section4, section5, editor

def build():
    workflow = StateGraph(dict)

    # 1. Parallel Research Nodes
    workflow.add_node("section1", section1.run)
    workflow.add_node("section2", section2.run)
    workflow.add_node("section3", section3.run)
    workflow.add_node("section4", section4.run)
    
    # 2. Sequential Synthesis Nodes
    workflow.add_node("section5", section5.run)
    workflow.add_node("editor", editor.run)

    # 3. Parallel Dispatch
    workflow.set_entry_point(["section1", "section2", "section3", "section4"])
    
    # 4. Synchronization Barrier
    workflow.add_edge(["section1", "section2", "section3", "section4"], "section5")
    workflow.add_edge("section5", "editor")
    workflow.add_edge("editor", END)

    return workflow.compile()
