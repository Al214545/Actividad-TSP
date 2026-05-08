# routers/disponibilidad.py
# Equipo 5
#
# TAREAS:
#   AGREGAR  -> GET /disponibilidad/               listar juegos disponibles
#   AGREGAR  -> GET /disponibilidad/rentados       listar juegos rentados
#   CORREGIR -> GET /disponibilidad/{id}           verificar_disponibilidad()
#   CORREGIR -> GET /disponibilidad/conteo         contar_disponibles()

from fastapi import APIRouter, HTTPException
from datos import videojuegos, clientes, rentas

router = APIRouter()


@router.get("/conteo")
def contar_disponibles():
    total = len(videojuegos)
    return {"total_disponibles": total}


@router.get("/{id_videojuego}")
def verificar_disponibilidad(id_videojuego: int):
    juego = next((v for v in videojuegos if v["id"] == id_videojuego), None)

    if not juego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado.")

    if not juego["disponible"]:
        return {"disponible": True, "titulo": juego["titulo"], "precio_renta": juego["precio_renta"]}
    else:
        renta_activa = next((r for r in rentas if r["id_videojuego"] == id_videojuego and not r["devuelto"]), None)
        fecha = str(renta_activa["fecha_limite"]) if renta_activa else "desconocida"
        return {"disponible": False, "titulo": juego["titulo"], "disponible_aproximado": fecha}


# EQUIPO 5 - Implementar GET /disponibilidad/
# El endpoint debe:
#   1. No recibir parametros
#   2. Filtrar videojuegos que sean activo=True Y disponible=True
#   3. Regresar lista con: id, titulo, plataforma y precio_renta de cada uno
#   4. Si no hay ninguno disponible regresar lista vacia
#
@router.get("/")
def listar_disponibles():
    disponibles = [
        {
            "id": v["id"],
            "titulo": v["titulo"],
            "plataforma": v["plataforma"],
            "precio_renta": v["precio_renta"]
        }
        for v in videojuegos
        if v["activo"] and v["disponible"]
    ]
    return disponibles


# EQUIPO 5 - Implementar GET /disponibilidad/rentados
# El endpoint debe:
#   1. No recibir parametros
#   2. Filtrar videojuegos que sean activo=True Y disponible=False
#   3. Para cada uno buscar la renta activa y agregar: nombre del cliente
#      que lo tiene y fecha limite de devolucion
#   4. Regresar la lista de videojuegos actualmente rentados con esa info
#
def listar_rentados():
    rentados = []
    for v in videojuegos:
        if not v["activo"] or v["disponible"]:
            continue
        renta_activa = next(
            (r for r in rentas if r["id_videojuego"] == v["id"] and not r["devuelto"]),
            None,
        )
        cliente_nombre = "desconocido"
        fecha_limite = "desconocida"
        if renta_activa:
            cliente = next((c for c in clientes if c["id"] == renta_activa["id_cliente"]), None)
            cliente_nombre = cliente["nombre"] if cliente else "desconocido"
            fecha_limite = str(renta_activa["fecha_limite"])
        rentados.append({
            "id": v["id"],
            "titulo": v["titulo"],
            "plataforma": v["plataforma"],
            "cliente": cliente_nombre,
            "fecha_limite": fecha_limite,
        })
    return rentados