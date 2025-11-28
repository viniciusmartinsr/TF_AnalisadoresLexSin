# main.py
from obs_lexer import ObsLexer
from obs_parser import ObsParser
from translator import translate
import sys
import os

if __name__ == "__main__":
    # Verifica se passou o arquivo como argumento
    if len(sys.argv) < 2:
        print("Uso: python main.py arquivo.obs")
        sys.exit(1)

    filename = sys.argv[1]

    # Tenta ler o arquivo de entrada
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        sys.exit(1)

    lexer = ObsLexer()
    parser = ObsParser()

    # Executa a análise léxica e sintática
    try:
        tokens = lexer.tokenize(text)
        ast = parser.parse(tokens)
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        sys.exit(1)

    # Se a AST não foi gerada (ex: erro de sintaxe), para aqui
    if not ast:
        print("Erro: Não foi possível gerar o código (verifique erros de sintaxe acima).")
        sys.exit(1)

    # Traduz para C
    c_code = translate(ast)

    # --- CORREÇÃO DO ERRO DA PASTA ---
    output_dir = "out"
    
    # Cria a pasta 'out' se ela não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Diretório '{output_dir}' criado.")

    # Define o caminho final do arquivo (ex: out/teste.c)
    out_name = os.path.join(output_dir, os.path.basename(filename).replace(".obs", ".c"))
    
    # Salva o arquivo
    with open(out_name, "w", encoding='utf-8') as f:
        f.write(c_code)

    print(f"Sucesso! Arquivo gerado: {out_name}")