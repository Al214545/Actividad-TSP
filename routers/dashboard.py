# routers/dashboard.py
# Equipo 9
#
# TAREAS:
#   AGREGAR  -> GET /dashboard/completo    dashboard con toda la info
#   AGREGAR  -> GET /dashboard/alerta      alerta de stock critico
#   CORREGIR -> GET /dashboard/            resumen_general()
#   CORREGIR -> GET /dashboard/ocupacion   porcentaje_ocupacion()

from fastapi import APIRouter
from datetime import date
from datos import videojuegos, clientes, rentas

router = APIRouter()

@router.get("/ocupacion")
def porcentaje_ocupacion():
    activos  = [v for v in videojuegos if v["activo"]]
    total    = len(activos)
    rentados = len([v for v in activos if not v["disponible"]])
    if total == 0:
        return {"porcentaje": 0}
    porcentaje = (rentados / total) * 100
    return {"porcentaje": round(porcentaje, 1), "rentados": rentados, "total": total}


@router.get("/")
def resumen_general():
    total_clientes    = len([c for c in clientes if c["activo"]])
    total_disponibles = len([v for v in videojuegos if v["activo"] and v["disponible"]])
    rentas_activas    = len([r for r in rentas if not r["devuelto"]])
    rentas_vencidas   = len([r for r in rentas if not r["devuelto"] and date.today() > r["fecha_limite"]])

    return {
        "clientes_activos":  total_clientes,
        "juegos_disponibles": total_disponibles,
        "rentas_activas":    rentas_activas,
        "rentas_vencidas":   rentas_vencidas,
    }



# EQUIPO 9 - Implementar GET /dashboard/completo
# El endpoint debe:
#   1. No recibir parametros
#   2. Llamar a resumen_general() internamente para obtener los datos base
#   3. Agregar: el juego mas rentado (top 1) y el cliente con mas rentas historicas
#   4. Agregar el porcentaje de ocupacion actual
#   5. Regresar todo en un solo objeto JSON
#
# @router.get("/completo")
# def mostrar_dashboard():
#     pass


# EQUIPO 9 - Implementar GET /dashboard/alerta
# El endpoint debe:
#   1. No recibir parametros
#   2. Calcular el porcentaje de juegos activos que estan disponibles
#   3. Si menos del 30% esta disponible, regresar alerta=True con cuantos quedan
#   4. Si no hay stock critico, regresar alerta=False con mensaje positivo
#   5. Incluir el porcentaje actual de disponibilidad en la respuesta
#
# @router.get("/alerta")
# def alerta_stock_critico():
#     pass
