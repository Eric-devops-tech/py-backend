import json
import os

ARQUIVO_DADOS = "dados.json"

pacientes = []
dentistas = []
consultas_agendadas = []

# PERSISTÊNCIA DOS DADOS

def salvar_dados(arquivo=ARQUIVO_DADOS):  # ← valor padrão
    dados = {
        "pacientes": pacientes,
        "dentistas": dentistas,
        "consultas_agendadas": consultas_agendadas
    }
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"❌ Erro ao salvar dados: {e}")


def carregar_dados(arquivo=ARQUIVO_DADOS):  # ← valor padrão
    """Carrega os dados do arquivo JSON para as listas globais."""
    global pacientes, dentistas, consultas_agendadas
    if not os.path.exists(arquivo):
        return
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            pacientes = dados.get("pacientes", [])
            dentistas = dados.get("dentistas", [])
            consultas_agendadas = dados.get("consultas_agendadas", [])
        print("✅ Dados carregados com sucesso.\n")
    except (IOError, json.JSONDecodeError) as e:
        print(f" Erro ao carregar dados: {e}. Iniciando com dados vazios.\n")


# FUNÇÕES AUXILIARES DE VALIDAÇÃO

def obter_inteiro(mensagem):
    """Vai garantir que a entrada do usuário é um número inteiro válido."""
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print(" Entrada inválida. Por favor, digite um número inteiro.")

def obter_float(mensagem):
    """Garante que a entrada do usuário é um número decimal válido."""
    while True:
        try:
            entrada = input(mensagem).replace(',', '.')
            valor = float(entrada)
            return valor
        except ValueError:
            print(" Entrada inválida. Por favor, digite um número (Ex: 1 ou 1.5).")


def obter_tipo_dor(mensagem):
    """Valida e retorna o tipo de dor informado."""
    while True:
        tipo_dor = input(mensagem).lower()
        if tipo_dor in ["leve", "forte", "dente quebrado"]:
            return tipo_dor
        print(" Tipo de dor inválido. Escolha entre 'leve', 'forte' ou 'dente quebrado'.")


def obter_especialidade(mensagem):
    """Valida e retorna a especialidade informada."""
    especialidades_validas = ["prótese", "ortodontia", "odontopediatria", "clínico geral", "cirurgia", "endodontia"]
    while True:
        especialidade = input(mensagem).lower()
        if especialidade in especialidades_validas:
            return especialidade
        print(f" Especialidade inválida. Opções: {', '.join(especialidades_validas)}")


def calcular_urgencia(tipo_dor="leve", tempo_dor=1, renda=1.0, idade=0):  # ← valores padrão
    """Calcula e retorna o nível de urgência do paciente."""
    urgencia = 0
    if tipo_dor == "forte":
        urgencia += 3
    elif tipo_dor == "dente quebrado":
        urgencia += 4
    else:
        urgencia += 1
    if tempo_dor > 7:
        urgencia += 2
    if renda <= 2:
        urgencia += 1
    if 6 <= idade <= 17:
        urgencia += 2
    elif 18 <= idade <= 29:
        urgencia += 1

    return urgencia

# ALGORITMO DE MATCH

def encontrar_melhor_dentista(paciente, priorizar_bairro=True):  # ← valor padrão
    """Encontra o dentista mais compatível e disponível para um paciente."""
    compatibilidade = {
        "leve": ["clínico geral", "odontopediatria"],
        "forte": ["endodontia", "clínico geral"],
        "dente quebrado": ["prótese", "cirurgia"]
    }
    melhor_dentista = None
    maior_pontuacao = -1

    for d in dentistas:
        if d["atendidos"] >= d["max_pacientes"]:
            continue
        pontos = 0
        if d["especialidade"] in compatibilidade.get(paciente["tipo_dor"], []):
            pontos += 2
        if priorizar_bairro and d["bairro"].lower() == paciente["bairro"].lower():
            pontos += 3
        if paciente["urgencia"] >= 5:
            pontos += 5
        if pontos > maior_pontuacao:
            maior_pontuacao = pontos
            melhor_dentista = d
        elif pontos == maior_pontuacao and melhor_dentista and d["atendidos"] < melhor_dentista["atendidos"]:
            melhor_dentista = d

    return melhor_dentista, maior_pontuacao

# CRUD — PACIENTES

def cadastrar_paciente(nome="", idade=0, tipo_dor="leve", tempo_dor=1, renda=1.0, bairro=""):  # ← valores padrão
    """Cadastra um novo paciente."""
    print("\n--- 🦷 Cadastrar Paciente ---")
    nome = input(f"Nome do paciente [{nome or 'obrigatório'}]: ").strip() or nome
    if not nome:
        print(" Nome não pode ser vazio.")
        return

    idade = obter_inteiro(f"Idade [{idade}]: ") if not idade else obter_inteiro(f"Idade [{idade}]: ")
    tipo_dor = obter_tipo_dor(f"Tipo de dor (leve/forte/dente quebrado) [{tipo_dor}]: ")
    tempo_dor = obter_inteiro(f"Há quanto tempo sente a dor (dias) [{tempo_dor}]: ")
    renda = obter_float(f"Renda familiar (em salários mínimos) [{renda}]: ")
    bairro = input(f"Bairro/Cidade [{bairro or 'obrigatório'}]: ").strip() or bairro
    urgencia = calcular_urgencia(tipo_dor, tempo_dor, renda, idade)

    paciente = {
        "nome": nome,
        "idade": idade,
        "tipo_dor": tipo_dor,
        "tempo_dor": tempo_dor,
        "renda": renda,
        "bairro": bairro,
        "urgencia": urgencia
    }
    pacientes.append(paciente)
    salvar_dados()
    print(f"\n Paciente '{nome}' cadastrado com urgência {urgencia}.\n")


def listar_pacientes():
    """Lista todos os pacientes cadastrados."""
    print("\n---  Lista de Pacientes ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    for i, p in enumerate(pacientes):
        print(f"[{i + 1}] Nome: {p['nome']}, Idade: {p['idade']} anos")
        print(f"    Bairro: {p['bairro']}, Renda: {p['renda']} Sal. Mín.")
        print(f"    Dor: {p['tipo_dor']} há {p['tempo_dor']} dias | Urgência: {p['urgencia']}")
        print("-" * 35)
    print(f"Total: {len(pacientes)} paciente(s).\n")
