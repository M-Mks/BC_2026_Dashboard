import matplotlib
matplotlib.use('Agg')

from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from wordcloud import WordCloud, STOPWORDS
import io
import base64
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "Copy_Rand_Quantitative_results.csv"  # Update with your CSV file path
df = pd.read_csv(file_path, sep=";")

# Custom legend mapping for specific columns
custom_legend = {
    "Professional Group": {
        "A": "Marine (data) scientist and/or researcher",
        "B": "IT programmer/software developer",
        "C": "Business, infrastructure, or operations manager",
        "D": "Public administration",
        "E": "Other (please specify)",
    },
    "Organization Sector": {
        "A": "Academia",
        "B": "Research organisation",
        "C": "Data and service providers",
        "D": "Government or related policy organisations",
        "E": "Blue Economy industry, including SMEs",
        "F": "NGOs, including civil society & citizens",
        "G": "Other (please specify)",
    }
}

# Apply the legend replacements for specific columns
for col, legend in custom_legend.items():
    if col in df.columns:
        df[col] = df[col].map(legend)

# Define custom words to omit from the word cloud
custom_stopwords = set(STOPWORDS).union({"survey", "data", "result", "Data", "value", "Lake", "Blue", "Cloud", "EDITO", "user", "s"})  # Add/remove words as needed

# Centralized configuration for graph styles

GRAPH_LAYOUT = {
    "title": {
        "x": 0.5,  # Center the title horizontally
        "xanchor": "center",  # Align the title to the center
        "yanchor": "top",  # Place the title just below the top of the plot
        "font": {"size": 24, "color": "#1f2a44", "family": "Helvetica, Arial, sans-serif"},  # More modern font and color
        "pad": {"t": 20},  # Add some padding above the title for more breathing room
    },
    "legend": {
        "font": {"size": 16, "color": "#4b4b4b"},  # Slightly lighter color for better legibility
        "itemclick": "toggleothers",
        "itemdoubleclick": "toggle",
        "title_font_size": 18,
        "itemwidth": 50,
        "x": 0.5,  # Center the legend horizontally below the plot
        "xanchor": "center",  # Align legend to the center
        "y": -0.15,  # Position the legend below the graph
        "yanchor": "top",  # Ensure the legend is positioned below the plot
        "orientation": "h",  # Horizontal layout
        "traceorder": "normal",  # Control the order in which legend items appear
        "bgcolor": "rgba(255, 255, 255, 0.7)",  # Optional: Add a background color for better visibility
        "bordercolor": "#ccc",  # Optional: Add a border color for the legend box
        "borderwidth": 1,  # Optional: Add border width for clarity
        "itemwidth": 30,  # Set a maximum width for legend items
        "itemsizing": "constant",  # Keep consistent symbol sizing
        "tracegroupgap": 5,  # Space between groups
    },
    "general": {
        "template": "plotly",  # Switch to 'plotly' for a more vibrant, modern style with subtle effects
        "autosize": True,
        "margin": {"t": 20, "b": 5, "l": 20, "r": 20},  # Increased margins for better spacing
        "plot_bgcolor": "#f7f7f7",  # Slightly lighter background for a softer feel
        "paper_bgcolor": "#ffffff",  # White background for contrast
        "xaxis": {
            "showgrid": True,
            "gridcolor": "#e0e0e0",  # Subtle gridlines
            "zeroline": False,
            "showline": True,  # Show axis lines for a cleaner look
            "linecolor": "#ccc",  # Lighter axis line color
            "ticks": "outside",  # Place ticks outside for better readability
            "ticklen": 8,  # Increase tick length for visibility
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": "#e0e0e0",
            "zeroline": False,
            "showline": True,  # Show axis lines for a cleaner look
            "linecolor": "#ccc",
            "ticks": "outside",
            "ticklen": 8,
        },
    },
}

# Graph div styling to enhance layout
DIV_STYLE = {
    "flex": "1 1 45%",  # Two graphs per row, each taking up 45% of the space
    "padding": "10px",  # Padding around the graph for better layout
    "boxSizing": "border-box",
    "border": "1px solid #ecf0f1",  # Light border for a clean appearance
    "borderRadius": "12px",  # Rounded corners for a modern touch
    "backgroundColor": "#ffffff",  # White background for contrast
    "boxShadow": "0px 4px 16px rgba(0, 0, 0, 0.1)",  # Slightly more pronounced shadow for depth
    "transition": "all 0.3s ease-in-out",  # Smooth transition when hovering over elements
}

