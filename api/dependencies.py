from graph import build_graph

graph_app = None


async def get_graph():
    return graph_app


async def init_graph():
    global graph_app
    graph_app = await build_graph()