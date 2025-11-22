TF_AnalizadoresLexSin/
│
├── lexer.py          # analisador léxico (SLY)
├── parser.py         # analisador sintático baseado na gramática ObsAct
├── ast_nodes.py      # definição das classes da AST
├── translator.py     # tradutor de ObsAct para C
├── runtime.c         # funções obrigatórias: ligar, desligar, alerta
├── main.py           # ponto de entrada do compilador
│
├── tests/            # programas ObsAct usados como teste (.obs)
├── out/              # códigos C gerados pelo compilador
│
├── README.md         # este arquivo
└── relatorio.pdf     # relatório final do trabalho
