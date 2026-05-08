# routers/videojuegos.py
# Equipo 1
#
# TAREAS:
#   AGREGAR  -> POST /videojuegos/         agregar un videojuego nuevo
#   AGREGAR  -> GET  /videojuegos/{id}     obtener un videojuego por ID
#   CORREGIR -> GET  /videojuegos/         listar_videojuegos()
#   CORREGIR -> GET  /videojuegos/genero   buscar_por_genero()
#   CORREGIR -> DELETE /videojuegos/{id}   eliminar_videojuego()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datos import videojuegos

router = APIRouter()


class VideoJuegoIn(BaseModel):
    titulo: str
    genero: str
    plataforma: str
    precio_renta: float


@router.get("/")
def listar_videojuegos():
    return [v for v in videojuegos if v["activo"]]


@router.get("/genero")
def buscar_por_genero(genero: str):
    resultados = [v for v in videojuegos if v["activo"] and genero.lower() == v["genero"].lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron juegos del genero '{genero}'")
    return resultados


@router.delete("/{id_videojuego}")
def eliminar_videojuego(id_videojuego: int):
    for v in videojuegos:
        if v["id"] == id_videojuego and v["activo"]:
            v["activo"] = False
            return {"mensaje": f"'{v['titulo']}' eliminado del catalogo.", "id": id_videojuego}
    raise HTTPException(status_code=404, detail="Videojuego no encontrado o ya fue eliminado.")


# EQUIPO 1 - Implementar POST /videojuegos/
# El endpoint debe:
#   1. Recibir un body tipo VideoJuegoIn con: titulo, genero, plataforma, precio_renta
#   2. Validar que titulo no este vacio y precio_renta sea mayor a 0
#      si no cumple, lanzar HTTPException status 400
#   3. Generar id nuevo (max id actual + 1)
#   4. Agregar a videojuegos con disponible=True y activo=True
#   5. Regresar el videojuego creado
#
# @router.post("/")
# def agregar_videojuego(data: VideoJuegoIn):
#     pass


# EQUIPO 1 - Implementar GET /videojuegos/{id}
# El endpoint debe:
#   1. Recibir id_videojuego como parametro en la URL
#   2. Buscar el videojuego por id solo entre los activos
#   3. Si no existe o esta inactivo lanzar HTTPException status 404
#   4. Regresar el diccionario completo del videojuego encontrado
#
# @router.get("/{id_videojuego}")
# def obtener_videojuego(id_videojuego: int):
#     pass


@router.post("/", status_code=201)
def agregar_videojuego(data: VideoJuegoIn):
    if not data.titulo.strip():
        raise HTTPException(status_code=400, detail="El titulo no puede estar vacio.")
    if data.precio_renta <= 0:
        raise HTTPException(status_code=400, detail="El precio_renta debe ser mayor a 0.")
 
    nuevo_id = max((v["id"] for v in videojuegos), default=0) + 1
 
    nuevo = {
        "id": nuevo_id,
        "titulo": data.titulo.strip(),
        "genero": data.genero,
        "plataforma": data.plataforma,
        "precio_renta": data.precio_renta,
        "disponible": True,
        "activo": True,
    }
    videojuegos.append(nuevo)
    return nuevo
 
@router.get("/{id_videojuego}")
def obtener_videojuego(id_videojuego: int):
    # Buscar solo entre activos
    for v in videojuegos:
        if v["id"] == id_videojuego and v["activo"]:
            return v
    raise HTTPException(status_code=404, detail="Videojuego no encontrado o esta inactivo.") 
