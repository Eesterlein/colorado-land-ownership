# Who owns Colorado? - a land ownership analysis with python


# Who Owns Colorado?

This is an interactive data story exploring public vs. private land ownership across Colorado using real parcel data, geospatial analysis, and Python-powered visualizations. Dive into statewide trends and explore a detailed case study of Gunnison County.

# Project Overview

This project visualizes land ownership patterns in Colorado:

Public vs. Private land distribution by county

Ownership breakdown by individuals, trusts, LLCs, and others

A deep dive into Gunnison County with parcel-level data

Tree maps showing where out-of-town property owners come from

# Data & Resources

This project uses publicly available geospatial and tabular data to analyze land ownership in Colorado. The following resources were used:

COMaP Protected Lands – shapefiles for publicly managed and conserved lands
COMaP FeatureServer API - https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0

Colorado Statewide Parcel Composite (2024) - 
Colorado.gov FeatureServer API - https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0

Gunnison Assessor Data – classified parcel-level data with flags for local vs. out-of-town ownership 
Gunnison County Assesors - https://www.gunnisoncounty.org/132/Assessors-Office

Colorado County Boundaries – shapefile from the U.S. Census TIGER dataset
Colorado County Shapefile (TIGER/Line) - https://www2.census.gov/geo/tiger/TIGER2023/COUSUB/tl_2023_08_cousub.zip

Ownership Summaries by County – cleaned CSVs summarizing public vs. private acreage totals

Python Notebooks – for generating all maps, donut charts, bar charts, and treemaps

⚠️ Note on Data Access
The full COMaP protected lands dataset and the U.S. county boundary shapefiles are too large to include directly in this GitHub repository.
To ensure reproducibility without bloating the repo, these files are intended to be accessed programmatically through public APIs or official download portals:

Cleaned and merged CSV summary files

Final analysis-ready files used in the visualizations

These make it easier for others to follow along or extend the analysis without needing to preprocess raw geospatial files.

# Key Insights

62.6% of land in Colorado is privately owned, with the rest held by federal, state, or local agencies.

Gunnison County is 76% public land, yet most private parcels are owned by non-residents.

Out-of-town ownership trends show strong second-home and investment interest from Texas, Florida, and Colorado’s Front Range.

# Tools Used

Python (Pandas, GeoPandas, Plotly, Matplotlib)

Folium / Leaflet.js for interactive mapping

HTML/CSS for layout and presentation

GitHub Pages for hosting

# Data Sources

Colorado Statewide Parcel Composite (2024) - https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0

COMaP - Colorado Ownership, Management, and Protection dataset - https://services.arcgis.com/CnX1n8u40Yn3egci/arcgis/rest/services/COMaP_V202312/FeatureServer

Gunnison County Assessor's Office - https://www.gunnisoncounty.org/132/Assessors-Office

This project was built with the help of ChatGPT & open data from Colorado. 

# Additional Links 

github pages report - [here](https://eesterlein.github.io/colorado-land-ownership/) 
Interactive kaggle report - [here](https://www.kaggle.com/code/elissaesterlein/who-owns-colorado-a-land-ownership-analysis-in-py)


