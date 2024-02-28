from dash import callback
import dash
from dash.dependencies import Input, Output


@callback(Output("title", "children"), Input("url", "pathname"))
def update_title(pathname) -> str:
    """Updates the title of the page based on the current pathname.

    Args:
        pathname (str): The current pathname of the page.

    Returns:
        str: The title of the page.
    """
    if pathname == "/":
        return "Home"
    else:
        for page in dash.page_registry.values():
            if page["path"] == pathname:
                return page["name"]
    return "404 - Not Found"
