import plotly.express as px
import pandas as pd
from dash import html, dcc
from plotly.colors import sample_colorscale
from assets.layouts import GRAPH_LAYOUT

def clean_S3_question_title(question):
    # Define the part of the question to remove
    intro_text = ("Blue-Cloud is conceived as a marine thematic service that is contributing "
                  "to shaping the European Open Science Cloud (EOSC). Likewise, participation "
                  "in EOSC opens opportunities for the Blue-Cloud community. As a Blue-Cloud "
                  "stakeholder, what type of value, services and/or type of representation "
                  "would you be looking for in EOSC? Please rank the following according to your level of interest:")
    
    # Remove the intro if it exists
    cleaned_S3_question = question.replace(intro_text, "").strip()
    
    return cleaned_S3_question

def clean_S4_question_title(question):
    # Define the part of the question to remove
    intro_text = ("Please consider the following statements, which tackle aspects related " 
                  "to interoperability between Blue-Cloud and EDITO -the public infrastructure of the " 
                  "European Digital Twin Ocean- and classify them according to their interest to you:")
    
    # Remove the intro if it exists
    cleaned_S4_question = question.replace(intro_text, "").strip()
    
    return cleaned_S4_question

def clean_S42_question_title(question):
    # Define the part of the question to remove
    intro2_text = ("Please indicate to which extent you agree with the following statements:: --")
    
    # Remove the intro if it exists
    cleaned_S42_question = question.replace(intro2_text, "").strip()
    
    return cleaned_S42_question

