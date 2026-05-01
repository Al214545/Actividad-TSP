# routers/historial.py
# Equipo 7
#
# TAREAS:
#   AGREGAR  -> GET /historial/{id}        historial de un cliente
#   AGREGAR  -> GET /historial/top         cliente con mas rentas
#   CORREGIR -> GET /historial/vencidas    rentas_vencidas()
#   CORREGIR -> GET /historial/estados     total_rentas_por_estado()

from fastapi import APIRouter, HTTPException
from datetime import date
from datos import rentas, clientes, videojuegos

router = APIRouter()


@router.get("/estados")
def total_rentas_por_estado():
    activas   = len(rentas)
    devueltas = len([r for r in rentas if r["devuelto"]])
    return {"activas": activas, "devueltas": devueltas}


@router.get("/vencidas")
def rentas_vencidas():
    hoy = date.today()
    vencidas = [r for r in rentas if hoy > r["fecha_renta"]]
    return vencidas


# EQUIPO 7 - Implementar GET /historial/{id_cliente}
# El endpoint debe:
#   1. Recibir id_cliente como parametro en la URL
#   2. Verificar que el cliente exista y este activo
#      si no, lanzar HTTPException status 404
#   3. Filtrar todas las rentas (activas y devueltas) de ese cliente
#   4. Para cada renta agregar: titulo del juego y estado (Devuelto/Activo/Vencido)
#   5. Regresar la lista de rentas del cliente
#
# @router.get("/{id_cliente}")
# def historial_cliente(id_cliente: int):
#     pass


# EQUIPO 7 - Implementar GET /historial/top
# El endpoint debe:
#   1. No recibir parametros
#   2. Contar el total de rentas historicas por cada cliente
#   3. Encontrar al cliente con mayor numero de rentas
#   4. Regresar: nombre, telefono y total de rentas del cliente top
#   5. Si no hay rentas lanzar HTTPException status 404
#
# @router.get("/top")
# def cliente_mas_rentas():
#     pass