# Section layout to improve visual spacing and clarity
SECTION_LAYOUT = {
    "display": "flex",
    "flexWrap": "wrap",
    "padding": "10px",  # Padding for sections
    "gap": "30px",  # Larger gap for more breathing room between graphs
    "alignItems": "center",  # Vertically center the content in each section
}
# Initialize the Dash app
app = Dash(__name__)
server = app.server
app.title = "Survey Results Dashboard"

# Define the sections with corrected column indices
sections = {
    "Section 1: About the Respondent": [1, 2],  # Indices of columns B and C
    "Section 2: About your current use of Blue-Cloud": [3, 4, 5, 6, 7, 8, 9, 10, 11],  # Columns C to N
    "Section 3: About Blue-Cloud thematic contribution to EOSC": [12, 13, 14, 15, 16, 17, 18, 19, 20],  # Columns M to X
    "Section 4: About Blue-Cloud evolution as an incubator for the EU DTO": [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],  # Columns Y to AJ
    "Section 5: About Blue-Cloud as a contributor to the UN Ocean Decade": [36],  # Column AK
}

def create_graph_for_question(question, is_numeric=False):
    # Debugging: print out the current question being processed
    print(f"Creating graph for question: {question}")
    
    # For pie charts (custom columns for pie chart)
    if question in [df.columns[1], df.columns[2], df.columns[3], df.columns[13], df.columns[32], df.columns[33], df.columns[34]]:
        print(f"Generating pie chart for {question}")  # Debugging
        fig = px.pie(df, names=question, title=f"{question}".replace("/", "<br>"))
        fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r))  # Custom color scheme
        fig.update_layout(
            title=None,  # Centered title
            legend=GRAPH_LAYOUT["legend"],  # Vertical legend to the right
            **GRAPH_LAYOUT["general"],  # Apply general layout settings
        )
        # Create a custom title for the pie chart
        title_html = html.Div(
            f"{question}".replace("/", "<br>"),  # Custom title (replace '/' with a line break)
            style={
                'textAlign': 'center',
                'fontSize': '24px',
                'color': '#1f2a44',
                'fontFamily': 'Helvetica, Arial, sans-serif',
                'fontWeight': 'normal',
                'marginBottom': '2px',  # Ensure spacing between title and graph
            }
        )
        return html.Div(
                children=[
                    title_html, 
                        dcc.Graph(figure=fig, style={"margin": "10px 0", "padding": "0", "display": "flex", "flexDirection": "column", "alignItems": "center"})
                    ],
                      # Correct placement of 'style'
            )
    
    elif df[question].dtype in ["int64", "float64"] or is_numeric:
        print(f"Generating numeric graph for {question}")  # Debugging
        # Define value mapping and category order
        value_mapping = {1: "Very Poor", 2: "Poor", 3: "Good", 4: "Very Good"}
        category_order = ["Very Poor", "Poor", "Good", "Very Good"]

        # Map the numeric values to their respective labels
        value_counts = df[question].map(value_mapping).value_counts()  # Directly map and count
        value_counts = value_counts.reindex(category_order, fill_value=0).reset_index()  # Ensure order
        value_counts.columns = ["Value", "Count"]  # Rename columns for Plotly
        
        # Create pie chart
        fig = px.pie(
            value_counts,
            names="Value",
            values="Count",
            title=None,
            color="Value",
            color_discrete_sequence=px.colors.sequential.Blues_r,
            category_orders={"Value": category_order},  # Ensure legend order
        )
        fig.update_layout(
            title=None,
            legend=GRAPH_LAYOUT["legend"],
            **GRAPH_LAYOUT["general"],
        )
        # Create a custom title for the numeric graph
        title_html = html.Div(
            f"{question}".replace("/", "<br>"),
            style={
                'textAlign': 'center',
                'fontSize': '24px',
                'color': '#1f2a44',
                'fontFamily': 'Helvetica, Arial, sans-serif',
                'fontWeight': 'normal',
                'marginBottom': '2px',  # Ensure spacing between title and graph
            }
        )
        
        # Return the title and the graph together
        return html.Div(
            children=[title_html, dcc.Graph(figure=fig, style={"width": "100%", "height": "100%"})],  # Ensure the container has the same style as the graphs
        )

    elif df[question].dtype == "object":
        print(f"Generating wordcloud for {question}")  # Debugging
        # Wordcloud generation for textual data
        return generate_wordcloud_for_question(question)

    return html.Div(f"No graph or word cloud for {question} - unsupported data type.")
    
