from dataclasses import dataclass
import pandas as pd
import plotly.express as px


@dataclass
class MostSuccessfulPlotDetails:
    query: str
    x: str
    y: str
    labels: dict
    title: str
    text: str


def get_most_successful_graph(selected, engine, definition):
    d = definition[selected]

    df = pd.read_sql_query(d.query, engine)

    fig = px.bar(df,
                 x=d.x,
                 y=d.y,
                 labels=d.labels,
                 title=d.title,
                 text=d.text)  # Display text when hovering

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside',
                      hovertemplate='%{x}: %{y:,.0f} $<extra></extra>')
    fig.update_layout(
        xaxis_tickangle=-90,
        height=700,
        width=1250,
        margin=dict(l=50, r=50, t=100, b=100),
    )
    fig.show()


# interactive_output = widgets.interactive(update_graph,
#                                          selected=dropdown,
#                                          engine=fixed(engine),
#                                          definition=fixed(setting))
# display(interactive_output)
