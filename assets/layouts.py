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
        "itemclick": False,
        "itemdoubleclick": False,
        "title_font_size": 18,
        "itemwidth": 50,
        "x": 0.5,  # Center the legend horizontally below the plot
        "xanchor": "center",  # Align legend to the center
        "y": -0.15,  # Position the legend below the graph
        "yanchor": "top",  # Ensure the legend is positioned below the plot
        "orientation": "h",  # Horizontal layout
        "bgcolor": "rgba(255, 255, 255, 0.7)",  # Optional: Add a background color for better visibility
        "bordercolor": "#ccc",  # Optional: Add a border color for the legend box
        "borderwidth": 1,  # Optional: Add border width for clarity
        "itemwidth": 30,  # Set a maximum width for legend items
        "itemsizing": "constant",  # Keep consistent symbol sizing
        "tracegroupgap": 10,  # Space between groups
        "traceorder": "normal"
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
            "tickmode": "linear",
            "automargin": True
        },
    },
}
HISTOGRAM_GRAPH_LAYOUT = {
    "legend": {
        "font": {"size": 14, "color": "#4b4b4b"},
        "itemclick": False,
        "itemdoubleclick": False,
        "title_font_size": 16,
        "itemwidth": 500,  # Increase width to allow multi-line wrapping
        "x": 0.5,
        "xanchor": "center",
        "y": -0.2,  # Push it further below if needed
        "yanchor": "top",
        "orientation": "h",
        "bgcolor": "rgba(255, 255, 255, 0.7)",
        "bordercolor": "#ccc",
        "borderwidth": 1,
        "tracegroupgap": 100,  # Reduce space between grouped legend items
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

HISTOGRAM_STYLE = {
    "display: flex"
    "flex": "1 1 100%",  # Ensure the histogram takes up 100% of the space (full width)
    "flexDirection: column" 
    "padding": "20px",  # Padding around the graph for better layout and spacing
    "boxSizing": "border-box",  # Ensure padding and borders are included in width/height calculations
    "border": "1px solid #ecf0f1",  # Light border for a clean appearance
    "borderRadius": "12px",  # Rounded corners for a modern touch
    "backgroundColor": "#ffffff",  # White background for contrast
    "boxShadow": "0px 4px 16px rgba(0, 0, 0, 0.1)",  # Slightly more pronounced shadow for depth
    "transition": "all 0.3s ease-in-out",  # Smooth transition when hovering over elements
    "height": "auto",  # Allow for auto-height adjustment
}

COUNTER_STYLE = {
    "textAlign": "center",
    "fontSize": "18px",
    "color": "#2c3e50",
    "marginBottom": "10px",
    "width": "20%",  # Box takes up 20% of the window width
    "marginLeft": "auto",  # Automatically center horizontally
    "marginRight": "auto",  # Automatically center horizontally
    "backgroundColor": "#ffffff",  # Light grey background
    "padding": "10px",  # Add some padding for better appearance
    "borderRadius": "12px",  # Add rounded corners for aesthetics
    "boxShadow": "0px 4px 16px rgba(0, 0, 0, 0.1)",  # Slightly more pronounced shadow for depth
    "transition": "all 0.3s ease-in-out",
}

# Section layout to isual spacing and claritimprove vy
SECTION_LAYOUT = {
    "display": "flex",
    "flexWrap": "wrap",
    "padding": "10px",  # Padding for sections
    "gap": "30px",  # Larger gap for more breathing room between graphs
    "alignItems": "center",  # Vertically center the content in each section
}

# Define the sections with corrected column indices
sections = {
    "Section 1: About the Respondent": [3, 4],
    "Section 2: About your current use of Blue-Cloud": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "Extra Section: Blue cloud Services usage": [16],
    "Section 3: About Blue-Cloud thematic contribution to EOSC": [59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
    "Section 4: About Blue-Cloud evolution as an incubator for the EU DTO": [71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84],
    "Section 5: About Blue-Cloud as a contributor to the UN Ocean Decade": [85, 86],
}
# Define subtitles for each section
section_subtitles = {
    "Section 1: About the Respondent": "Professional and Organisational repartition of respondants",
    "Section 2: About your current use of Blue-Cloud": "Blue-Cloud is designed to support collaborative scientific research by promoting open science practices. It aims to be more than just a platform: it seeks to be a comprehensive infrastructure that fosters collaboration, open science, and efficient research workflows. This is achieved by providing customizable and readily available VLabs that can be tailored to the specific needs of diverse research communities. In this section, we invite your input on Blue-Cloud’s services, including those offered by existing VLabs.",
    "Extra Section: Blue cloud Services usage": "Usage and Evaluation of specific Services",
    "Section 3: About Blue-Cloud thematic contribution to EOSC": "Blue-Cloud is conceived as a marine thematic service that is contributing to shaping the European Open Science Cloud (EOSC). Likewise, participation in EOSC opens opportunities for the Blue-Cloud community. As a Blue-Cloud stakeholder, what type of value, services and/or type of representation would you be looking for in EOSC? Please rank the following according to your level of interest",
    "Section 4: About Blue-Cloud evolution as an incubator for the EU DTO": "Please consider the following statements, which tackle aspects related to interoperability between Blue-Cloud and EDITO -the public infrastructure of the European Digital Twin Ocean- and classify them according to their interest to you:",
    "Section 5: About Blue-Cloud as a contributor to the UN Ocean Decade": "", 
}