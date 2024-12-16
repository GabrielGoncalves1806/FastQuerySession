import subprocess
import flet as ft
import os 

def get_sessions():
    """Executa o comando query session e retorna a saída formatada."""
    try:
        result = subprocess.run(["query", "session"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        sessions = []
        
        for line in lines[1:]:  # Ignorando o cabeçalho
            parts = line.split()
            
            if len(parts) >= 4:  # Certificando-se de que há dados suficientes na linha
                session_id = parts[2]  # ID da sessão
                user = parts[1]  # Nome do usuário
                sessions.append({"user":user,"id":session_id})
        return sessions
    except Exception as e:
        print(f"Erro ao executar query session: {e}")
        return []
    
class QuerySession():
    def __init__(self,page:ft.Page):
        self.page = page
        self.page.title = "Query session"
        self.page.theme_mode = "dark"
        self.page.scroll = True
        self.sessions_list = ft.Column()

        self.update_list()
        self.page.views.append(self.get_controls())
        self.page.update()

    def refresh(self,e):
        self.sessions_list.controls.clear()
        self.update_list()

    def handle_close(self,e):
        self.shadow_dialog.open = False
        self.page.update()

    def shadow(self,e):
        os.system(f"mstsc.exe /shadow:{e.control.data} /control")
    
    def noconsent_dialog(self,e):
        self.shadow_dialog = ft.AlertDialog(
            title=ft.Text("Sombra sem consentimento",weight="bold"),
            content=ft.Text("Dejesa realmente conectar nessa sessão sem o consentimento do usuário?"),
            actions=[
                ft.ElevatedButton(text="Sim",data=e.control.data,on_click=self.shadow_noconsent),
                ft.ElevatedButton(text="Não",on_click=self.handle_close)
            ]
        )
        self.page.overlay.append(self.shadow_dialog)
        
        self.shadow_dialog.open = True
        self.page.update()

    def shadow_noconsent(self,e):
        os.system(f"mstsc.exe /shadow:{e.control.data} /control /noconsentprompt")
        
            
    def update_list(self,e=None):
        sessions = get_sessions()
        self.sessions_list.controls.clear()
        print(e)
        if e is not None:
            for session in sessions:
                if e.data in session["user"].lower():
                    self.sessions_list.controls.append(
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(f"Usuário: {session["user"]}"),
                                    ft.Text(f"ID da sessão: {session["id"]}"),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                "Sombra",
                                                on_click=self.shadow,
                                                data=session["id"],
                                            ),
                                            ft.ElevatedButton(
                                                "Sombra sem consentimento",
                                                on_click=self.noconsent_dialog,
                                                data=session["id"],
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            padding=10,
                            margin=5,
                            border=ft.border.all(1),
                            border_radius=10,
                            expand=True,
                        )
                    )
        else:
            for session in sessions:
                self.sessions_list.controls.append(
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f"Usuário: {session["user"]}"),
                                        ft.Text(f"ID da sessão: {session["id"]}"),
                                        ft.Row(
                                            controls=[
                                                ft.ElevatedButton(
                                                    "Sombra",
                                                    on_click=self.shadow,
                                                    data=session["id"],
                                                ),
                                                ft.ElevatedButton(
                                                    "Sombra sem consentimento",
                                                    on_click=self.noconsent_dialog,
                                                    data=session["id"],
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                padding=10,
                                margin=5,
                                border=ft.border.all(1),
                                border_radius=10,
                                expand=True,
                            )
                        )
        self.page.update()   

    def get_controls(self):
        return ft.View(
            route='/home',
            scroll=True,
            controls=[
                ft.Row(
                    [
                        ft.TextField(label="Digite o nome do usuário",on_submit=self.update_list),
                        ft.IconButton(icon=ft.Icons.REFRESH,on_click=self.refresh,tooltip="Atualizar lista")
                    ]
                ),
                self.sessions_list
            ]
        )

def main(page:ft.Page):
    QuerySession(page)
ft.app(target=main)
