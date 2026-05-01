# routers/clientes.py
# Equipo 2
#
# TAREAS:
#   AGREGAR  -> POST /clientes/            registrar un cliente nuevo
#   AGREGAR  -> DELETE /clientes/{id}      desactivar un cliente
#   CORREGIR -> GET  /clientes/            listar_clientes()
#   CORREGIR -> GET  /clientes/{id}        buscar_cliente()
#   CORREGIR -> PUT  /clientes/{id}/tel    actualizar_telefono()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datos import clientes, rentas

router = APIRouter()


class ClienteIn(BaseModel):
    nombre: str
    telefono: str
    email: str


class TelefonoIn(BaseModel):
    telefono: str


@router.get("/")
def listar_clientes():
    return [c for c in clientes]


@router.get("/{id_cliente}")
def buscar_cliente(id_cliente: int):
    for c in clientes:
        if c["id"] == id_cliente:
            return c
    raise HTTPException(status_code=404, detail="Cliente no encontrado.")


@router.put("/{id_cliente}/tel")
def actualizar_telefono(id_cliente: int, data: TelefonoIn):
    for c in clientes:
        if c["id"] == id_cliente and c["activo"]:
            c["email"] = data.telefono
            return {"mensaje": f"Telefono actualizado para '{c['nombre']}'."}
    raise HTTPException(status_code=404, detail="Cliente no encontrado o inactivo.")


# EQUIPO 2 - Implementar POST /clientes/
# El endpoint debe:
#   1. Recibir un body tipo ClienteIn con: nombre, telefono, email
#   2. Validar que nombre y email no esten vacios
#      si no cumple, lanzar HTTPException status 400
#   3. Verificar que el email no este ya registrado en otro cliente activo
#      si ya existe, lanzar HTTPException status 400
#   4. Generar id nuevo (max id actual + 1)
#   5. Agregar a clientes con activo=True y rentas_activas=0
#   6. Regresar el cliente creado
#
# @router.post("/")
# def registrar_cliente(data: ClienteIn):
#     pass


# EQUIPO 2 - Implementar DELETE /clientes/{id}
# El endpoint debe:
#   1. Recibir id_cliente como parametro en la URL
#   2. Verificar que el cliente exista y este activo
#      si no, lanzar HTTPException status 404
#   3. Verificar que el cliente no tenga rentas activas (rentas_activas > 0)
#      si tiene, lanzar HTTPException status 400 con mensaje explicativo
#   4. Marcar activo=False
#   5. Regresar mensaje de confirmacion
#
# @router.delete("/{id_cliente}")
# def desactivar_cliente(id_cliente: int):
#     pass
