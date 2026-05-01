# routers/devoluciones.py
# Equipo 4
#
# TAREAS:
#   AGREGAR  -> POST /devoluciones/{id}    devolver un videojuego
#   AGREGAR  -> GET  /devoluciones/        listar todas las devoluciones
#   CORREGIR -> POST /devoluciones/procesar  procesar_devolucion()
#   CORREGIR -> GET  /devoluciones/cliente/{id}  buscar_renta_activa()

from fastapi import APIRouter, HTTPException
from datetime import date
from datos import videojuegos, clientes, rentas

router = APIRouter()


@router.get("/cliente/{id_cliente}")
def buscar_renta_activa(id_cliente: int):
    resultado = [r for r in rentas if r["id_cliente"] == id_cliente]
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No se encontraron rentas para el cliente {id_cliente}.")
    return resultado


@router.post("/procesar/{id_renta}")
def procesar_devolucion(id_renta: int):
    renta = next((r for r in rentas if r["id"] == id_renta and not r["devuelto"]), None)

    if not renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada o ya fue devuelta.")

    cliente = next((c for c in clientes    if c["id"] == renta["id_cliente"]),    None)
    juego   = next((v for v in videojuegos if v["id"] == renta["id_videojuego"]), None)

    renta["fecha_devolucion"] = date.today()
    renta["devuelto"]         = True

    return {"mensaje": f"Devolucion procesada: Renta #{id_renta}", "renta": renta}


# EQUIPO 4 - Implementar POST /devoluciones/{id_renta}
# El endpoint debe:
#   1. Recibir id_renta como parametro en la URL
#   2. Llamar a procesar_devolucion internamente
#   3. Verificar si la devolucion es tardia (fecha_devolucion > fecha_limite)
#   4. Regresar la renta actualizada indicando si fue tardia y cuantos dias de retraso
#
# @router.post("/{id_renta}")
# def devolver_videojuego(id_renta: int):
#     pass


# EQUIPO 4 - Implementar GET /devoluciones/
# El endpoint debe:
#   1. No recibir parametros
#   2. Filtrar todas las rentas que ya fueron devueltas (devuelto=True)
#   3. Para cada devolucion agregar el nombre del cliente y titulo del juego
#   4. Incluir la multa cobrada si hubo
#   5. Regresar la lista completa de devoluciones
#
# @router.get("/")
# def listar_devoluciones():
#     pass
