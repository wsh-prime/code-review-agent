
def setup_sys_prompt(dbs: DBs) -> str:
    return (
        dbs.preprompts["generate"] + "\nUseful to know:\n" + dbs.preprompts["philosophy"]
    )


def get_prompt(dbs: DBs) -> str:
    """While we migrate we have this fallback getter"""
    assert (
        "prompt" in dbs.input or "main_prompt" in dbs.input
    ), "Please put your prompt in the file `prompt` in the project directory"

    if "prompt" not in dbs.input:
        print(
            colored("Please put the prompt in the file `prompt`, not `main_prompt", "red")
        )
        print()
        return dbs.input["main_prompt"]

    return dbs.input["prompt"]


def curr_fn() -> str:
    """Get the name of the current function"""
    return inspect.stack()[1].function


# All steps below have the signature Step


def simple_gen(ai: AI, dbs: DBs) -> List[dict]:
    """Run the AI on the main prompt and save the results"""
    messages = ai.start(setup_sys_prompt(dbs), get_prompt(dbs), step_name=curr_fn())
    to_files(messages[-1]["content"], dbs.workspace)
    return messages


def clarify(ai: AI, dbs: DBs) -> List[dict]:
    """
    Ask the user if they want to clarify anything and save the results to the workspace
    """
    messages = [ai.fsystem(dbs.preprompts["qa"])]
    user_input = get_prompt(dbs)
    while True:
        messages = ai.next(messages, user_input, step_name=curr_fn())

        if messages[-1]["content"].strip() == "Nothing more to clarify.":
            break

        if messages[-1]["content"].strip().lower().startswith("no"):