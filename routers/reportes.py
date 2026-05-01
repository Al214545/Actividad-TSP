# routers/reportes.py
# Equipo 8
#
# TAREAS:
#   AGREGAR  -> GET /reportes/top          juegos mas rentados
#   AGREGAR  -> GET /reportes/plataformas  reporte por plataforma
#   CORREGIR -> GET /reportes/ingresos     ingresos_totales()
#   CORREGIR -> GET /reportes/promedio     promedio_duracion_renta()

from fastapi import APIRouter
from datos import rentas, videojuegos, MULTA_POR_DIA

router = APIRouter()


@router.get("/promedio")
def promedio_duracion_renta():
    devueltas = [r for r in rentas if r["devuelto"]]
    if not devueltas:
        return {"promedio_dias": 0, "mensaje": "No hay rentas completadas."}
    total_dias = sum((r["fecha_devolucion"] - r["fecha_renta"]).days for r in rentas)
    promedio = total_dias / len(devueltas)
    return {"promedio_dias": round(promedio, 1)}


@router.get("/ingresos")
def ingresos_totales():
    total = 0.0
    for r in rentas:
        juego = next((v for v in videojuegos if v["id"] == r["id_videojuego"]), None)
        if juego and r["fecha_devolucion"]:
            dias = (r["fecha_devolucion"] - r["fecha_renta"]).days
            ingreso = juego["precio_renta"] * dias
            total += ingreso
    return {"ingresos_totales": round(total, 2)}


# EQUIPO 8 - Implementar GET /reportes/top
# El endpoint debe:
#   1. No recibir parametros
#   2. Contar cuantas veces ha sido rentado cada videojuego (activas + pasadas)
#   3. Ordenar de mayor a menor numero de rentas
#   4. Regresar lista con: titulo, plataforma y cantidad de rentas de cada juego
#
# @router.get("/top")
# def juegos_mas_rentados():
#     pass


# EQUIPO 8 - Implementar GET /reportes/plataformas
# El endpoint debe:
#   1. No recibir parametros
#   2. Agrupar los videojuegos activos por plataforma
#   3. Para cada plataforma calcular: total de juegos, disponibles y rentados
#   4. Ordenar de mayor a menor cantidad de juegos
#   5. Regresar un listado con las estadisticas por plataforma
#
# @router.get("/plataformas")
# def reporte_por_plataforma():
#     pass
