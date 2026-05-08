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
from collections import Counter

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



@router.get("/completo")
def mostrar_dashboard():
    datos = resumen_general()
    ocupacion = porcentaje_ocupacion()
    
    if not rentas:
        juego_top = None
        cliente_top = None
    else:
        juegos_counter = Counter([r["id_videojuego"] for r in rentas])
        juego_id_top = juegos_counter.most_common(1)[0][0]
        juego_top = next((v["titulo"] for v in videojuegos if v["id"] == juego_id_top), None)
        
        clientes_counter = Counter([r["id_cliente"] for r in rentas])
        cliente_id_top = clientes_counter.most_common(1)[0][0]
        cliente_top = next((c["nombre"] for c in clientes if c["id"] == cliente_id_top), None)
        
    datos["juego_mas_rentado"] = juego_top
    datos["cliente_mas_rentas"] = cliente_top
    datos["porcentaje_ocupacion"] = ocupacion["porcentaje"]
    
    return datos


@router.get("/alerta")
def alerta_stock_critico():
    activos = [v for v in videojuegos if v.get("activo", True)]
    total_activos = len(activos)
    
    if total_activos == 0:
        return {"alerta": False, "mensaje": "No hay juegos activos", "disponibilidad": 0.0, "quedan": 0}
        
    disponibles = len([v for v in activos if v.get("disponible", False)])
    porcentaje = (disponibles / total_activos) * 100
    
    if porcentaje < 30:
        return {
            "alerta": True,
            "mensaje": "Alerta de stock crítico",
            "quedan": disponibles,
            "disponibilidad": round(porcentaje, 1)
        }
    else:
        return {
            "alerta": False,
            "mensaje": "Stock saludable",
            "quedan": disponibles,
            "disponibilidad": round(porcentaje, 1)
        }
