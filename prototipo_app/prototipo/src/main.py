import flet as ft

def main(page: ft.Page):
    page.title = "Red Neuronal"
    page.bgcolor = ft.Colors.AMBER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    x1, x2 = 1, -1
    w1, w2 = 0.7, 0.5
    
    y = x1 * w1 + x2 * w2

    if y > 0:
        color = ft.Colors.GREEN
        estado = " Neurona activa"
    else:
        color = ft.Colors.RED
        estado = "Neurona inactiva"

    texto_estado = ft.Text(
        estado,
        size=26,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD
    )

    circulo_neurona = ft.Container(
        width =200,
        height=200,
        bgcolor=color,
        border_radius=100,
        alignment=ft.MainAxisAlignment.CENTER,
        shadow=ft.BoxShadow(blur_radius=20, color=color)
    )
    
    page.add(texto_estado, circulo_neurona)

ft.app(target=main)