from urllib.parse import urlparse
import flet as ft

GUINDA = "#800020"
BLANCO = "WHITE"
AZUL = "#001F3F"
CYAN = "#00E8FF"

def to_raw_github(url: str) -> str:
    if not url:
        return url
    p = urlparse(url)
    if "github.com" in p.netloc and "/blob/" in p.path:
        parts = p.path.strip("/").split("/")
        if len(parts) >= 5 and parts[2] == "blob":
            user, repo, _, branch, *rest = parts
            return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/" + "/".join(rest)
    return url

# Lista de tuplas (route, título, imagen, audio)
ROUTES = [
    ("/intro","Introducción",
    "https://www.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/intro.gif",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/intro.mp3"),

    ("p1","Paso 1",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/1.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/1.mp3"),

    ("p2","Paso 2",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/2.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/2.mp3"),

    ("p3","Paso 3",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/3.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/3.mp3"),

    ("p4","Paso 4",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/4.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/4.mp3"),

    ("p5","Paso 5",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/5.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/5.mp3"),

    ("p6","Paso 6",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/6.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/6.mp3"),

    ("p7","Paso 7",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/7.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/7.mp3"),

    ("p8","Paso 8",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/blob/1.2/8.png", # se normaliza abajo
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/8.mp3"),

    ("p9","Paso 9",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/9.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/9.mp3"),

    ("p10","Paso 10",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/refs/heads/1.2/10.png",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/10.mp3"),

    ("/cierre","Cierre",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/cierre.gif",
    "https://raw.githubusercontent.com/Prof-Luis1986/Procyctos_3roB/1.2/cierre.mp3"),
]

ROUTES = [(r,t,to_raw_github(img),aud) for (r,t,img,aud) in ROUTES]
ROUTE_INDEX = {r:i for i,(r,*_rest) in enumerate(ROUTES)}

def main(page: ft.Page):
    page.title = "🧠 Audio Makey Makey"
    page.bgcolor = AZUL
    page.padding = 0
    page.spacing = 0

    # Estática
    indice_actual = 0
    reproduciendo = True

    # Audio (ft.Audio aún existe en 0.28)
    audio = ft.Audio(src=ROUTES[0][3], autoplay=True, volume=1.0)
    page.overlay.append(audio)

    # Header guía
    header = ft.Container(
        bgcolor=GUINDA,
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.MUSEUM, color=BLANCO, size=40),
                ft.Text("MUSEO DE LA INFORMÁTICA – CETis 50",
                        size=20, color=BLANCO, weight=ft.FontWeight.BOLD),
            ],
        ),
    )

    # UI principal
    titulo = ft.Text(ROUTES[0][1], size=36, weight=ft.FontWeight.BOLD, color=CYAN, text_align=ft.TextAlign.CENTER)
    contador = ft.Text(f"1/{len(ROUTES)}", size=16, color=GUINDA, text_align=ft.TextAlign.CENTER)
    imagen = ft.Image(src=ROUTES[0][2], height=440, fit=ft.ImageFit.CONTAIN, gapless_playback=True, border_radius=10)

    instrucciones = ft.Container(
        bgcolor=GUINDA,
        padding=10, border_radius=10, border=ft.border.all(2, GUINDA),
        content=ft.Row(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6,
            controls=[
                ft.Text("🎧 CONTROLES MAKEY MAKEY", size=18, weight=ft.FontWeight.BOLD, color=GUINDA),
                ft.Text(
                    "▼/▶ = Siguiente    ▲/◀ = Anterior    Espacio = Play/Pausa    • H = Inicio    • C = Cierre    • R = Repetir",
                    size=12, color="#B6E2AA", text_align=ft.TextAlign.CENTER
                ),
            ],
        ),
    )

    page.add(
        header,
        ft.Container(
            expand=True, padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    titulo, contador, imagen, ft.Container(height=6),
                    instrucciones,
                ],
            ),
        ),
    )

    # Helpers
    def cargar_por_indice(i: int):
        nonlocal indice_actual, reproduciendo
        indice_actual = max(0, min(i, len(ROUTES)-1))
        route, titulo_text, img_url, aud_url = ROUTES[indice_actual]
        titulo.value = titulo_text
        contador.value = f"{indice_actual+1}/{len(ROUTES)}"
        imagen.src = img_url
        audio.src = aud_url
        page.update()
        audio.play()
        reproduciendo = True

    def go_route(route: str):
        i = ROUTE_INDEX.get(route, 0)
        page.go(route)
        cargar_por_indice(i)

    # Routing
    def route_change(e: ft.RouteChangeEvent):
        i = ROUTE_INDEX.get(e.route, 0)
        cargar_por_indice(i)

    page.on_route_change = route_change

    # Navegación por teclas (comparación exacta para Flet 0.28)
    def on_key(e: ft.KeyboardEvent):
        nonlocal indice_actual, reproduciendo
        k = e.key

        # Siguiente
        if k in ("Arrow Down", "Arrow Right", "s", "S", "d", "D"):
            if indice_actual < len(ROUTES)-1:
                go_route(ROUTES[indice_actual+1][0])

        # Anterior
        elif k in ("Arrow Up", "Arrow Left", "w", "W", "a", "A"):
            if indice_actual > 0:
                go_route(ROUTES[indice_actual-1][0])

        # Play/Pausa
        elif k == " " or k == "Space":
            if reproduciendo:
                audio.pause(); reproduciendo = False
            else:
                audio.play(); reproduciendo = True

        # Inicio / Cierre
        elif k in ("h", "H"):
            go_route("/intro")
        elif k in ("c", "C"):
            go_route("/cierre")

        # Repetir
        elif k in ("r", "R"):
            curr = audio.src
            audio.src = None
            page.update()
            audio.src = curr
            page.update()
            audio.play()
            reproduciendo = True

    page.on_keyboard_event = on_key

    # Ruta inicial
    page.go("/intro")

    print("🟢 App iniciada (Flet 0.28, routes + Makey Makey).")
    print(f"🔊 Audio inicial: {ROUTES[0][3]}")

if __name__ == "__main__":
    ft.app(target=main)
