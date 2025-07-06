from llm.db import get_entries, save
from llm.prompts import gen_prompt, gen_advice

def run(user_id):
    entries = get_entries(user_id)
    prompt = gen_prompt(entries)

    print("\nToday's Prompt:\n", prompt)
    journal = input("\nWrite your journal entry:\n")

    advice = gen_advice(journal)
    print("\nAI Advice:\n", advice)

    save(user_id, prompt, journal, advice)

if __name__ == "__main__":
    run("sayantan123")