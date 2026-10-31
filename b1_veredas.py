import requests
import geopandas as gpd

print("1. VEREDAS DE TUNJA")

url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"
params = {"where": "NOMB_MPIO = 'TUNJA'", "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER", "outSR": "4326", "f": "geojson"}
r = requests.get(url, params=params, timeout=30)
r.raise_for_status()
tunja = gpd.GeoDataFrame.from_features(r.json()["features"], crs=4326)
print(len(tunja), "veredas en Tunja")
print(tunja[["NOMBRE_VER", "CODIGO_VER"]])
print()
print("2. TOP 10 MUNICIPIOS CON MAS VEREDAS")

gdf = gpd.read_file("datos/veredas_boyaca.geojson")
print("Total de veredas en Boyaca:", len(gdf))
por_municipio = gdf.groupby("NOMB_MPIO").size().sort_values(ascending=False)
print(por_municipio.head(10))
print()
print("3. LAS 5 VEREDAS MAS GRANDES")

gdf_m = gdf.to_crs(9377)
gdf_m["area_ha"] = gdf_m.geometry.area / 10_000
top5 = gdf_m.sort_values("area_ha", ascending=False).head(5)
print(top5[["NOMB_MPIO", "NOMBRE_VER", "area_ha"]])

gdf_m.to_file("salidas/veredas_area.gpkg", driver="GPKG")
print("Resultado guardado en salidas/veredas_area.gpkg")