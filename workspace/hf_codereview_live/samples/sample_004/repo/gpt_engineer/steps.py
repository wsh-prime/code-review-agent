            'If everything is sufficiently clear, only answer "no".'
        )

    print()
    return messages


def gen_spec(ai: AI, dbs: DBs):
    '''
    Generate a spec from the main prompt + clarifications and save the results to the workspace
    '''
    messages = [ai.fsystem(setup_sys_prompt(dbs)), ai.fsystem(f"Main prompt: {dbs.input['main_prompt']}")]

    messages = ai.next(messages, dbs.identity['spec'])
    messages = ai.next(messages, dbs.identity['respec'])
    messages = ai.next(messages, dbs.identity['spec'])

    dbs.memory['specification'] = messages[-1]['content']

    return messages

def pre_unit_tests(ai: AI, dbs: DBs):
    '''
    Generate unit tests based on the specification, that should work.
    '''
    messages = [ai.fsystem(setup_sys_prompt(dbs)), ai.fuser(f"Instructions: {dbs.input['main_prompt']}"), ai.fuser(f"Specification:\n\n{dbs.memory['specification']}")]

    messages = ai.next(messages, dbs.identity['unit_tests'])

    dbs.memory['unit_tests'] = messages[-1]['content']
    to_files(dbs.memory['unit_tests'], dbs.workspace)

    return messages


def run_clarified(ai: AI, dbs: DBs):
    # get the messages from previous step

    messages = [
        ai.fsystem(setup_sys_prompt(dbs)),
        ai.fuser(f"Instructions: {dbs.input['main_prompt']}"),
        ai.fuser(f"Specification:\n\n{dbs.memory['specification']}"),
        ai.fuser(f"Unit tests:\n\n{dbs.memory['unit_tests']}"),
    ]
    messages = ai.next(messages, dbs.identity['use_qa'])
    to_files(messages[-1]['content'], dbs.workspace)
    return messages


# Different configs of what steps to run
STEPS = {