from dash import callback
import dash
import pandas as pd
from db.mongodb import get_db
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


@callback(Output("linpot-data", "data"), Input("session-id", "data"))
def load_data(session_id):
    db = get_db()
    collection = db["realtime_metrics"]
    # Query MongoDB for data with the given run ID
    # Case to string just in case int is passed
    mongo_data = list(
        collection.find(
            {"metadata.session_id": str(session_id), "metadata.source": "linpot"},
            {"_id": 0}
        )
    )
    # Convert MongoDB data to DataFrame
    df = pd.DataFrame(mongo_data)
    # Convert DataFrame to JSON and return
    return df.to_json(date_format="iso", orient="split")
