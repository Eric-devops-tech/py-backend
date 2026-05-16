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

def consultar_paciente():
    """Busca um paciente pelo nome."""
    print("\n--- 🔍 Consultar Paciente ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    termo = input("Digite o nome (ou parte do nome) do paciente: ").strip().lower()
    resultados = [p for p in pacientes if termo in p["nome"].lower()]
    if not resultados:
        print("⚠️ Nenhum paciente encontrado com esse nome.\n")
        return
    print(f"\n{len(resultados)} resultado(s) encontrado(s):")
    for p in resultados:
        print(f"  • {p['nome']} | Idade: {p['idade']} | Bairro: {p['bairro']} | Urgência: {p['urgencia']}")
    print()


def editar_paciente():
    """Edita os dados de um paciente existente."""
    print("\n--- ✏ Editar Paciente ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    listar_pacientes()
    while True:
        escolha = obter_inteiro("Número do paciente a editar (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(pacientes):
            break
        print(" Número inválido. Tente novamente.")

    p = pacientes[escolha]
    print(f"\nEditando: {p['nome']} (pressione Enter para manter o valor atual)\n")

    nome = input(f"Nome [{p['nome']}]: ").strip()
    if nome:
        p["nome"] = nome

    entrada_idade = input(f"Idade [{p['idade']}]: ").strip()
    if entrada_idade:
        try:
            p["idade"] = int(entrada_idade)
        except ValueError:
            print(" Idade inválida, mantendo valor anterior.")

    print(f"Tipo de dor atual: {p['tipo_dor']}")
    nova_dor = input("Novo tipo de dor (leve/forte/dente quebrado) ou Enter para manter: ").strip().lower()
    if nova_dor in ["leve", "forte", "dente quebrado"]:
        p["tipo_dor"] = nova_dor

    entrada_tempo = input(f"Tempo de dor em dias [{p['tempo_dor']}]: ").strip()
    if entrada_tempo:
        try:
            p["tempo_dor"] = int(entrada_tempo)
        except ValueError:
            print(" Valor inválido, mantendo anterior.")

    entrada_renda = input(f"Renda [{p['renda']}]: ").strip().replace(',', '.')
    if entrada_renda:
        try:
            p["renda"] = float(entrada_renda)
        except ValueError:
            print(" Valor inválido, mantendo anterior.")

    bairro = input(f"Bairro [{p['bairro']}]: ").strip()
    if bairro:
        p["bairro"] = bairro

    p["urgencia"] = calcular_urgencia(p["tipo_dor"], p["tempo_dor"], p["renda"], p["idade"])
    salvar_dados()
    print(f"\n Paciente '{p['nome']}' atualizado com sucesso. Nova urgência: {p['urgencia']}.\n")


def excluir_paciente():
    """Remove um paciente da lista."""
    print("\n--- 🗑️ Excluir Paciente ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    listar_pacientes()
    while True:
        escolha = obter_inteiro("Número do paciente a excluir (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(pacientes):
            break
        print(" Número inválido. Tente novamente.")

    nome = pacientes[escolha]["nome"]
    confirmacao = input(f"Tem certeza que deseja excluir '{nome}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        pacientes.pop(escolha)
        salvar_dados()
        print(f"\n Paciente '{nome}' excluído com sucesso.\n")
    else:
        print(" Exclusão cancelada.\n")

# CRUD — DENTISTAS

def cadastrar_dentista(nome="", especialidade="clínico geral", bairro="", max_pacientes=10):  # ← valores padrão
    """Cadastra um novo dentista voluntário."""
    print("\n Cadastrar Dentista ")
    nome = input(f"Nome do dentista [{nome or 'obrigatório'}]: ").strip() or nome
    if not nome:
        print(" Nome não pode ser vazio.")
        return

    especialidade = obter_especialidade(
        f"Especialidade (prótese/ortodontia/odontopediatria/clínico geral/cirurgia/endodontia) [{especialidade}]: "
    )
    bairro = input(f"Bairro/Cidade [{bairro or 'obrigatório'}]: ").strip() or bairro
    max_pacientes = obter_inteiro(f"Número máximo de pacientes por mês [{max_pacientes}]: ")

    dentista = {
        "nome": nome,
        "especialidade": especialidade,
        "bairro": bairro,
        "max_pacientes": max_pacientes,
        "atendidos": 0
    }
    dentistas.append(dentista)
    salvar_dados()
    print(f"\nDentista '{nome}' cadastrado.\n")