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

def create_multi_select_histogram(df, question):
    options = df[question].dropna().str.split(",").explode().str.strip()
    unique_options = sorted(options.unique())
    option_counts = pd.DataFrame({
        "Option": unique_options,
        "Count": [options.tolist().count(opt) for opt in unique_options]
    })
    
    fig = px.bar(
        option_counts, x="Option", y="Count", 
        color="Option", 
        category_orders={"Option": unique_options}
    )
    print(option_counts["Count"] / option_counts["Count"].max())
    fig.update_traces(marker_color=sample_colorscale("RdYlGn", option_counts["Count"] / option_counts["Count"].max()))
    
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

def create_numeric_pie_chart(df, question, value_mapping, category_order):
    # Map the values using the value_mapping and ensure missing values are handled
    mapped_values = df[question].map(value_mapping).fillna("Unknown")
       
    # Calculate the value counts of the mapped values
    mapped_values = pd.Categorical(mapped_values, categories=category_order, ordered=True)
    # Create the pie chart with the mapped values
    value_counts = mapped_values.value_counts()
    value_counts.columns = ["Value", "Count"]
    
    fig = px.pie(
        names=value_counts.index,  # Use the categories (index) directly
        values=value_counts.values,  # Use the counts
        color=value_counts.index,  # Color by category name
        category_orders={'Value': category_order}
        )
    
    # Update trace style (optional)
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

def create_ordered_pie_chart(df, question, category_order):
    value_counts = df[question].value_counts()
    value_counts = value_counts.reindex(category_order, fill_value=0).reset_index()
    value_counts.columns = ["Value", "Count"]
    fig = px.pie(
        value_counts, names="Value", values="Count", 
        color="Value", 
        category_orders={"Value": category_order}
    )
    fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r), hoverinfo="name+value")
    fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    
    title_html = html.Div(
        f"{question}".replace("/", "<br>"),
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])
pass