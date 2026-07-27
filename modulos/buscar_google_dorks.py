#!/usr/bin/env python3
"""
Google Dorks Assembler & Search Tool - CORRIGIDO
Autor: HackerAI
Uso: python3 dorks_assembler.py
"""

import webbrowser
import urllib.parse
import sys
import re

# ============================================================
# BASE DE DORKS ORGANIZADA POR CATEGORIA
# ============================================================

DORKS_DB = {
    "1": {
        "nome": "Painéis de Administração",
        "dorks": [
            "inurl:admin",
            "inurl:login",
            "inurl:admin/login",
            "inurl:administrator",
            'intitle:"admin login"',
            'intitle:"painel de controle"',
            "inurl:wp-admin",
            "inurl:admin.php",
            "inurl:user/login",
            "inurl:admin/login.php",
            'intitle:"Administration"'
        ]
    },
    "2": {
        "nome": "Diretórios Abertos (Index Of)",
        "dorks": [
            'intitle:"index of /"',
            'intitle:"index of" "parent directory"',
            'intitle:"index of" /etc/',
            'intitle:"index of" /root/',
            'intitle:"index of" /backup/',
            'intitle:"index of" "private"',
            'intitle:"index of" "config"',
            'intitle:"index of" "database"',
            'intitle:"Directory Listing"',
            '"Index of /admin"',
            '"Index of /secret"',
            '"Index of /backup"'
        ]
    },
    "3": {
        "nome": "Arquivos com Credenciais e Dados Sensíveis",
        "dorks": [
            'filetype:txt "senha"',
            'filetype:txt "password"',
            'filetype:xls "username" "password"',
            'filetype:xlsx "senha"',
            'filetype:csv "password"',
            'filetype:sql "INSERT INTO" "password"',
            'filetype:ini "db_password"',
            'filetype:env "DB_PASSWORD"',
            'filetype:cfg "password"',
            'filetype:conf "password"',
            'filetype:log "password"',
            'ext:log "admin" "password"',
            'ext:bak "password"',
            'filetype:pdf "confidencial"'
        ]
    },
    "4": {
        "nome": "Configurações e Código Expostos",
        "dorks": [
            'filetype:php "DB_HOST"',
            'filetype:php "DB_PASSWORD"',
            'filetype:php "$db_password"',
            'filetype:asp "connectionstring"',
            'filetype:config "connectionString"',
            'filetype:yaml "database" "password"',
            'filetype:xml "password"',
            'filetype:json "password"',
            'ext:env "DB_PASSWORD"',
            'ext:gitignore "DB_PASSWORD"'
        ]
    },
    "5": {
        "nome": "Logs e Dump de Dados",
        "dorks": [
            'filetype:log "admin" "login"',
            'filetype:log "failed password"',
            'filetype:log "root:"',
            'filetype:log "POST /login"',
            "inurl:access.log",
            "inurl:error.log",
            'intitle:"index of" logs',
            "inurl:/proc/self/environ"
        ]
    },
    "6": {
        "nome": "Câmeras, IoT e Dispositivos Expostos",
        "dorks": [
            'intitle:"webcam" "live"',
            'intitle:"Live View / - AXIS"',
            'intitle:"Network Camera" -user',
            "inurl:/view/view.shtml",
            "inurl:/cgi-bin/webcam",
            'intitle:"EvoCam"',
            'intitle:"webcam 7"',
            'intitle:"IP CAMERA" -login',
            '"dvr login" inurl:admin'
        ]
    },
    "7": {
        "nome": "SQL Injection (IDs na URL)",
        "dorks": [
            "inurl:product.php?id=",
            "inurl:item.php?id=",
            "inurl:article.php?id=",
            "inurl:page.php?id=",
            "inurl:index.php?id=",
            "inurl:cat.php?id=",
            "inurl:details.php?id=",
            "inurl:view.php?id=",
            "inurl:show.php?id=",
            "inurl:pid=",
            "inurl:category.php?id="
        ]
    },
    "8": {
        "nome": "WordPress Específico",
        "dorks": [
            "inurl:wp-config.php",
            'inurl:wp-admin intitle:"login"',
            "inurl:wp-content/uploads/filetype:php",
            'intitle:"index of" wp-content',
            "inurl:/wp-json/wp/v2/users",
            'filetype:sql "wp_users"',
            "inurl:wp-config.bak"
        ]
    },
    "9": {
        "nome": "Cloud / AWS Exposto",
        "dorks": [
            'filetype:pem "BEGIN RSA PRIVATE KEY"',
            "inurl:.aws/config",
            "inurl:.aws/credentials",
            '"bucket.s3.amazonaws.com" intitle:"index of"',
            'filetype:json "aws_access_key_id"'
        ]
    },
    "10": {
        "nome": "Personalizado (digitar manualmente)",
        "dorks": ["__CUSTOM__"]
    },
    "11": {
        "nome": "Menu inicial",
        
    }
}