def Section_1_pie_chart(df, question):
# Define colors: Red-Green for Yes/No, otherwise Sequential Blue

    fig = px.pie(df, names=question, title=f"{question}")
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r))
    fig.update_layout(title = None, legend=dict(
        orientation="v",  # Vertical legend
        x=0.5,           # Position it on the right
        y=1,            # Center it vertically
        xanchor="center",
        yanchor="bottom"
    ), **GRAPH_LAYOUT["general"])
    # General layout updates
    fig.update_traces(hovertemplate="%{label}: %{value}")
    
    title_html = html.Div(
        f"{question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])

def Interest_S3_pie_chart(df, question):
    category_order = ["Not interested",
                    "Somewhat Interested", 
                    "Interested", 
                    "Essential"]
    color_mapping = {"Not interested": "#e34a42",
                    "Somewhat Interested":"#fcd177", 
                    "Interested":"#98c792", 
                    "Essential":"#32a35e"}
    
    cleaned_question = clean_S3_question_title(question)

    # Get value counts and convert to DataFrame
    ord_values = df[question].value_counts().reset_index()
    cat_c, v_c = ord_values.columns  

    ord_values[cat_c] = pd.Categorical(ord_values[cat_c], categories=category_order, ordered=True)
    ord_values = ord_values.sort_values(by=cat_c)
    
# Create the pie chart
    fig = px.pie(
        ord_values,  
        names=cat_c,  # Use the column name directly
        values=v_c,
        color=cat_c,
        color_discrete_map = color_mapping,
        )
    
    fig.update_traces(hovertemplate="%{label}: %{value}",sort = False)
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    title_html = html.Div(
        f"{cleaned_question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])

def Interest_S4_pie_chart(df, question):
    category_order = ["Not Interested",
                    "Somewhat Interested", 
                    "Interested", 
                    "Essential"]
    color_mapping = {"Not Interested": "#e34a42",
                    "Somewhat Interested":"#fcd177", 
                    "Interested":"#98c792", 
                    "Essential":"#32a35e"}
    
    cleaned_S4_question = clean_S4_question_title(question)

    # Get value counts and convert to DataFrame
    ord_values = df[question].value_counts().reset_index()
    cat_c, v_c = ord_values.columns  

    ord_values[cat_c] = pd.Categorical(ord_values[cat_c], categories=category_order, ordered=True)
    ord_values = ord_values.sort_values(by=cat_c)
        
    # Create the pie chart
    fig = px.pie(
        ord_values,  
        names=cat_c,  # Use the column name directly
        values=v_c,
        color=cat_c,
        color_discrete_map = color_mapping,
        )
    
    fig.update_traces(hovertemplate="%{label}: %{value}",sort = False)
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    title_html = html.Div(
        f"{cleaned_S4_question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])

def create_pies(df, question, category_order, color_mapping):
    # Handle missing values by replacing with "No Answer"
    df_cleaned = df.copy()
    df_cleaned[question] = df_cleaned[question].fillna("No Answer")

    # Compute value counts
    vc = df_cleaned[question].value_counts().reset_index()
    category_column, value_column = vc.columns  

    # Ensure "No Answer" is included in category_order if missing
    if "No Answer" in vc[category_column].values and "No Answer" not in category_order:
        category_order.append("No Answer")

    # Convert to categorical and sort
    vc[category_column] = pd.Categorical(vc[category_column], categories=category_order, ordered=True)
    vc = vc.sort_values(by=category_column)

    # Ensure "No Answer" gets a color if not in the color mapping
    color_mapping = color_mapping.copy()  # Avoid modifying the original dictionary
    if "No Answer" not in color_mapping:
        color_mapping["No Answer"] = "#bbbbbb"  # Light gray for missing data

    # Create the pie chart
    fig = px.pie(
        vc,
        names=category_column,
        values=value_column,
        color=category_column,
        color_discrete_map=color_mapping
    )

    # Update trace style
    fig.update_traces(hovertemplate="%{label}: %{value}", sort=False)
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])

    # Create a title for the chart
    title_html = html.Div(
        f"{question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )

    return html.Div([title_html, dcc.Graph(figure=fig)])

def count_yes_responses(df, columns):
    yes_counts = {df.columns[col]: (df.iloc[:, col] == "Yes").sum() for col in columns}
    return pd.DataFrame({
        "Column": list(yes_counts.keys()),
        "Yes Count": list(yes_counts.values())
    })

def create_yes_histogram(df, extra_hist_cols):
    """Creates a single horizontal bar chart showing the 'Yes' counts per column with styling."""
    # Count "Yes" responses for the specified columns
    yes_counts_df = count_yes_responses(df, extra_hist_cols)
    
    # Create the bar chart
    fig = px.bar(
        yes_counts_df,
        x="Yes Count",  # Use "Yes Count" as the x-axis
        y="Column",  # Columns are used as the y-axis (questions)
        orientation="h",  # Horizontal bars
        text="Yes Count",
    )

    # Apply color scaling
    fig.update_traces(
        marker_color=sample_colorscale("RdYlGn", yes_counts_df["Yes Count"] / yes_counts_df["Yes Count"].max())
    )

    # Update layout with custom legend and other settings
    fig.update_layout(
        title=None,
        xaxis_title="Counts",
        yaxis_title="Answers",
        legend=dict(
            title="Legend",
            itemsizing="constant",  # Ensures the size remains constant
            traceorder="normal",  # Keeps the order of traces
            font=dict(size=12),
            orientation="h",  # Horizontal legend
            tracegroupgap=10 # Space between legend items
        ),
        **GRAPH_LAYOUT["general"]  # Apply the general layout settings
    )

    # Title for the graph
    title_html = html.Div(
        "Number of 'Yes' Responses per Option",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )

    # Return the graph inside a div
    return html.Div([title_html, dcc.Graph(figure=fig)])

def Agreement_pie_chart(df, question, category_order):
    # Get value counts and convert to DataFrame
    ord_values = df[question].value_counts().reset_index()
    cat_c, v_c = ord_values.columns  

    ord_values[cat_c] = pd.Categorical(ord_values[cat_c], categories=category_order, ordered=True)
    ord_values = ord_values.sort_values(by=cat_c)
    
    color_mapping = {"I fully disagree": "#e34a42",
                    "I slightly disagree":"#fcd177", 
                    "I slightly agree":"#98c792", 
                    "I fully agree":"#32a35e"}
    
    cleaned_S42_question = clean_S42_question_title(question)
# Create the pie chart
    fig = px.pie(
        ord_values,  
        names=cat_c,  # Use the column name directly
        values=v_c,
        color=cat_c,
        color_discrete_map = color_mapping,
        )
    
    fig.update_traces(hovertemplate="%{label}: %{value}",sort = False)
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    title_html = html.Div(
        f"{cleaned_S42_question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])

def YesNo_pie_chart(df, question):
    color_mapping = {"Yes": "#32a35e", "No": "#e34a42"}  # Green for Yes, Red for No
    fig = px.pie(df, names=question, title=f"{question}", color=question, color_discrete_map=color_mapping)
    
    # Update trace style
    fig.update_traces(hovertemplate="%{label}: %{value}", sort = False)
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    
    # Create a title for the chart
    title_html = html.Div(
        f"{question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    
    return html.Div([title_html, dcc.Graph(figure=fig)])
pass