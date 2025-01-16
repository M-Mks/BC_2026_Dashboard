import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Load the CSV file
file_path = "dashboard\Copy_Rand_Quantitative_results.csv"  # Update with your CSV file path
df = pd.read_csv(file_path, sep=";")

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Survey Results Dashboard"

# Layout of the dashboard
app.layout = html.Div(
    style={"font-family": "Arial, sans-serif", "margin": "20px"},
    children=[
        html.H1("Survey Results Dashboard", style={"text-align": "center", "color": "#2c3e50"}),
        html.P(
            "Explore the survey results through interactive visualizations.",
            style={"text-align": "center", "color": "#7f8c8d"}
        ),
        # Dropdown to select a question
        html.Div(
            [
                html.Label("Select a Question:", style={"font-weight": "bold"}),
                dcc.Dropdown(
                    id="question-dropdown",
                    options=[{"label": col, "value": col} for col in df.columns],
                    value=df.columns[0],  # Default selection
                    clearable=False,
                    style={"width": "50%"}
                ),
            ],
            style={"margin-bottom": "20px"}
        ),
        # Graph container
        html.Div(
            [
                dcc.Graph(id="histogram"),
                dcc.Graph(id="pie-chart"),
            ]
        )
    ]
)
# Define the graph type for each question
graph_types = {
    "Question1": "histogram",
    "Question2": "pie",
    "Question3": "line",
    # Add more questions and graph types as needed
}

# Callback to update the graphs based on the selected question
@app.callback(
    [Output("histogram", "figure"), Output("pie-chart", "figure")],
    [Input("question-dropdown", "value")]
)
def update_graphs(selected_question):
    # Histogram
    hist_figure = px.histogram(
        df,
        x=selected_question,
        nbins=10,
        title=f"Histogram of {selected_question}",
        labels={selected_question: "Response Values"},
        color_discrete_sequence=["#3498db"],
    )
    hist_figure.update_layout(
        title={"x": 0.5},
        xaxis_title="Response Values",
        yaxis_title="Count",
        template="plotly_white"
    )

    # Pie Chart
    pie_figure = px.pie(
        df,
        names=selected_question,
        title=f"Response Distribution for {selected_question}",
        color_discrete_sequence=px.colors.sequential.Teal
    )
    pie_figure.update_layout(title={"x": 0.5}, template="plotly_white")

    return hist_figure, pie_figure


#Run the app
if __name__ == "__main__":
     app.run_server(debug=True)

