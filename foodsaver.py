import customtkinter as ctk
import json
import os
from PIL import Image 

# --- Configurações Globais ---
ARQUIVO_DADOS = "alimentos.json"
alimentos_compartilhados = []

# --- Funções de Manipulação de Dados ---

def carregar_alimentos():
    global alimentos_compartilhados

    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                file_content = f.read()
                if file_content:
                    alimentos_compartilhados = json.loads(file_content)
                else:
                    alimentos_compartilhados = []
        except json.JSONDecodeError:
            print(f"AVISO: O arquivo {ARQUIVO_DADOS} está vazio ou corrompido. Iniciando com lista vazia.")
            alimentos_compartilhados = []
    else:
        alimentos_compartilhados = []

    for i, alimento in enumerate(alimentos_compartilhados):
        if "id" not in alimento:
            alimento["id"] = i + 1000

def salvar_alimentos():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(alimentos_compartilhados, f, indent=4, ensure_ascii=False)

def gerar_novo_id():
    if not alimentos_compartilhados:
        return 1
    return max(alimento.get("id", 0) for alimento in alimentos_compartilhados) + 1

# --- CLASSE PRINCIPAL DO APLICATIVO ---

class FoodSaverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configurações da Janela ---
        self.title("FoodSaver: Compartilhe e Evite o Desperdício")
        self.geometry("420x700")
        self.resizable(False, False)
        self.configure(fg_color="#ECEFF1")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Carrega os dados existentes ao iniciar
        carregar_alimentos()


        # --- Frames para organização ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=15, padx=20, fill="x")

        self.form_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        self.form_frame.pack(pady=10, padx=20, fill="x", ipady=15)

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=12)
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # --- Layout do Cabeçalho ---
        self.title_label = ctk.CTkLabel(self.header_frame, text="FoodSaver",
                                        font=ctk.CTkFont(size=34, weight="bold"),
                                        text_color="#1E88E5")
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Compartilhe alimentos e combata o desperdício!",
                                           font=ctk.CTkFont(size=14), # Alterado para normal
                                           text_color="#607D8B")
        self.subtitle_label.pack(pady=(0, 10))

        ctk.CTkFrame(self.header_frame, height=1, fg_color="#CFD8DC").pack(fill="x", pady=5)

        # --- Layout do Formulário de Cadastro ---
        ctk.CTkLabel(self.form_frame, text="Cadastrar Novo Alimento",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#455A64").pack(pady=10)

        self.txt_nome_alimento = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do Alimento (Ex: Maçãs)",
                                            width=300, height=35, corner_radius=8,
                                            fg_color="#F5F5F5", text_color="#263238",
                                            border_color="#B0BEC5", placeholder_text_color="#78909C")
        self.txt_nome_alimento.pack(pady=5)

        self.txt_quantidade_obs = ctk.CTkEntry(self.form_frame, placeholder_text="Quantidade/Observações (Ex: 3 unidades)",
                                               width=300, height=35, corner_radius=8,
                                               fg_color="#F5F5F5", text_color="#263238",
                                               border_color="#B0BEC5", placeholder_text_color="#78909C")
        self.txt_quantidade_obs.pack(pady=5)

        self.txt_local = ctk.CTkEntry(self.form_frame, placeholder_text="Local (Bairro/Região)",
                                      width=300, height=35, corner_radius=8,
                                      fg_color="#F5F5F5", text_color="#263238",
                                      border_color="#B0BEC5", placeholder_text_color="#78909C")
        self.txt_local.pack(pady=5)

        self.btn_compartilhar = ctk.CTkButton(self.form_frame, text="Compartilhar Alimento",
                                               command=self.adicionar_alimento,
                                               width=300, height=40, corner_radius=8,
                                               font=ctk.CTkFont(size=16, weight="bold"),
                                               fg_color="#2196F3", hover_color="#1976D2", text_color="white")
        self.btn_compartilhar.pack(pady=10)

        ctk.CTkFrame(self.form_frame, height=1, fg_color="#CFD8DC").pack(fill="x", pady=10)

        # --- Layout da Lista de Alimentos ---
        ctk.CTkLabel(self.list_frame, text="Alimentos Compartilhados",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#455A64").pack(pady=10)

        self.update_food_list()

    # --- Métodos de Ação ---

    def exibir_snack_bar(self, mensagem, cor_fundo):
        print(f"Feedback: {mensagem}")

    def adicionar_alimento(self):
        nome = self.txt_nome_alimento.get().strip()
        quantidade = self.txt_quantidade_obs.get().strip()
        local = self.txt_local.get().strip()

        if nome and quantidade and local:
            novo_alimento = {
                "id": gerar_novo_id(),
                "nome": nome,
                "quantidade": quantidade,
                "local": local
            }
            alimentos_compartilhados.append(novo_alimento)

            self.txt_nome_alimento.delete(0, ctk.END)
            self.txt_quantidade_obs.delete(0, ctk.END)
            self.txt_local.delete(0, ctk.END)
            self.txt_nome_alimento.focus_set()

            salvar_alimentos()
            self.update_food_list()

            self.exibir_snack_bar("Alimento compartilhado com sucesso!", "green")
        else:
            self.exibir_snack_bar("Por favor, preencha todos os campos.", "red")

    def remover_alimento(self, alimento_id):
        global alimentos_compartilhados
        alimentos_compartilhados = [
            alimento for alimento in alimentos_compartilhados if alimento["id"] != alimento_id
        ]

        salvar_alimentos()
        self.update_food_list()

        self.exibir_snack_bar("Alimento removido!", "orange")

    def update_food_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not alimentos_compartilhados:
            empty_container = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            empty_container.pack(pady=40)

            empty_icon_label = ctk.CTkLabel(empty_container, text="🧺", font=ctk.CTkFont(size=50))
            empty_icon_label.pack(pady=(0, 10))

            empty_message_label = ctk.CTkLabel(empty_container,
                                                 text="Nenhum alimento compartilhado ainda.\nSeja o primeiro!",
                                                 font=ctk.CTkFont(size=16, weight="normal"), # Alterado para normal
                                                 text_color="#90A4AE",
                                                 wraplength=300)
            empty_message_label.pack()

        else:
            for alimento in alimentos_compartilhados:
                self.create_food_card(alimento)


    def create_food_card(self, alimento):
        card_frame = ctk.CTkFrame(self.list_frame, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#CFD8DC")
        card_frame.pack(fill="x", pady=5, padx=5)

        card_frame.grid_columnconfigure(1, weight=1)

        icon_label = ctk.CTkLabel(card_frame, text="🍎", font=ctk.CTkFont(size=30))
        icon_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")

        name_label = ctk.CTkLabel(card_frame, text=alimento["nome"],
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  text_color="#263238", anchor="w")
        name_label.grid(row=0, column=1, sticky="ew", pady=(5,0))

        qty_location_label = ctk.CTkLabel(card_frame, text=f"Qtde: {alimento['quantidade']} | Local: {alimento['local']}",
                                            font=ctk.CTkFont(size=12), # Alterado para normal
                                            text_color="#607D8B", anchor="w")
        qty_location_label.grid(row=1, column=1, sticky="ew", pady=(0,5))

        remove_button = ctk.CTkButton(card_frame, text="X",
                                      command=lambda: self.remover_alimento(alimento["id"]),
                                      width=30, height=30, corner_radius=5,
                                      fg_color="#EF5350", hover_color="#D32F2F", text_color="white",
                                      font=ctk.CTkFont(size=14, weight="bold"))
        remove_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="e")

# --- Inicia o Aplicativo ---
if __name__ == "__main__":
    app = FoodSaverApp()
    app.mainloop()