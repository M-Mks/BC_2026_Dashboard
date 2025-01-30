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
    hist_df = df[question].dropna().str.split(",").explode().str.strip()
    unique_hist = sorted(hist_df.unique())
    hist_counts = pd.DataFrame({
        "Option": unique_hist,
        "Count": [hist_df.tolist().count(opt) for opt in unique_hist]
    })
    print(unique_hist)
    fig = px.bar(
        hist_counts, x="Option", y="Count", 
        color="Option", 
        category_orders={"Option": unique_hist}
    )
    print(hist_counts["Count"] / hist_counts["Count"].max())
    fig.update_traces(marker_color=sample_colorscale("RdYlGn", hist_counts["Count"] / hist_counts["Count"].max()))
    
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
    # Map the values using the value_mapping and handle missing values
    mapped_pie = df[question].map(value_mapping).fillna("Unknown")
    
    # Count occurrences of each category
    vc = mapped_pie.value_counts().reset_index()
    vc.columns = ["option", "Count"]  # Rename for clarity

    print(vc)  # Debugging

    # Create the pie chart
    fig = px.pie(
        vc,
        names="option",  # Use column names directly
        values="Count",
        color="option",  
        category_orders={"option": category_order}
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
    # Get value counts and convert to DataFrame
    ord_values = df[question].value_counts().reset_index()
    ord_values.columns = ["option", "Count"]  # Rename columns

    print(ord_values)  # Debugging
    print(ord_values.shape)
    print(ord_values.head())

    # Create the pie chart
    fig = px.pie(
        ord_values,  
        names="option",  # Use the column name directly
        values="Count",
        color="option",
        category_orders={"option": category_order}
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