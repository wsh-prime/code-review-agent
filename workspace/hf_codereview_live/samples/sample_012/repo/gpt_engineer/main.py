
    model = fallback_model(model)
    ai = AI(
        model=model,
        temperature=temperature,
    )

    input_path = Path(project_path).absolute()
    memory_path = input_path / f"{run_prefix}memory"
    workspace_path = input_path / f"{run_prefix}workspace"
    archive_path = input_path / f"{run_prefix}archive"

    initial_run = not os.path.exists(memory_path) and not os.path.exists(workspace_path)
    dbs = DBs(
        memory=DB(memory_path),
        logs=DB(memory_path / "logs"),
        input=DB(input_path),
        workspace=DB(workspace_path),
        preprompts=DB(Path(__file__).parent / "preprompts"),
        archive=None if initial_run else DB(archive_path),
    )

    steps = STEPS[steps_config]
    for step in steps:
        messages = step(ai, dbs)
        dbs.logs[step.__name__] = json.dumps(messages)

    collect_learnings(model, temperature, steps, dbs)


if __name__ == "__main__":
    app()
