from typing import Dict
import dash_mantine_components as dmc
from filters.session_id import SessionIdFilter
# format {graph_group: {graph_name: graph_component}}


def make_components(graphs: Dict[str, Dict[str, "dmc.Component"]]):
    """
    Generate a list of Mantine components for the layout of the page
    :param graphs: list of graphs to display on the page
    :return: list of Mantine components
    """

    nav_children = [
        SessionIdFilter(),
        dmc.NavLink(label="Overview", href="#", sx={"color": "var(--white)"}, mb="md", className="rounded"),
    ]

    for graph_group, graph_group_dict in graphs.items():
        nav_children.append(dmc.Text(graph_group))
        for graph_name in graph_group_dict.keys():
            nav_children.append(
                dmc.NavLink(
                    label=graph_name, href=f"#{graph_name.replace(' ', '-').lower()}", className="rounded", sx={"color": "var(--grey)"}
                )
            )

    # navbar of all graphs on the left taking up 1/3 of the screen and list of graphs on the right taking up 2/3 of the screen
    return dmc.Grid(
        [
            dmc.Col(
                [
                    dmc.Navbar(p="md", width={"base": 300}, children=nav_children),
                ],
                xs=12,
                md=3,
            ),
            dmc.Col(
                [
                    dmc.Group(
                        [
                            graph
                            for graph_group in graphs.values()
                            for graph in graph_group.values()
                        ],
                    )
                ],
                xs=12,
                md=9,
            ),
        ],
        gutter="xl",
    )
