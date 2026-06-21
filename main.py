import dash
from dash import dcc, html, Input, Output
from compounds import COMPOUNDS
from graph_layout import list_families
from graph_layout import build_figure

app = dash.Dash(__name__)

# Extract all family names for the filter
ALL_FAMILIES = list_families()

app.layout = html.Div([
    html.H1("Chemical Stammbaum Harm Reduction Portal", style={'textAlign': 'center'}),
    
    # Global Filter
    html.Div([
        html.Label("Filter by Family:"),
        dcc.Checklist(
            id='family-filter',
            options=[{'label': f, 'value': f} for f in ALL_FAMILIES],
            value=ALL_FAMILIES, # Default to showing all
            inline=True
        )
    ], style={'padding': '20px', 'backgroundColor': '#1c1c1f', 'color': 'white'}),

    # Main Visualization
    dcc.Graph(id='stammbaum-graph', style={'height': '80vh'}),
    
    # Metadata Sidebar / Footer Area
    html.Div(id='node-details', style={'padding': '20px', 'marginTop': '20px', 'borderTop': '1px solid #444'})
])

@app.callback(
    Output('stammbaum-graph', 'figure'),
    Input('family-filter', 'value')
)
def update_graph(selected_families):
    return build_figure(visible_families=selected_families)

# (Line 39, no indentation)
if __name__ == '__main__': # Line 40
    app.run_server(host='0.0.0.0', port=10000) # Line 41 (indented with 4 spaces)