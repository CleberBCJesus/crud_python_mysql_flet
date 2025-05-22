import flet as ft

def main(page: ft.Page):
    page.title = "Exemplo com Column e Row"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    row_exemplo = ft.Row(
        controls=[
            ft.Text("Item 1"),
            ft.Text("Item 2"),
            ft.Text("Item 3"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    column_exemplo = ft.Column(
        controls=[
            ft.Text("Linha 1"),
            ft.Text("Linha 2"),
            ft.Text("Linha 3"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    container_row = ft.Row(
        controls=[
            ft.Container(content=ft.Text("A"), bgcolor="red", expand=1),
            ft.Container(content=ft.Text("B"), bgcolor="green", expand=1)
        ]
    )

    page.add(
        ft.Text("Exemplo de Row e Column", size=24, weight=ft.FontWeight.BOLD),
        container_row,
        row_exemplo,
        column_exemplo
    )

ft.app(target=main, view=ft.WEB_BROWSER)
