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
from datetime import date


# Importing custom layout configurations from layouts.py
from assets.helper_functions import YesNo_pie_chart, Section_1_pie_chart, create_yes_histogram, Interest_S3_pie_chart, Interest_S4_pie_chart, Agreement_pie_chart, create_pies
from assets.layouts import DIV_STYLE, SECTION_LAYOUT, sections, section_subtitles, COUNTER_STYLE, DIV5_STYLE

# Load the CSV file
file_path = "stakeholder_consultation.csv"  # Update with your CSV file path
df = pd.read_csv(file_path, sep=";", encoding="utf-8")

# Define custom words to omit from the word cloud
custom_stopwords = set(STOPWORDS).union({"survey", "data", "result", "Data", "value", "Lake", "Blue", "Cloud", "EOSC", "user","EDITO", "EMODnet"})  # Add/remove words as needed , "s"

respondent_count = df.shape[0]  # Number of rows in the DataFrame
today1 = date.today()
today = today1.strftime("%d-%m-%Y")  # Format the date as Month Day, Year
# Initialize the Dash app
app = Dash(__name__)
server = app.server
app.title = "Survey Results Dashboard"

# Graph style definition
wordcloud_cols = list(range(13, 16)) + list(range(67, 71)) + list(range(84, 87)) + [72,80]
interestS3_cols = list(range(60, 67))
interestS4_cols =  list(range(73, 80))
extra_hist_cols = [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58]
agreement_cols = list(range(81, 84))  # CA to CC
pies_cols = list([5, 7, 9, 11, 12, 13, 59, 71])  # Z to AG
YesNo_col = list([6])

def create_graph_for_question(question):
    #General
    question_index = df.columns.get_loc(question)
        
    # For section1 pie charts
    if question_index in sections["Section 1: About the Respondent"]:
        return Section_1_pie_chart(df, question)
    if question_index in wordcloud_cols:  # Only create word clouds for text data
        return generate_wordcloud_for_question(question)
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
                                                            "Very Good",
                                                            "No Answer"], 
                                        color_mapping = {"Very Poor": "#e34a42",       
                                                            "Poor": "#fcd177",     
                                                            "Good": "#98c792",      
                                                            "Very Good": "#32a35e",
                                                            "No Answer": "#d3d3d3"})
    if question in [df.columns[8]]:
        return create_pies(df, question, category_order=["Not Useful",
                                                         "Limited Usefulness",
                                                         "Useful",
                                                         "Very Useful"],     
                                        color_mapping = {"Not Useful": "#e34a42",       
                                                            "Limited Usefulness": "#fcd177",
                                                            "Useful": "#98c792",  # Light Olive Green
                                                            "Very Useful": "#32a35e"})
    if question in [df.columns[10]]:
        return create_pies(df, question, category_order=["Very Poor",
                                                            "Poor", 
                                                            "Comprehensive",
                                                           "Very Comprehensive"], 
                                        color_mapping = {"Very Poor": "#e34a42",       
                                                            "Poor": "#fcd177",
                                                            "Comprehensive": "#98c792",      
                                                            "Very Comprehensive": "#32a35e"})
    if question_index in YesNo_col:
        return YesNo_pie_chart(df, question)  
    if question_index in [df.columns[16]]:
        return create_yes_histogram(df, extra_hist_cols)
                                    
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
        plt.figure(figsize=(10, 6))  # Reduce figure size
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(buffer, format="png", bbox_inches='tight')  # Removes extra padding
        buffer.seek(0)
        encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()

        # Title for word cloud
        title_html = html.Div(
            question,
            style={
                'textAlign': 'center',
                'fontSize': '20px',  # Reduce font size slightly
                'color': '#1f2a44',
                'fontFamily': 'Helvetica, Arial, sans-serif',
                'fontWeight': 'normal',
                'marginBottom': '5px',  # Reduce space between title and word cloud
            }
        )

        wordcloud_html = html.Img(
            src=f"data:image/png;base64,{encoded_image}",
            style={
                'display': 'block',
                'margin': 'auto',  # Center the image and remove extra space
                'width': '80%',  # Reduce width
                'maxHeight': '600px',  # Adjust maximum height
            }
        )

        return html.Div(
            [title_html, wordcloud_html],
            style={
                'textAlign': 'center',
                'padding': '10px',
                'margin': '0px auto',
                'maxWidth': '1000px'  # Limit max width to prevent excessive stretching
            }
        )
    

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
                        html.Div([
                                f"Respondent Count: {respondent_count}", 
                                html.Br(), 
                                f"Latest update: {today}"
                                ],
                            style=COUNTER_STYLE
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
    graphs = {section: [] for section in sections}

    if selected_section == "Extra Section: Blue cloud Services usage":
        # Create the combined histogram for the extra section
        graphs[selected_section].append(create_yes_histogram(df, extra_hist_cols))

    for col in section_columns:
            question = df.columns[col]
            question_index = df.columns.get_loc(question)
            if question_index in wordcloud_cols:
                graph = generate_wordcloud_for_question(question)
                style = DIV5_STYLE
            else:
                graph = create_graph_for_question(question)
                style = DIV_STYLE

            graphs[selected_section].append(html.Div(children=[graph], style=style))

    # Ensure proper structure for the selected section's graphs
    return [html.Div(
        children=graphs[section], 
        style=({"width": "100%"} if selected_section == "Extra Section: Blue cloud Services usage" else SECTION_LAYOUT)
    )
    for section in sections
]   
    
# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
