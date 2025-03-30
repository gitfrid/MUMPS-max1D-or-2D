# csv data from

# case incidence rate per 1M
# https://immunizationdata.who.int/global/wiise-detail-page/mumps-reported-cases-and-incidence?GROUP=Countries&YEAR=

# vac coverage Official Numbers MMR-containing vaccine 2d Dose
# https://immunizationdata.who.int/global/wiise-detail-page/measles-vaccination-coverage?CODE=ISR&ANTIGEN=MCV2&YEAR=


import pandas as pd
import plotly.graph_objects as go

# Load the data with error handling
vac_coverage_df = pd.read_csv(r"C:\MUMPS-max1D-or-2D\max_vac_coverage_1D_or_2D.csv", encoding='ISO-8859-1',on_bad_lines='skip',delimiter=';')
reported_cases_df = pd.read_csv(r"C:\MUMPS-max1D-or-2D\MUMPS reported cases and incidence 2025-04-03 15-25 RATE.csv", encoding='ISO-8859-1', on_bad_lines='skip', delimiter=';')
year_range_text = "2000-2023"

# Clean column names
vac_coverage_df.columns = vac_coverage_df.columns.str.strip()
reported_cases_df.columns = reported_cases_df.columns.str.strip()

# Set 'Country' as the index for both DataFrames
vac_coverage_df.set_index('Country', inplace=True)
reported_cases_df.set_index('Country', inplace=True)

# Clean country names by stripping extra spaces
vac_coverage_df.index = vac_coverage_df.index.str.strip()
reported_cases_df.index = reported_cases_df.index.str.strip()

# Normalize country names (strip spaces and convert to lowercase) for comparison
vac_coverage_df.index = vac_coverage_df.index.str.lower()
reported_cases_df.index = reported_cases_df.index.str.lower()

# Remove thousands dots and replace commas with periods for all values in the dataframes
vac_coverage_df = vac_coverage_df.replace({r'\.': '', ',': '.'}, regex=True)
reported_cases_df = reported_cases_df.replace({r'\.': '', ',': '.'}, regex=True)

# Convert columns (except the 'Country' index) to numeric, forcing errors to NaN
vac_coverage_df = vac_coverage_df.apply(pd.to_numeric, errors='coerce')
reported_cases_df = reported_cases_df.apply(pd.to_numeric, errors='coerce')

# Filter columns to include only years from 2000 onwards
vac_coverage_df = vac_coverage_df.loc[:, vac_coverage_df.columns.astype(int) >= 2000]
reported_cases_df = reported_cases_df.loc[:, reported_cases_df.columns.astype(int) >= 2000]

# Find common countries between both datasets
common_countries = vac_coverage_df.index.intersection(reported_cases_df.index)

# Sort countries alphabetically
common_countries = sorted(common_countries)

# Create interleaved traces for both datasets
traces = []

for country in common_countries:
    # Truncate the country name for the legend if it's too long
    legend_name = f'{country[:20]}...' if len(country) > 20 else country
    
    # Vaccination coverage trace
    trace_vac_coverage = go.Scatter(
        x=vac_coverage_df.columns,  # Year columns
        y=vac_coverage_df.loc[country],  # Values for this country
        mode='lines',
        name=f'{legend_name} - Vac Cover',  # Truncated name
        yaxis='y2',
        visible=True
    )
    traces.append(trace_vac_coverage)
    
    # Reported cases trace
    trace_reported_cases = go.Scatter(
        x=reported_cases_df.columns,  # Year columns
        y=reported_cases_df.loc[country],  # Values for this country
        mode='lines',
        name=f'{legend_name} - case incidence/1M',  # Truncated name
        yaxis='y1',
        visible=False
    )
    traces.append(trace_reported_cases)

# Layout with two y-axes and legend visibility
layout = go.Layout(
    title=f'MMR vaccination coverage max(1st or 2nd Dose) vs reported case incidence rate Mumps/1M for different countries {year_range_text}',
    xaxis=dict(title='Year'),
    yaxis=dict(
        title='cases/1M',
        side='left',
        tickformat=".0f"
    ),
    yaxis2=dict(
        title='Vaccination Coverage (%)',
        side='right',
        overlaying='y1',
        tickformat=".0f",
        tickmode='auto',
        showgrid=True,
        ticksuffix=' ',
        tickprefix=''
    ),
    showlegend=True,
    legend=dict(
        x=1.05,
        y=1,
        traceorder='normal',  # Default order, traces will already be interleaved
        orientation='v',
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor='black',
        borderwidth=1,
        itemwidth=30,
        itemsizing='trace',
        tracegroupgap=5,
        font=dict(size=10),
    ),
    updatemenus=[
        dict(
            type='dropdown',
            buttons=[
                dict(
                    label='Show Vaccination Coverage',
                    method='update',
                    args=[{'visible': [i % 2 == 0 for i in range(len(traces))]},
                          {'title': f'MMR Vaccination Coverage max(1st or 2nd Dose) coverage {year_range_text}'}]
                ),
                dict(
                    label='Show Reported Cases',
                    method='update',
                    args=[{'visible': [i % 2 != 0 for i in range(len(traces))]},
                          {'title': f'MUMPS Reported Cases Incidence Rate {year_range_text}'}]
                ),
                dict(
                    label='Show Both',
                    method='update',
                    args=[{'visible': [True] * len(traces)},
                          {'title': f'MMR Vaccination Coverage max(1st or 2nd Dose) and Mumps Reported Cases {year_range_text}'}]
                ),
            ],
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.8,
            xanchor='left',
            y=1.1,
            yanchor='top',
        ),
    ]
)

# Create the figure
fig = go.Figure(data=traces, layout=layout)

# Save the plot to an HTML file
fig.write_html(fr"C:\MUMPS-max1D-or-2D\D) MUMPS vaccination_vs_reported_cases_dropdown_{year_range_text}.html")

print("Plot has been saved to 'vaccination_vs_reported_cases.html'.")

# Show the plot (uncomment if you want to display it in a browser)
# fig.show()
