"Aluno: Eduardo Teixeira Ribeiro Cardoso"
"Aluno: Weverton Valério da Silva"

from gemma import decidir_ferramenta, gerar_resposta_final
from executor import executar_ferramenta


def main():
    print("JARVIS Acadêmico iniciado!")
    print("Digite sua pergunta normalmente.")
    print("Para sair, digite: sair\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower().strip() == "sair":
            print("JARVIS finalizado.")
            break

        decisao = decidir_ferramenta(pergunta)

        resultado = executar_ferramenta(decisao)

        resposta_final = gerar_resposta_final(pergunta, resultado)

        print("\nJARVIS:")
        print(resposta_final)

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()