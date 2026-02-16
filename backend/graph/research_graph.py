from langgraph.graph import StateGraph, START, END
from agents import section1, section2, section3, section4, section5, editor

def build():
    # 1. Initialize with your state dict or Pydantic model
    workflow = StateGraph(dict)

    # 2. Add all nodes
    workflow.add_node("section1", section1.run)
    workflow.add_node("section2", section2.run)
    workflow.add_node("section3", section3.run)
    workflow.add_node("section4", section4.run)
    workflow.add_node("section5", section5.run)
    workflow.add_node("editor", editor.run)

    # --- THE FIX ---
    # Use the START constant to branch into parallel nodes. 
    # Do NOT pass a list to set_entry_point.
    workflow.add_edge(START, "section1")
    workflow.add_edge(START, "section2")
    workflow.add_edge(START, "section3")
    workflow.add_edge(START, "section4")
    
    # 3. Fan-in: Wait for parallel sections to finish before moving to section 5
    workflow.add_edge(["section1", "section2", "section3", "section4"], "section5")
    
    # 4. Final sequence
    workflow.add_edge("section5", "editor")
    workflow.add_edge("editor", END)

    return workflow.compile()
