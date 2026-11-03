\# Ejercicio C1 — Comparativa de estándares de servicios geográficos



\*\*Autora:\*\* Daniela Monroy



\## 1. GetCapabilities del WMS del DANE (MGN 2024)



\- \*\*URL:\*\* https://geoportal.dane.gov.co/mparcgis/services/MGN2024/Serv\_CapasMGN\_2024/MapServer/WMSServer?service=WMS\&request=GetCapabilities

\- \*\*Capas publicadas:\*\* 10 (Name 0 a 9; la capa 0 es Manzana)

\- \*\*CRS soportados:\*\* CRS:84, EPSG:4326, EPSG:3857 y EPSG:102100 (alias de 3857)



\## 2. Comparación del JSON: FeatureServer vs OGC API – Features



| Aspecto | FeatureServer (Veredas Boyacá) | OGC API – Features (pygeoapi, lakes) |

|---|---|---|

| Petición | `.../FeatureServer/0/query?where=1=1\&outFields=\*\&resultRecordCount=3\&f=geojson` | `.../collections/lakes/items?f=json\&limit=3` |

| Formato | GeoJSON (`FeatureCollection`) | GeoJSON (`FeatureCollection`) |

| Cada elemento | `geometry` (Polygon) + `properties` (NOMB\_MPIO, NOMBRE\_VER...) | `geometry` (Polygon) + `properties` (name, featureclass...) + `id` |

| Metadatos extra | `exceededTransferLimit` si hay más registros | `numberMatched`, `numberReturned` y `links` (self, next) |



Ambos devuelven JSON navegable, pero OGC API incluye los enlaces de navegación (`next`) dentro de la respuesta, mientras que en el FeatureServer hay que calcular el `resultOffset` a mano.



\## 3. Resumen de estándares



| Estándar | Qué entrega | Cómo se filtra | Cómo se pagina |

|---|---|---|---|

| \*\*WMS\*\* | Imágenes del mapa ya dibujado (PNG, JPEG) | Por capa (`LAYERS`), área (`BBOX`) y estilo (`STYLES`); no filtra atributos de forma estándar | No pagina: cada `GetMap` devuelve una sola imagen del área pedida |

| \*\*WFS\*\* | Geometrías + atributos (GML, GeoJSON) | `BBOX` o filtros OGC (`FILTER`, `CQL\_FILTER` en GeoServer) | `count` (o `maxFeatures`) y `startIndex` |

| \*\*FeatureServer (Esri)\*\* | Geometrías + atributos por REST (JSON, GeoJSON) | `where` (SQL), `geometry` (espacial), `outFields` | `resultRecordCount` y `resultOffset` (máx. \~2000 por petición) |

| \*\*OGC API – Features\*\* | Geometrías + atributos por REST (GeoJSON, HTML) | `bbox`, `datetime` y filtros por propiedad (`?campo=valor`) | `limit` y `offset`, con enlace `next` en la respuesta |



\*\*Conclusión:\*\* WMS y WFS son los estándares clásicos (XML + parámetros KVP y `GetCapabilities`); FeatureServer y OGC API – Features son REST, usan rutas y JSON, y son más fáciles de consumir desde la web.

