import plotly.express as px
import pandas as pd
from dash import html, dcc
from plotly.colors import sample_colorscale
from assets.layouts import GRAPH_LAYOUT, bc_service_label


def create_pie_chart(df, question):
        # Get unique values from the column
    unique_labels = df[question].dropna().unique()

    # Define colors: Red-Green for Yes/No, otherwise Sequential Blue
    if set(unique_labels) == {"Yes", "No"}:
        color_mapping = {"Yes": "#32a35e", "No": "#e34a42"}  # Green for Yes, Red for No
        fig = px.pie(df, names=question, title=f"{question}", color=question, color_discrete_map=color_mapping)
        fig.update_layout(title=None, legend=GRAPH_LAYOUT["legend"], **GRAPH_LAYOUT["general"])
    else:
        fig = px.pie(df, names=question, title=f"{question}")
        fig.update_traces(marker=dict(colors=px.colors.sequential.Blues_r))
        fig.update_layout(title = None, legend=dict(
            orientation="v",  # Vertical legend
            x=0.5,           # Position it on the right
            y=1,            # Center it vertically
            xanchor="center",
            yanchor="bottom"
        ))
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

def create_numeric_pie_chart(df, question, value_mapping, category_order,color_mapping):
    
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
        color_discrete_map = color_mapping
    )
    
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

def create_multi_select_histogram(df, question):
    hist_df = df[question].dropna().str.split(",").explode().str.strip()
    hist_df = hist_df.map(bc_service_label).dropna()
    unique_hist = sorted(hist_df.unique(), reverse = True)
    hist_counts = pd.DataFrame({
        "Answers": unique_hist,
        "Counts": [hist_df.tolist().count(opt) for opt in unique_hist] 
    })
            
    fig = px.bar(hist_counts, x="Counts", y="Answers", orientation="h")
    
    fig.update_traces(marker_color=sample_colorscale("RdYlGn", hist_counts["Counts"] / hist_counts["Counts"].max())) 
       
    fig.update_layout(
        title=None, 
        xaxis_title="Counts",
        yaxis_title="Answers",
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
    
    color_mapping = {"I fully disagree": "#e34a42",
                    "I slightly disagree":"#fcd177", 
                    "I slightly agree":"#98c792", 
                    "I fully agree":"#32a35e"}
    
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
        f"{question}",
        style={
            'textAlign': 'center', 'fontSize': '20px', 'color': '#1f2a44',
            'fontFamily': 'Helvetica, Arial, sans-serif', 'fontWeight': 'normal', 'marginBottom': '2px'
        }
    )
    return html.Div([title_html, dcc.Graph(figure=fig)])
pass