# routers/historial.py
# Equipo 7

from fastapi import APIRouter, HTTPException
from datetime import date
from datos import rentas, clientes, videojuegos

router = APIRouter()


@router.get("/estados")
def total_rentas_por_estado():

    activas = len([
        r for r in rentas
        if (
            not r["devuelto"]
            and (
                r["fecha_devolucion"] is None
                or date.today() <= r["fecha_devolucion"]
            )
        )
    ])

    vencidas = len([
        r for r in rentas
        if (
            not r["devuelto"]
            and r["fecha_devolucion"] is not None
            and date.today() > r["fecha_devolucion"]
        )
    ])

    devueltas = len([
        r for r in rentas
        if r["devuelto"]
    ])

    return {
        "activas": activas,
        "vencidas": vencidas,
        "devueltas": devueltas
    }


@router.get("/vencidas")
def rentas_vencidas():

    hoy = date.today()

    vencidas = [
        r for r in rentas
        if (
            not r["devuelto"]
            and r["fecha_devolucion"] is not None
            and hoy > r["fecha_devolucion"]
        )
    ]

    return vencidas


@router.get("/top")
def cliente_mas_rentas():

    if len(rentas) == 0:
        raise HTTPException(
            status_code=404,
            detail="No hay rentas registradas"
        )

    conteo = {}

    # Contar rentas por cliente
    for renta in rentas:

        cliente_id = renta["id_cliente"]

        if cliente_id in conteo:
            conteo[cliente_id] += 1
        else:
            conteo[cliente_id] = 1

    # Obtener cliente top
    top_cliente_id = max(conteo, key=conteo.get)
    total_rentas = conteo[top_cliente_id]

    # Buscar cliente
    cliente = next(
        (
            c for c in clientes
            if c["id"] == top_cliente_id
        ),
        None
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return {
        "nombre": cliente["nombre"],
        "telefono": cliente["telefono"],
        "total_rentas": total_rentas
    }



@router.get("/{id_cliente}")
def historial_cliente(id_cliente: int):

    # Buscar cliente activo
    cliente = next(
        (
            c for c in clientes
            if c["id"] == id_cliente and c["activo"]
        ),
        None
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado o inactivo"
        )

    historial = []

    # Buscar rentas del cliente
    for renta in rentas:

        if renta["id_cliente"] == id_cliente:

            # Buscar videojuego
            juego = next(
                (
                    v for v in videojuegos
                    if v["id"] == renta["id_videojuego"]
                ),
                None
            )

            # Determinar estado
            if renta["devuelto"]:
                estado = "Devuelto"

            elif (
                renta["fecha_devolucion"] is not None
                and date.today() > renta["fecha_devolucion"]
            ):
                estado = "Vencido"

            else:
                estado = "Activo"

            historial.append({
                "id_renta": renta["id"],
                "titulo": juego["titulo"] if juego else "Desconocido",
                "fecha_renta": renta["fecha_renta"],
                "fecha_devolucion": renta["fecha_devolucion"],
                "estado": estado
            })

    return historial