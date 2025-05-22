import flet as ft

def main(page: ft.Page):
    page.title = "Aula 2 - Interatividade" # titulo da página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # alinhamento da página

    nome_input = ft.TextField(label="Digite seu nome", width=300) # cria um campo para o usuário digitar
    sobrenome_input = ft.TextField(label="Digite seu sobrenome", width=300)
    saudacao_texto = ft.Text(value="", size=24) # label em branco

    def botao_clicado(evento): # evento ao clicar o botão
        nome = nome_input.value # recebendo o nome do input
        sobrenome = sobrenome_input.value # recebendo o sobrenome
        saudacao_texto.value = f"Olá, {nome} {sobrenome}!" # label recebe o nome
        page.update()  # Atualiza a interface

    botao = ft.ElevatedButton(text="Dizer olá", on_click=botao_clicado) # botão

    page.add(nome_input,sobrenome_input,botao, saudacao_texto) # adiciona os elementos gráficos na página

ft.app(target=main, view=ft.WEB_BROWSER) # executa o app


# Usuário digita algo no TextField

# Clica no botão

# A função botao_clicado() é chamada

# Essa função pega o texto digitado e atualiza o Text

# A tela é atualizada com page.update()

