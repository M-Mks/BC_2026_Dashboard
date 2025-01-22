# Custom legend mapping for specific columns
custom_legend = {
    "Professional Group": {
        "A": "Marine (data) scientist and/or researcher",
        "B": "IT programmer/software developer",
        "C": "Business, infrastructure, or operations manager",
        "D": "Public administration",
        "E": "Other (please specify)",
    },
    "Organization Sector": {
        "A": "Academia",
        "B": "Research organisation",
        "C": "Data and service providers",
        "D": "Government or related policy organisations",
        "E": "Blue Economy industry, including SMEs",
        "F": "NGOs, including civil society & citizens",
        "G": "Other (please specify)",
    }
}

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
        "itemclick": "toggleothers",
        "itemdoubleclick": "toggle",
        "title_font_size": 18,
        "itemwidth": 50,
        "x": 0.5,  # Center the legend horizontally below the plot
        "xanchor": "center",  # Align legend to the center
        "y": -0.15,  # Position the legend below the graph
        "yanchor": "top",  # Ensure the legend is positioned below the plot
        "orientation": "h",  # Horizontal layout
        "traceorder": "normal",  # Control the order in which legend items appear
        "bgcolor": "rgba(255, 255, 255, 0.7)",  # Optional: Add a background color for better visibility
        "bordercolor": "#ccc",  # Optional: Add a border color for the legend box
        "borderwidth": 1,  # Optional: Add border width for clarity
        "itemwidth": 30,  # Set a maximum width for legend items
        "itemsizing": "constant",  # Keep consistent symbol sizing
        "tracegroupgap": 10,  # Space between groups
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
        },
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
    "Section 1: About the Respondent": [1, 2],  # Indices of columns B and C
    "Section 2: About your current use of Blue-Cloud": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],  # Columns C to N
    "Section 3: About Blue-Cloud thematic contribution to EOSC": [14, 15, 16, 17, 18, 19, 20],  # Columns M to X
    "Section 4: About Blue-Cloud evolution as an incubator for the EU DTO": [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],  # Columns Y to AJ
    "Section 5: About Blue-Cloud as a contributor to the UN Ocean Decade": [36],  # Column AK
}
# Define subtitles for each section
section_subtitles = {
    "Section 1: About the Respondent": "Professional and Organisational repartition of respondants",
    "Section 2: About your current use of Blue-Cloud": "Evaluation of Blue Cloud services on a scale of 1 to 4",
    "Section 3: About Blue-Cloud thematic contribution to EOSC": "As a Blue-Cloud stakeholder, what type of value, services and/or type of representation would you be looking for in EOSC? ",
    "Section 4: About Blue-Cloud evolution as an incubator for the EU DTO": "Classification of interest in potential new services.",
    "Section 5: About Blue-Cloud as a contributor to the UN Ocean Decade": "", 
    # Add more sections and subtitles as needed
}
