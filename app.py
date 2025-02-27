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
from assets.helper_functions import YesNo_pie_chart, Section_1_pie_chart, create_multi_select_histogram, Interest_S3_pie_chart, Interest_S4_pie_chart, Agreement_pie_chart, create_pies
from assets.layouts import DIV_STYLE, SECTION_LAYOUT, sections, section_subtitles, COUNTER_STYLE

# Load the CSV file
file_path = "stakeholder_consultation.csv"  # Update with your CSV file path
df = pd.read_csv(file_path, sep=";", encoding="utf-8")

# Define custom words to omit from the word cloud
custom_stopwords = set(STOPWORDS).union({"survey", "data", "result", "Data", "value", "Lake", "Blue", "Cloud", "EDITO", "user", "s"})  # Add/remove words as needed
respondent_count = df.shape[0]  # Number of rows in the DataFrame


# Initialize the Dash app
app = Dash(__name__)
server = app.server
app.title = "Survey Results Dashboard"

# Graph style definition
wordcloud_cols = list(range(33, 36)) + list(range(64, 67)) + list(range(81, 84)) + [67,69, 77]
interestS3_cols = list(range(57, 64))
interestS4_cols =  list(range(70, 77))
extra_wc_cols = list(range(37, 56))
agreement_cols = list(range(78, 81))  # CA to CC
pies_cols = list(range(27, 33))+[56, 68]  # Z to AG
histogram_col = [36]
print(wordcloud_cols)

def create_graph_for_question(question):
    #General
    question_index = df.columns.get_loc(question)
        
    # For section1 pie charts
    if question_index in sections["Section 1: About the Respondent"]:
        return Section_1_pie_chart(df, question)
    
    if question_index in wordcloud_cols:  # Only create word clouds for text data
        return generate_wordcloud_for_question(question)
    
    # For multi-select pie chart in a specific section
    if  question in [df.columns[36]]:
        return create_multi_select_histogram(df, question)
    
    if question_index in interestS3_cols:
        return Interest_S3_pie_chart(df, question)
    
    if question_index in interestS4_cols:
        return Interest_S4_pie_chart(df, question)
    
    if question_index in agreement_cols:
        return Agreement_pie_chart(df, question, category_order={"I fully disagree",
                                                                    "I slightly disagree", 
                                                                    "I slightly agree", 
                                                                    "I fully agree"})
                
    if question_index in pies_cols:
        return create_pies(df, question,category_order=["Very Poor",
                                                            "Poor", 
                                                            "Good", 
                                                            "Very Good"], 
                                        color_mapping = {"Very Poor": "#e34a42",       
                                                            "Poor": "#fcd177",     
                                                            "Good": "#98c792",      
                                                            "Very Good": "#32a35e"})
    if question in [df.columns[25]]:
        return create_pies(df, question, category_order=["Very Unsatisfied",
                                                            "Unsatisfied", 
                                                            "Neutral", 
                                                            "Satisfied",
                                                           "Very Satisfied"], 
                                        color_mapping = {"Very Unsatisfied": "#e34a42",       
                                                            "Unsatisfied": "#fcd177",
                                                            "Neutral": "#c5d89f",  # Light Olive Green
                                                            "Satisfied": "#98c792",      
                                                            "Very Satisfied": "#32a35e"})

    if question in [df.columns[26]]:
        return YesNo_pie_chart(df, question)  

def generate_wordcloud_for_question(question):      
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
                            style=SECTION_LAYOUT,   
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
        graph = create_graph_for_question(question)

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
