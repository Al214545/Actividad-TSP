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

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from datos import videojuegos, clientes, rentas
MULTA_POR_DIA = 20.0

router = APIRouter()


@router.get("/cliente/{id_cliente}")
def buscar_renta_activa(id_cliente: int):
    resultado = [r for r in rentas if r["id_cliente"] == id_cliente and not r["devuelto"]]
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

    if juego:
        juego["disponible"] = True
    if cliente:
        cliente["rentas_activas"] = max(0, cliente["rentas_activas"] - 1)

    return {"mensaje": f"Devolucion procesada: Renta #{id_renta}", "renta": renta}


@router.post("/{id_renta}")
def devolver_videojuego(id_renta: int):
    resultado = procesar_devolucion(id_renta)
    renta = resultado["renta"]

    dias_retraso = (renta["fecha_devolucion"] - renta["fecha_limite"]).days
    tardia = dias_retraso > 0

    if tardia:
        renta["multa"] = dias_retraso * MULTA_POR_DIA

    return {
        "mensaje":      "Devolucion registrada.",
        "tardia":       tardia,
        "dias_retraso": dias_retraso if tardia else 0,
        "multa":        renta["multa"],
        "renta":        renta,
    }


@router.get("/")
def listar_devoluciones():
    resultado = []
    for r in rentas:
        if not r["devuelto"]:
            continue

        cliente = next((c for c in clientes    if c["id"] == r["id_cliente"]),    None)
        juego   = next((v for v in videojuegos if v["id"] == r["id_videojuego"]), None)

        resultado.append({
            "id_renta":         r["id"],
            "cliente":          cliente["nombre"] if cliente else "Desconocido",
            "videojuego":       juego["titulo"]   if juego   else "Desconocido",
            "fecha_renta":      r["fecha_renta"],
            "fecha_limite":     r["fecha_limite"],
            "fecha_devolucion": r["fecha_devolucion"],
            "multa":            r["multa"],
        })

    return resultado