def sanitizar_site(input_site):
    """
    Remove protocolo (http/https), barras no final, www, e caminhos extras
    para deixar apenas o domínio limpo para o operador site:
    """
    # Remove http:// ou https://
    site = re.sub(r'^https?://', '', input_site.strip())
    # Remove www. se existir (opcional, as vezes o Google trata diferente)
    # site = re.sub(r'^www\.', '', site)
    # Remove tudo após a primeira barra (caminhos)
    site = site.split('/')[0]
    # Remove trailing slash se sobrou
    site = site.rstrip('/')
    return site


def buscar_google_dorks():
    """
    Monta e executa busca no Google com base em Dorks selecionados.
    O usuário escolhe categoria, dork, adiciona site: e busca.
    """
    print("=" * 70)
    print("  🔍  GOOGLE DORKS ASSEMBLER & SEARCH TOOL")
    print("=" * 70)

    # --- ETAPA 1: ESCOLHER CATEGORIA ---
    print("\n📂 CATEGORIAS DISPONÍVEIS:\n")
    for key, cat in DORKS_DB.items():
        print(f"  [{key}] {cat['nome']}")

    cat_choice = input("\n👉 Escolha a categoria (número): ").strip()

    while cat_choice not in DORKS_DB:
        cat_choice = input("❌ Inválido. Digite o número da categoria: ").strip()

    categoria = DORKS_DB[cat_choice]
    
    # --- ETAPA 2: LISTAR DORKS DA CATEGORIA ---
    if cat_choice != "11":
        dorks = categoria["dorks"]

    if categoria["nome"] == "Personalizado (digitar manualmente)":
        dork_escolhido = input("\n✏️  Digite sua query personalizada: ").strip()
        if not dork_escolhido:
            print("❌ Query vazia. Saindo.")
            return None
        
    elif cat_choice == "11": 
        print("Voltando ao menu inicial")
        return "menu"
        
    else:
        print(f"\n📋 DORKS DISPONÍVEIS em '{categoria['nome']}':\n")
        for i, dork in enumerate(dorks, 1):
            print(f"  [{i}] {dork}")

        try:
            dork_idx = int(input("\n👉 Escolha o dork (número): ").strip())
            dork_escolhido = dorks[dork_idx - 1]
        except (ValueError, IndexError):
            print("❌ Opção inválida. Saindo.")
            return None

    # --- ETAPA 3: MONTAR QUERY FINAL ---
    print(f"\n✅ Dork base: {dork_escolhido}")

    # Perguntar se quer adicionar um site:
    raw_site = input("\n🌐 Adicionar site:? (ex: ead.exemplo.com) [Enter para pular]: ").strip()
    
    if raw_site:
        # LIMPA O DOMÍNIO - ESSA É A CORREÇÃO PRINCIPAL
        site_limpo = sanitizar_site(raw_site)
        if site_limpo != raw_site:
            print(f"   ⚡ Domínio normalizado: '{raw_site}' → '{site_limpo}'")
        query = f"site:{site_limpo} {dork_escolhido}"
    else:
        query = dork_escolhido

    # Extras que o usuário queira adicionar
    extras = input("\n➕ Termos extras (opcional, Enter para pular): ").strip()
    if extras:
        query = f"{query} {extras}"

    # ----- ETAPA 4: PERGUNTA SE QUER TENTAR VARIAÇÕES -----
    tentar_variacoes = input("\n🔄 Tentar variações da busca? (remove aspas, testa sem site:) [s/N]: ").strip().lower()
    
    queries_para_testar = [query]
    
    if tentar_variacoes == "s":
        # Variação 1: remove aspas duplas
        q_sem_aspas = query.replace('"', '')
        if q_sem_aspas != query:
            queries_para_testar.append(q_sem_aspas)
        
        # Variação 2: se tem site:, tenta sem ele também
        if "site:" in query and raw_site:
            q_sem_site = dork_escolhido
            if extras:
                q_sem_site = f"{q_sem_site} {extras}"
            queries_para_testar.append(f"🔹 SEM SITE: {q_sem_site}")
            queries_para_testar.append(q_sem_site)  # versão real
        
        # Variação 3: usando www. se não tinha
        if raw_site and "www." not in query:
            q_com_www = query.replace("site:", "site:www.")
            queries_para_testar.append(f"🔹 COM WWW: {q_com_www}")
            queries_para_testar.append(q_com_www)

    # --- ETAPA 5: EXIBIR E ABRIR ---
    print("\n" + "=" * 70)
    
    # Mostra todas as variações
    queries_reais = [q for q in queries_para_testar if not q.startswith("🔹")]
    queries_descricao = [q for q in queries_para_testar if q.startswith("🔹")]
    
    print("\n📌 QUERY PRINCIPAL:")
    print(f"   {queries_reais[0]}")
    
    if queries_descricao:
        print("\n📌 VARIAÇÕES DISPONÍVEIS:")
        for desc in queries_descricao:
            print(f"   {desc}")
    
    print("\n" + "=" * 70)

    # Abre a query principal
    url_principal = f"https://www.google.com/search?q={urllib.parse.quote_plus(queries_reais[0])}"
    print(f"\n   🌍 URL: {url_principal}")

    abrir = input("\n💻 Abrir no navegador agora? [s/N]: ").strip().lower()
    if abrir == "s":
        webbrowser.open(url_principal)
        print("   ✅ Navegador aberto com a query principal!")
        
        # Se tiver variações, pergunta se quer abrir também
        if len(queries_reais) > 1:
            for q_alt in queries_reais[1:]:
                if input(f"\n🔄 Abrir variação '{q_alt[:60]}...'? [s/N]: ").strip().lower() == "s":
                    url_alt = f"https://www.google.com/search?q={urllib.parse.quote_plus(q_alt)}"
                    webbrowser.open(url_alt)
                    print("   ✅ Aberto!")
    else:
        print("   ℹ️  Copie a URL e cole manualmente no navegador.")

    return {
        "query": queries_reais[0],
        "url": url_principal,
        "categoria": categoria["nome"],
        "dork": dork_escolhido,
        "variacoes": queries_reais[1:] if len(queries_reais) > 1 else []
    }


    def listar_todos_dorks():
        return dict(DORKS_DB)

    def montar_query_rapida(site_alvo=None, tipo="admin"):
        prefixo = f"site:{sanitizar_site(site_alvo)} " if site_alvo else ""
        busca_rapida = {
            "admin": 'inurl:admin intitle:"login"',
            "backup": 'intitle:"index of" backup',
            "config": "filetype:env DB_PASSWORD",
            "log": 'filetype:log "password" "admin"',
            "cameras": 'intitle:"webcam" "live"'
        }
        if tipo not in busca_rapida:
            print(f"❌ Tipo '{tipo}' não encontrado. Opções: {list(busca_rapida.keys())}")
            return None
        query = f"{prefixo}{busca_rapida[tipo]}"
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        webbrowser.open(url)
        print(f"🔍 Buscando: {query}")
        return url

    # ============================================================
    # EXECUÇÃO DIRETA
    # ============================================================
    

    """
    if __name__ == "__main__":
        try:
            resultado = buscar_google_dorks()
            if resultado:
                print("\n📝 RESUMO DA BUSCA:")
                print(f"   Categoria: {resultado['categoria']}")
                print(f"   Dork:      {resultado['dork']}")
                print(f"   Query:     {resultado['query']}")
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até mais!")
            sys.exit(0)
    """
