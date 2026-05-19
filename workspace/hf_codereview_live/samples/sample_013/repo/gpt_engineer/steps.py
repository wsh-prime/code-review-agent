    return []


def human_review(ai: AI, dbs: DBs):
    review = human_input()
    dbs.memory["review"] = review.to_json()  # type: ignore
    return []


class Config(str, Enum):
    DEFAULT = "default"
    BENCHMARK = "benchmark"
    SIMPLE = "simple"
    TDD = "tdd"
    TDD_PLUS = "tdd+"
    CLARIFY = "clarify"
    RESPEC = "respec"
    EXECUTE_ONLY = "execute_only"
    EVALUATE = "evaluate"
    USE_FEEDBACK = "use_feedback"


# Different configs of what steps to run
STEPS = {
    Config.DEFAULT: [
        archive,
        clarify,
        gen_clarified_code,
        gen_entrypoint,
        execute_entrypoint,
        human_review,
    ],
    Config.BENCHMARK: [archive, simple_gen, gen_entrypoint],
    Config.SIMPLE: [archive, simple_gen, gen_entrypoint, execute_entrypoint],
    Config.TDD: [
        archive,
        gen_spec,
        gen_unit_tests,
        gen_code,
        gen_entrypoint,
        execute_entrypoint,
        human_review,
    ],
    Config.TDD_PLUS: [
        archive,
        gen_spec,
        gen_unit_tests,
        gen_code,
        fix_code,
        gen_entrypoint,
        execute_entrypoint,