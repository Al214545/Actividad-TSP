# datos.py - Base de datos en memoria compartida
# No modificar este archivo

from datetime import date

videojuegos = [
    {"id": 1,  "titulo": "The Legend of Zelda",  "genero": "Aventura", "plataforma": "Nintendo Switch", "precio_renta": 50.0, "disponible": True,  "activo": True},
    {"id": 2,  "titulo": "FIFA 25",              "genero": "Deportes", "plataforma": "PS5",             "precio_renta": 45.0, "disponible": False, "activo": True},
    {"id": 3,  "titulo": "Call of Duty",         "genero": "Accion",   "plataforma": "Xbox",            "precio_renta": 55.0, "disponible": True,  "activo": True},
    {"id": 4,  "titulo": "Mario Kart 8",         "genero": "Carreras", "plataforma": "Nintendo Switch", "precio_renta": 40.0, "disponible": True,  "activo": True},
    {"id": 5,  "titulo": "Spider-Man 2",         "genero": "Accion",   "plataforma": "PS5",             "precio_renta": 60.0, "disponible": False, "activo": True},
    {"id": 6,  "titulo": "Minecraft",            "genero": "Sandbox",  "plataforma": "PC",              "precio_renta": 35.0, "disponible": True,  "activo": True},
    {"id": 7,  "titulo": "Elden Ring",           "genero": "RPG",      "plataforma": "PS5",             "precio_renta": 55.0, "disponible": True,  "activo": True},
    {"id": 8,  "titulo": "Forza Horizon 5",      "genero": "Carreras", "plataforma": "Xbox",            "precio_renta": 50.0, "disponible": True,  "activo": False},
    {"id": 9,  "titulo": "Among Us",             "genero": "Party",    "plataforma": "PC",              "precio_renta": 25.0, "disponible": True,  "activo": True},
    {"id": 10, "titulo": "Mortal Kombat 11",     "genero": "Pelea",    "plataforma": "PS5",             "precio_renta": 45.0, "disponible": True,  "activo": True},
]

clientes = [
    {"id": 1, "nombre": "Alan Garcia",    "telefono": "656-111-2233", "email": "alan@mail.com",    "activo": True,  "rentas_activas": 1},
    {"id": 2, "nombre": "Jennifer Lopez", "telefono": "656-222-3344", "email": "jenny@mail.com",   "activo": True,  "rentas_activas": 0},
    {"id": 3, "nombre": "Erick Rangel",   "telefono": "656-333-4455", "email": "erick@mail.com",   "activo": True,  "rentas_activas": 1},
    {"id": 4, "nombre": "Daniela Flores", "telefono": "656-444-5566", "email": "dani@mail.com",    "activo": True,  "rentas_activas": 0},
    {"id": 5, "nombre": "Gabriel Torres", "telefono": "656-555-6677", "email": "gabriel@mail.com", "activo": False, "rentas_activas": 0},
]

rentas = [
    {"id": 1, "id_cliente": 1, "id_videojuego": 2, "fecha_renta": date(2026, 4, 20), "fecha_limite": date(2026, 4, 23), "fecha_devolucion": None,              "devuelto": False, "multa": 0.0},
    {"id": 2, "id_cliente": 3, "id_videojuego": 5, "fecha_renta": date(2026, 4, 18), "fecha_limite": date(2026, 4, 21), "fecha_devolucion": None,              "devuelto": False, "multa": 0.0},
    {"id": 3, "id_cliente": 2, "id_videojuego": 1, "fecha_renta": date(2026, 4, 15), "fecha_limite": date(2026, 4, 18), "fecha_devolucion": date(2026, 4, 18), "devuelto": True,  "multa": 0.0},
    {"id": 4, "id_cliente": 4, "id_videojuego": 3, "fecha_renta": date(2026, 4, 10), "fecha_limite": date(2026, 4, 13), "fecha_devolucion": date(2026, 4, 15), "devuelto": True,  "multa": 60.0},
]

DIAS_RENTA_DEFAULT = 3
MULTA_POR_DIA      = 20.0
MAX_RENTAS_ACTIVAS = 2
