import plotly.express as px
import pandas as pd
from dash import html, dcc
from plotly.colors import sample_colorscale
from assets.layouts import GRAPH_LAYOUT


def create_pie_chart(df, question):
    fig = px.pie(df, names=question, title=f"{question}")
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r), hoverinfo="name+value")
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])

    title_html = html.Div(
        f"{question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])

def create_numeric_pie_chart(df, question, value_mapping, category_order):
    # Map the values using the value_mapping and handle missing values
    mapped_pie = df[question].map(value_mapping).fillna("Unknown")
    
    vc = mapped_pie.value_counts().reset_index()
    category_column, value_column = vc.columns  

    vc[category_column] = pd.Categorical(vc[category_column], categories=category_order, ordered=True)
    vc = vc.sort_values(by=category_column)

    # Create the pie chart
    fig = px.pie(
        vc,
        names=category_column,  # Use extracted column names
        values=value_column,
        color=category_column,  
    )
    
    # Update trace style
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r), hoverinfo="name+value", sort = False)
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

def create_multi_select_histogram(df, question):
    hist_df = df[question].dropna().str.split(",").explode().str.strip()
    unique_hist = sorted(hist_df.unique())
    hist_counts = pd.DataFrame({
        "Answers": unique_hist,
        "Counts": [hist_df.tolist().count(opt) for opt in unique_hist] 
    })
            
    fig = px.bar(hist_counts, x="Answers", y="Counts")
    
    print(hist_counts)
    fig.update_traces(marker_color=sample_colorscale("RdYlGn", hist_counts["Counts"] / hist_counts["Counts"].max())) 
       
    fig.update_layout(
        title=None, 
        xaxis_title="Answers",
        yaxis_title="Counts",
        legend=GRAPH_LAYOUT["legend"], 
        **GRAPH_LAYOUT["general"]
    )

    title_html = html.Div(
        f"{question}".replace("/", "<br>"),
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )

    return html.Div([title_html, dcc.Graph(figure=fig)])

def create_ordered_pie_chart(df, question, category_order):
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
    )
    
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r), hoverinfo="name+value", sort = False)
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    
    title_html = html.Div(
        f"{question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])
pass