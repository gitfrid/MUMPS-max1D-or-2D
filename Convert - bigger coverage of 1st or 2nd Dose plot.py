import pandas as pd
import plotly.graph_objects as go

# Load the CSV files
file_1D = r"C:\MUMPS-max1D-or-2D\vac coverage 2025-04-03 15-07 UTC 1D.csv"
file_2D = r"C:\MUMPS-max1D-or-2D\MMR vac coverage 2025-04-03 15-07 UTC 2D.csv"

df_1D = pd.read_csv(file_1D, encoding='ISO-8859-1', delimiter=';')
df_2D = pd.read_csv(file_2D, encoding='ISO-8859-1', delimiter=';')

# Ensure country names are stripped of extra spaces and in lowercase for consistency
df_1D['Country'] = df_1D['Country'].str.strip().str.lower()
df_2D['Country'] = df_2D['Country'].str.strip().str.lower()

# Set 'Country' as index for both dataframes
df_1D.set_index('Country', inplace=True)
df_2D.set_index('Country', inplace=True)

# Convert all columns (years) to numeric, handling errors
df_1D = df_1D.apply(pd.to_numeric, errors='coerce')
df_2D = df_2D.apply(pd.to_numeric, errors='coerce')

# Find common countries in both datasets
common_countries = df_1D.index.intersection(df_2D.index)

# Keep only common countries
df_1D = df_1D.loc[common_countries]
df_2D = df_2D.loc[common_countries]

# Compute the correct max coverage following the specified logic
# Apply element-wise function to compare each value
def max_coverage(x, y):
    return x if pd.notna(x) and (pd.isna(y) or x > y) else (y if pd.notna(y) else None)

# Apply the max_coverage function element-wise
df_max_coverage = pd.DataFrame(index=df_1D.index, columns=df_1D.columns)

for country in common_countries:
    df_max_coverage.loc[country] = df_1D.loc[country].combine(df_2D.loc[country], max_coverage)

# Create a single plot for all countries
fig = go.Figure()

for country in common_countries:
    years = df_1D.columns.astype(str)
    values_1D = df_1D.loc[country]
    values_2D = df_2D.loc[country]
    values_max = df_max_coverage.loc[country]
    
    fig.add_trace(go.Scatter(x=years, y=values_1D, mode='lines+markers', name=f'{country} 1D'))
    fig.add_trace(go.Scatter(x=years, y=values_2D, mode='lines+markers', name=f'{country} 2D'))
    fig.add_trace(go.Scatter(x=years, y=values_max, mode='lines+markers', name=f'{country} Max(1D, 2D)'))
    
fig.update_layout(
    title='Vaccination Coverage for All Countries',
    xaxis_title='Year',
    yaxis_title='Coverage (%)',
    xaxis=dict(type='category'),
    template='plotly_white'
)

# Save the plot as an HTML file
output_file = r"C:\MUMPS-max1D-or-2D\max_vac_coverage_all_countries.html"
fig.write_html(output_file)
print(f"Plot saved: {output_file}")

# Save the result to a new CSV file
output_file_csv = r"C:\MUMPS-max1D-or-2D\max_vac_coverage_1D_or_2D.csv"  # Adjust output path if needed
df_max_coverage.to_csv(output_file_csv, sep=';', encoding='utf-8')

print(f"CSV file saved: {output_file_csv}")
