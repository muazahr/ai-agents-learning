"""Punto de entrada del primer agente."""

from app.agent import run_agent


def main() -> None:
    print("🤖 AI Agent — Proyecto 01")
    print("Escribe 'salir' para terminar.\n")
    while True:
        user_message = input("Tú: ").strip()
        if user_message.lower() in {"salir", "exit", "quit"}:
            print("Agente: ¡Hasta luego!")
            break
        if not user_message:
            continue
        try:
            print(f"Agente: {run_agent(user_message)}\n")
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
