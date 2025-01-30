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
    
    # Count occurrences of each category
    vc = mapped_pie.value_counts().reset_index()
    
    # Extract names and values dynamically without renaming columns
    category_column, value_column = vc.columns  # Get column names dynamically
    print(vc.dtypes)  # Debugging

    # Create the pie chart
    fig = px.pie(
        vc,
        names=category_column,  # Use extracted column names
        values=value_column,
        color=category_column,  
        category_orders={category_column: category_order}
    )
    
    # Update trace style
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r), hoverinfo="name+value")
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
        "a": unique_hist,
        "b": [hist_df.tolist().count(opt) for opt in unique_hist] 
    })
    # Rename columns
    hist_counts.columns = ["a", "b"]
    hist_counts["b"] = pd.to_numeric(hist_counts["b"])  # Ensure 'b' is numeric
        
    fig = px.bar(
        hist_counts, x="a", y="b", 
        color="a", 
        category_orders={"a": unique_hist}
    )

    fig.update_traces(marker_color=sample_colorscale("RdYlGn", hist_counts["b"] / hist_counts["b"].max()))    
    fig.update_layout(
        title=None, 
        xaxis_title="Options",
        yaxis_title="Count",
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
    ord_values.columns = ["a", "b"]  # Rename columns
    ord_values["b"] = pd.to_numeric(ord_values["b"])


    print(ord_values)  # Debugging
    print(ord_values.shape)
    print(ord_values.head())

    # Create the pie chart
    fig = px.pie(
        ord_values,  
        names="a",  # Use the column name directly
        values="b",
        color="a",
        category_orders={"a": category_order}
    )
    
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
pass