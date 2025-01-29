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

# Importing custom layout configurations from layouts.py
from assets.helper_functions import create_pie_chart, create_multi_select_pie_chart, create_numeric_pie_chart, create_ordered_pie_chart
from assets.layouts import custom_legend, DIV_STYLE, SECTION_LAYOUT, sections, section_subtitles, COUNTER_STYLE

# Load the CSV file
file_path = "Copy_Rand_Quantitative_results.csv"  # Update with your CSV file path
df = pd.read_csv(file_path, sep=";", encoding="utf-8")

# Apply the legend replacements for specific columns
for col, legend in custom_legend.items():
    if col in df.columns:
        df[col] = df[col].map(legend)

# Define custom words to omit from the word cloud
custom_stopwords = set(STOPWORDS).union({"survey", "data", "result", "Data", "value", "Lake", "Blue", "Cloud", "EDITO", "user", "s"})  # Add/remove words as needed
respondent_count = df.shape[0]  # Number of rows in the DataFrame


# Initialize the Dash app
app = Dash(__name__)
server = app.server
app.title = "Survey Results Dashboard"

def create_graph_for_question(question, is_numeric=False, section=None):
    print(f"Creating graph for question: {question}")  # Debugging
    
    # For specific pie charts
    if question in [df.columns[1], df.columns[2], df.columns[3]]:
        print(f"Generating pie chart for {question}")  # Debugging
        return create_pie_chart(df, question)
        
    # For numeric pie charts (non-Section 2)
    if question in df.columns[3:10]:
        print(f"Generating numeric graph for {question}")  # Debugging
        return create_numeric_pie_chart(df, question, value_mapping={
            1: "Very Poor", 2: "Poor", 3: "Good", 4: "Very Good"
        }, category_order=["Very Poor", "Poor", "Good", "Very Good"])
    
    # For multi-select pie chart in a specific section
    if  question in [df.columns[13]]:
        print(f"Generating multi-select pie chart for {question} in {section}")  # Debugging
        return create_multi_select_pie_chart(df, question)
    
    # For specific ordered pie charts
    if question in [df.columns[32], df.columns[33], df.columns[34]]:
        print(f"Generating ordered pie chart for {question}")  # Debugging
        return create_ordered_pie_chart(df, question, category_order=[
            "I fully disagree", "I slightly disagree", "I slightly agree", "I fully agree"
        ])
    
    # For numeric pie charts with a different value mapping
    if is_numeric:
        print(f"Generating numeric graph for {question}")  # Debugging
        return create_numeric_pie_chart(df, question, value_mapping={
            1: "Not Interested", 2: "Somewhat interested", 3: "Interested", 4: "Essential"
        }, category_order=["Not Interested", "Somewhat interested", "Interested", "Essential"])
    
    # For word clouds
    if df[question].dtype == "object":
        print(f"Generating word cloud for {question}")  # Debugging
        return generate_wordcloud_for_question(question)
    
    # Default fallback
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
                'fontSize': '20px',
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
                        # Use the subtitle dictionary to fetch a custom subtitle for each section
                        html.H2(
                            section_subtitles.get(section, "Explore this section for detailed insights."),  # Default subtitle if not found
                            style={"textAlign": "center", "fontSize": "20px", "color": "#34495e"}
                        ),
                        html.Div(
                            f"Respondent Count: {respondent_count}",
                            style=COUNTER_STYLE,
                        ) if section == "Section 1: About the Respondent" else None,
                            
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
