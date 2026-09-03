import random


def generate_evaluation(content: str):
    random.seed(len(content))  # deterministic: same transcript always scores the same
    communication = round(random.uniform(5, 10), 1)
    technical = round(random.uniform(5, 10), 1)
    problem_solving = round(random.uniform(5, 10), 1)

    strengths, weaknesses = [], []
    for label, score in [('communication', communication),
                          ('technical accuracy', technical),
                          ('problem-solving', problem_solving)]:
        (strengths if score >= 8 else weaknesses).append(label)

    if strengths:
        summary = f"The candidate demonstrated good {', '.join(strengths)}"
        summary += f" but could improve {', '.join(weaknesses)}." if weaknesses else "."
    else:
        summary = f"The candidate needs improvement in {', '.join(weaknesses)}."

    return communication, technical, problem_solving, summary