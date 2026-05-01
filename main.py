# main.py - Punto de entrada de la aplicacion
# No modificar este archivo

from fastapi import FastAPI
from routers import videojuegos, clientes, rentas, devoluciones, disponibilidad, multas, historial, reportes, dashboard

app = FastAPI(
    title="RentaVG - Sistema de Renta de Videojuegos",
    description="Practica TSP - Metricas del Software - UACJ 2026",
    version="1.0.0"
)

app.include_router(videojuegos.router,    prefix="/videojuegos",    tags=["Equipo 1 - Videojuegos"])
app.include_router(clientes.router,       prefix="/clientes",       tags=["Equipo 2 - Clientes"])
app.include_router(rentas.router,         prefix="/rentas",         tags=["Equipo 3 - Rentas"])
app.include_router(devoluciones.router,   prefix="/devoluciones",   tags=["Equipo 4 - Devoluciones"])
app.include_router(disponibilidad.router, prefix="/disponibilidad", tags=["Equipo 5 - Disponibilidad"])
app.include_router(multas.router,         prefix="/multas",         tags=["Equipo 6 - Multas"])
app.include_router(historial.router,      prefix="/historial",      tags=["Equipo 7 - Historial"])
app.include_router(reportes.router,       prefix="/reportes",       tags=["Equipo 8 - Reportes"])
app.include_router(dashboard.router,      prefix="/dashboard",      tags=["Equipo 9 - Dashboard"])

@app.get("/", tags=["General"])
def root():
    return {"mensaje": "RentaVG API corriendo. Visita /docs para ver los endpoints."}
