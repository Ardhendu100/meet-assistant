from langgraph.graph import StateGraph,START, END
# Define dummy nodes

def start_node(data):
    print("Start node")
    return {"step": "start", "data": data}

def do_something_node(data):
    print("Doing something...")
    return {"step": "do_something", "data": data}

def finish_node(data):
    print("Finish node")
    return {"step": "finish", "data": data}

# Build the graph
graph = StateGraph(dict)
graph.add_node("start", start_node)
graph.add_node("do_something", do_something_node)
graph.add_node("finish", finish_node)

# Connect nodes
graph.add_edge(START, "do_something")
graph.add_edge("do_something", "finish")
graph.add_edge("finish", END)

workflow = graph.compile()
# Run the workflow
if __name__ == "__main__":
    result = workflow.invoke({"input": "Hello LangGraph!"})
    print("Workflow result:", result)
