analisis_telco.py is a specialized Python module designed for telecommunications market analysis, geospatial intelligence, subscriber segmentation, and interactive data visualization.

It provides robust tools for working with Ookla/speedtest datasets, CRM exports (e.g., Odoo), B2B/B2C classification, market share tracking, latency/throughput distribution analysis, Sankey flow diagrams for churn/migration, and interactive Folium maps.

🛠️ Main Features
Provider Branding Integrity: Standardized hex color scheme mapping for over 60+ Venezuelan and international ISPs/telcos (COLORES_PROVEEDORES).

Dataset Discovery & Inspection: Fast extraction and counting of unique regions, subregions, postal codes, and places.

Smart Geospatial Filtering: Robust filtering by Postal Code (attr_place_postal_code), Subregion, Place Name, or State without losing record types.

B2B vs. B2C Segmentation: Automated regex-based classification derived from contract templates/plans.

Market Share Analytics: Dynamic calculation with automatic top-provider ranking, consolidation of smaller players into "Otros", and custom aggregation levels.

Comparative & Time-Series Visualizations:

Stacked bar plots comparing evolution across months/periods.

Side-by-side multi-region consolidated dashboards.

Embedded Top 5 Provider callouts.

Pie charts for contract types and operational zones.

Performance Metrics:

Throughput distribution (val_download_mbps) via Seaborn grouped bar charts.

Latency distribution (val_latency_min_ms) via Plotly interactive ribbon charts.

Subscriber Migration Analysis: Interactive Plotly Sankey diagrams and target provider inflow/outflow balance sheets using device-level tracking (id_device).

Geospatial Mapping: Interactive Folium maps with toggleable provider layers (toolbox) and auto-fitting map boundaries.

📋 Table of Contents
Installation & Requirements

Module Structure

Quick Start & Common Workflows

1. Discovery & Data Inspection

2. Data Filtering & B2B/B2C Segmentation

3. Market Share Calculation

4. Visualizations & Time-Series Evolution

5. Performance Analytics (Speed & Latency)

6. Migration Tracking (Sankey Diagram)

7. Interactive Geospatial Maps

Color Palette Customization

📦 Installation & Requirements
Ensure you have Python 3.8+ installed along with the following required packages:

Bash
pip install pandas numpy matplotlib seaborn folium plotly
Import the module in your Python script or Jupyter Notebook:

Python
import pandas as pd
import analisis_telco as telco
🏗️ Module Structure
Plaintext
analisis_telco.py
├── COLORES_PROVEEDORES         # Official provider color dictionary
├── 0. Data Inspection           # consultar_regiones(), consultar_subregiones(), consultar_lugares()
├── 1. Data Filtering            # filtrar_por_codigo_postal(), filtrar_clientes(), B2B/B2C filters
├── 2. Market Share Calculations # calcular_marketshare_region(), subregiones(), lugares(), etc.
├── 3. Plots & Visualizations    # Stacked bar charts, pie charts, consolidated dashboards
├── 4. Performance Metrics       # Speed & Latency distribution (Seaborn & Plotly Ribbons)
├── 5. Migration Analysis        # Sankey diagram & target provider inflow/outflow table
└── 6. Interactive Cartography   # Folium map generators with provider toolbox
🚀 Quick Start & Common Workflows
1. Discovery & Data Inspection
Explore available geographical regions or subregions before filtering:

Python
# List all regions with record and unique device counts
regiones = telco.consultar_regiones(df, mostrar_conteo=True)

# Consult subregions within a specific region
subregiones = telco.consultar_subregiones_por_region(df, region="Lara")

# Consult exact city/place names
lugares = telco.consultar_lugares_por_region(df, region="Guarico")
2. Data Filtering & B2B/B2C Segmentation
Filter datasets by postal code or separate commercial (B2B) from residential (B2C) contracts:

Python
# Filter by postal code(s)
df_caracas_central = telco.filtrar_por_codigo_postal(df, codigos_postales=[1010, 1020])

# Separate B2C (Residential) from B2B (Corporate/Dedicated)
df_b2c = telco.filtrar_clientesB2C(df_contratos)
df_b2b = telco.filtrar_clientesB2B(df_contratos)
3. Market Share Calculation
Calculate provider market share percentage for a region, subregion, or list of places:

Python
# Market Share by region
df_ms_lara = telco.calcular_marketshare_region(df, region="Lara")

# Market Share by subregions (returns pivot table and top 5 string summary)
df_ms_subregion, top_5_str = telco.calcular_marketshare_subregionesV2(
    df, 
    subregiones=["Iribarren", "Palavecino"], 
    region="Lara"
)
4. Visualizations & Time-Series Evolution
Compare Market Share across different time periods with embedded Top 5 callouts:

Python
dfs = [df_mes1_pivot, df_mes2_pivot, df_mes3_pivot]
titulos = ["Julio 2026", "Agosto 2026", "Septiembre 2026"]

# Generate evolution stacked bar chart
telco.generar_grafico_evolucion_marketsharev3(
    lista_dfs=dfs,
    lista_titulos=titulos,
    ruta_exportacion="evolucion_marketshare.png"
)

# Consolidated 2-period multi-city dashboard
telco.generar_grafico_consolidadov2(
    dfs_fila1=[df_m1_ccs, df_m1_bqto],
    dfs_fila2=[df_m2_ccs, df_m2_bqto],
    titulos_columnas=["Caracas", "Barquisimeto"],
    titulo_fila1="Periodo Anterior",
    titulo_fila2="Periodo Actual",
    ruta_exportacion="consolidado_periodos.png"
)
5. Performance Analytics (Speed & Latency)
Analyze throughput bins or interactive Plotly latency ribbons:

Python
# Speed distribution bar plot
telco.generar_grafico_distribucion_velocidades(
    df=df_mes,
    region="Lara",
    cantidad_proveedores=5,
    cortes=[0, 100, 300, 600, 10000],
    etiquetas=['<100 Mbps', '100-300 Mbps', '300-600 Mbps', '600+ Mbps'],
    ruta_exportacion="velocidades_lara.png"
)

# Interactive Plotly Latency Ribbon Plot
fig_latencia = telco.generar_grafico_distribucion_latencias(
    df=df_mes,
    region="Capital District",
    cantidad_proveedores=6
)
fig_latencia.show()
6. Migration Tracking (Sankey Diagram)
Track customer churn and migration between service providers between two months:

Python
# Interactive Sankey Diagram
fig_sankey = telco.generar_sankey_migraciones(df_mes_anterior, df_mes_actual)
fig_sankey.show()

# Get tabular breakdown of gains/losses for a target provider
df_migracion_target = telco.obtener_cuadro_migracion_proveedor(
    df_mes_anterior, 
    df_mes_actual, 
    proveedor_objetivo="Thundernet"
)
print(df_migracion_target)
7. Interactive Geospatial Maps
Create dynamic Folium maps with toggleable provider layers:

Python
# Map by Region
mapa_region = telco.generar_mapa_por_region_toolbox(
    df=df,
    region_seleccionada="Lara",
    diccionario_colores=telco.COLORES_PROVEEDORES,
    max_mostrar=8
)
mapa_region.save("mapa_lara.html")
🎨 Color Palette Customization
The module includes a default color palette mapped to major providers (COLORES_PROVEEDORES). You can override or extend colors directly in your script:

Python
custom_colores = telco.COLORES_PROVEEDORES.copy()
custom_colores['MiProveedor'] = '#FF1493'

telco.generar_grafico_barras(df_pivot, titulo="Market Share Custom", diccionario_colores=custom_colores)
📄 License
Internal utility library for Telecom Market Intelligence & Data Analytics.
