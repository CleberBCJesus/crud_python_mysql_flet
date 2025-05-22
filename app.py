import flet as ft

# pagina principal do app
def main(page: ft.Page): # tela
    page.title = "Meu primeiro app com flet" # titulo da janela
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # alinhamento da janela

    texto = ft.Text(value="Olá, mundo!", size=30) # texto
    page.add(texto) # adicionando o texto a janela


ft.app(target=main, view=ft.WEB_BROWSER) # executar o app