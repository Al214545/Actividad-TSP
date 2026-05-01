# RentaVG - Sistema de Renta de Videojuegos
Practica TSP - Metricas del Software - UACJ 2026

## Setup

```bash
git clone https://github.com/Al214545/Actividad-TSP.git
cd Actividad-TSP
```

Crea y activa el entorno virtual:

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Levanta el servidor:

```bash
uvicorn main:app --reload
```

Abre en el navegador:

```
http://127.0.0.1:8000/docs
```

## Estructura

```
Actividad-TSP/
├── main.py          <- punto de entrada (NO modificar)
├── datos.py         <- datos en memoria (NO modificar)
├── requirements.txt
└── routers/
    ├── videojuegos.py    <- Equipo 1
    ├── clientes.py       <- Equipo 2
    ├── rentas.py         <- Equipo 3
    ├── devoluciones.py   <- Equipo 4
    ├── disponibilidad.py <- Equipo 5
    ├── multas.py         <- Equipo 6
    ├── historial.py      <- Equipo 7
    ├── reportes.py       <- Equipo 8
    └── dashboard.py      <- Equipo 9
```

## Asignacion por equipo

| Equipo | Archivo | Endpoints a implementar |
|--------|---------|------------------------|
| 1 | videojuegos.py | POST /videojuegos/ \| GET /videojuegos/{id} |
| 2 | clientes.py | POST /clientes/ \| DELETE /clientes/{id} |
| 3 | rentas.py | POST /rentas/ \| GET /rentas/cliente/{id} |
| 4 | devoluciones.py | POST /devoluciones/{id} \| GET /devoluciones/ |
| 5 | disponibilidad.py | GET /disponibilidad/ \| GET /disponibilidad/rentados |
| 6 | multas.py | GET /multas/{id} \| GET /multas/pendientes |
| 7 | historial.py | GET /historial/{id} \| GET /historial/top |
| 8 | reportes.py | GET /reportes/top \| GET /reportes/plataformas |
| 9 | dashboard.py | GET /dashboard/completo \| GET /dashboard/alerta |

## Reglas

- Solo modificar tu archivo en routers/
- No tocar main.py, datos.py ni archivos de otros equipos
- Probar cada endpoint en /docs antes de hacer commit
- Formato de commits: feat: descripcion o fix: descripcion

```bash
git add routers/tuarchivo.py
git commit -m "feat: implementar endpoint nombre"
git push origin equipo-N
```

- Al terminar, abrir un Pull Request de equipo-N a main

Equipo supervisor: Alan Alejandro - UACJ 2026
