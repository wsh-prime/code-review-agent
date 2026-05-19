from termcolor import colored

from gpt_engineer.ai import AI
from gpt_engineer.chat_to_files import to_files
from gpt_engineer.db import DBs


def setup_sys_prompt(dbs):
    return (
        dbs.preprompts["generate"] + "\nUseful to know:\n" + dbs.preprompts["philosophy"]
    )


Step = TypeVar("Step", bound=Callable[[AI, DBs], List[dict]])


def get_prompt(dbs):
    """While we migrate we have this fallback getter"""
    assert (
        "prompt" in dbs.input or "main_prompt" in dbs.input
    ), "Please put your prompt in the file `prompt` in the project directory"

    if "prompt" not in dbs.input:
        print(
            colored("Please put the prompt in the file `prompt`, not `main_prompt", "red")
        )
        print()

    return dbs.input.get("prompt", dbs.input["main_prompt"])


def simple_gen(ai: AI, dbs: DBs):
    """Run the AI on the main prompt and save the results"""
    messages = ai.start(setup_sys_prompt(dbs), get_prompt(dbs))
    to_files(messages[-1]["content"], dbs.workspace)
    return messages


def clarify(ai: AI, dbs: DBs):
    """
    Ask the user if they want to clarify anything and save the results to the workspace
    """
    messages = [ai.fsystem(dbs.preprompts["qa"])]
    user_input = get_prompt(dbs)
    while True:
        messages = ai.next(messages, user_input)

        if messages[-1]["content"].strip().lower().startswith("no"):
            print("Nothing more to clarify.")
            break