def generate_wordcloud_for_question(question):
    print(f"Generating word cloud for question: {question}")  # Debugging
    if df[question].dtype == "object":  # Only create word clouds for text data
        text = " ".join(df[question].dropna().astype(str))  # Combine text from the column
        if len(text.strip()) == 0:
            return html.Div("No valid responses for word cloud.", style={"color": "red"})
        
        # Generate the word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            max_words=50,
            max_font_size=100,
            min_font_size=10,
            stopwords=custom_stopwords,
            background_color="white",
        ).generate(text)

        # Convert to base64 image for display
        buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()

        # Title for word cloud
        title_html = html.Div(
            question,
            style={
                'textAlign': 'center',
                'fontSize': '24px',
                'color': '#1f2a44',
                'fontFamily': 'Helvetica, Arial, sans-serif',
                'fontWeight': 'normal',
            }
        )
        wordcloud_html = html.Img(
            src=f"data:image/png;base64,{encoded_image}",
            style={
                'display': 'block',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'maxWidth': '100%',
                'maxHeight': '100%',
            }
        )
        return html.Div([title_html, wordcloud_html])
    return html.Div(f"No word cloud for {question} - not text data.")

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "margin": "24px"},
    children=[
        # Container for the image and title
        html.Div(
            style={
                "display": "flex",  # Flexbox for side-by-side layout
                "alignItems": "center",  # Vertically align items
                "marginBottom": "20px"  # Adds space below this section
            },
            children=[
                # Responsive image
                html.Img(
                    src='assets/EOSC _ BlueCloud2026_Payoff_ColourPos.png',  # Replace with your image file path
                    style={
                        "width": "35%",  # Larger width for better visibility
                        "height": "auto",  # Maintain aspect ratio
                        "maxWidth": "600px",  # Ensure image doesn't get too large
                        "marginRight": "20px"  # Add space between image and title
                    }
                ),
        # Title of the app
                html.Div(
                    children=[
                        html.H1(
                            "Stakeholder Consultation Survey Dashboard",
                            style={
                                "textAlign": "left",  # Align text to the left
                                "color": "#2c3e50",
                                "fontSize": "28px"  # Slightly larger font size for prominence
                            }
                        ),
                        html.P(
                            "Explore the survey results through interactive visualizations.",
                            style={
                                "textAlign": "left",
                                "color": "#7f8c8d",
                                "fontSize": "16px"
                            }
                        ),
                    ]
                )
            ]
        ),
        # Create tabs for each section
        dcc.Tabs(
            id="tabs",
            value="Section 1: About the Respondent",
            children=[
                dcc.Tab(
                    label=section,
                    value=section,
                    children=[
                        # Add custom subtitle for each section
                        html.H2(f"Subtitle for {section}", style={"textAlign": "center", "fontSize": "20px", "color": "#34495e"}),  # Custom subtitle
                        html.Div(
                            id=f"graphs-{section}",
                            style=SECTION_LAYOUT if section != "Section 1: About the Respondent" else {},  # Remove SECTION_LAYOUT for Section 1
                            
                        ),
                    ]
                ) for section in sections
            ]
        ),
    ]
)

@app.callback(
    [Output(f"graphs-{section}", "children") for section in sections],
    [Input("tabs", "value")]
)
def update_graphs_by_section(selected_section):
    print(f"Selected section: {selected_section}")  # Debugging: check which section was selected
    section_columns = sections[selected_section]
    graphs = []

    for col in section_columns:
        question = df.columns[col]
        print(f"Creating graph for question: {question}")  # Debugging: check the question being processed
        is_numeric = df[question].dtype in ["int64", "float64"]
        graph = create_graph_for_question(question, is_numeric=is_numeric)

        # Ensure that each graph is wrapped in a div with proper styling
        graphs.append(html.Div(children=[graph], style=DIV_STYLE))

    # Ensure proper structure for the selected section's graphs
    return [
        html.Div(
            children=graphs if selected_section == section else [],
            style=SECTION_LAYOUT if selected_section == section else {},  # Apply SECTION_LAYOUT only for selected section
        )
        for section in sections
    ]


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
