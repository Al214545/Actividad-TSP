# routers/rentas.py
# Equipo 3
#
# TAREAS:
#   AGREGAR  -> POST /rentas/              registrar una renta nueva
#   AGREGAR  -> GET  /rentas/cliente/{id}  listar rentas de un cliente
#   CORREGIR -> GET  /rentas/              listar_rentas_activas()
#   CORREGIR -> POST /rentas/procesar      procesar_renta()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
from datos import videojuegos, clientes, rentas, DIAS_RENTA_DEFAULT, MAX_RENTAS_ACTIVAS

router = APIRouter()


class RentaIn(BaseModel):
    id_cliente: int
    id_videojuego: int
    dias: int = DIAS_RENTA_DEFAULT


@router.get("/")
def listar_rentas_activas():
    return [r for r in rentas if not r["devuelto"]]


@router.post("/procesar")
def procesar_renta(data: RentaIn):
    cliente = next((c for c in clientes    if c["id"] == data.id_cliente    and c["activo"]), None)
    juego   = next((v for v in videojuegos if v["id"] == data.id_videojuego and v["activo"]), None)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o inactivo.")
    if not juego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado o inactivo.")
    if not juego["disponible"]:
        raise HTTPException(status_code=400, detail=f"'{juego['titulo']}' no esta disponible.")

    nueva_renta = {
        "id":               len(rentas) + 1,
        "id_cliente":       data.id_cliente,
        "id_videojuego":    data.id_videojuego,
        "fecha_renta":      date.today(),
        "fecha_limite":     date.today() + timedelta(days=data.dias),
        "fecha_devolucion": None,
        "devuelto":         False,
        "multa":            0.0,
    }
    rentas.append(nueva_renta)
    cliente["rentas_activas"] += 1
    juego["disponible"] = False
    return nueva_renta

@router.post("/")
def rentar_videojuego(data: RentaIn):
    if data.dias <= 0 or data.dias > 7:
        raise HTTPException(status_code=400, detail="Dias debe ser mayor a 0 y no mayor a 7.")

    nueva_renta = procesar_renta(data)
    juego = next((v for v in videojuegos if v["id"] == data.id_videojuego), None)
    nueva_renta["precio_total"] = juego["precio_renta"] * data.dias
    return nueva_renta


# EQUIPO 3 - Implementar GET /rentas/cliente/{id_cliente}
# El endpoint debe:
#   1. Recibir id_cliente como parametro en la URL
#   2. Verificar que el cliente exista y este activo
#      si no, lanzar HTTPException status 404
#   3. Filtrar todas las rentas (activas y devueltas) de ese cliente
#   4. Para cada renta agregar el titulo del juego en la respuesta
#   5. Regresar la lista de rentas del cliente
#
@router.get("/cliente/{id_cliente}")
def listar_rentas_cliente(id_cliente: int):
    cliente = next((c for c in clientes if c["id"] == id_cliente and c["activo"]), None)
    
    if not cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente no encontrado o inactivo."
        )
    historial_cliente = []
    
    for renta in rentas:
        if renta["id_cliente"] == id_cliente:
            juego = next((v for v in videojuegos if v["id"] == renta["id_videojuego"]), None)
            
            item = renta.copy()
            item["titulo_juego"] = juego["titulo"] if juego else "Título no disponible"
            
            historial_cliente.append(item)

    return historial_cliente
