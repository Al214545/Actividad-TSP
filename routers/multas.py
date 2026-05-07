# routers/multas.py
# Equipo 6
#
# TAREAS:
#   AGREGAR  -> GET /multas/{id}           cobrar multa de una renta
#   AGREGAR  -> GET /multas/pendientes     listar multas pendientes
#   CORREGIR -> GET /multas/calcular/{id}  calcular_multa()
#   CORREGIR -> GET /multas/total          total_multas_cobradas()

from fastapi import APIRouter, HTTPException
from datetime import date
from datos import rentas, clientes, videojuegos, MULTA_POR_DIA

router = APIRouter()


@router.get("/total")
def total_multas_cobradas():
    total = sum(r["multa"] for r in rentas)
    return {"total_multas": total}


@router.get("/calcular/{id_renta}")
def calcular_multa(id_renta: int):
    renta = next((r for r in rentas if r["id"] == id_renta), None)

    if not renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada.")

    fecha_referencia = renta["fecha_devolucion"] if renta["devuelto"] else date.today()
    dias_retraso = (fecha_referencia - renta["fecha_renta"]).days
    if dias_retraso < 0:
        dias_retraso = 0
    multa = dias_retraso * MULTA_POR_DIA
    renta["multa"] = multa

    return {"id_renta": id_renta, "dias_retraso": dias_retraso, "multa": multa}


# EQUIPO 6 - Implementar GET /multas/{id_renta}
# El endpoint debe:
#   1. Recibir id_renta como parametro en la URL
#   2. Llamar a calcular_multa internamente para obtener el monto
#   3. Si la multa es 0 regresar mensaje indicando que no hay multa
#   4. Si hay multa regresar desglose: dias de retraso, monto por dia y total
#
# @router.get("/{id_renta}")
# def cobrar_multa(id_renta: int):
#     pass


# EQUIPO 6 - Implementar GET /multas/pendientes
# El endpoint debe:
#   1. No recibir parametros
#   2. Buscar rentas activas (devuelto=False) que ya pasaron su fecha limite
#   3. Para cada una calcular dias de retraso y multa estimada
#   4. Incluir nombre del cliente y titulo del juego
#   5. Regresar lista con multas pendientes y total acumulado
#
# @router.get("/pendientes")
# def listar_multas_pendientes():
#     pass
