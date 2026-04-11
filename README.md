<!-- # 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

*Each Song in the system will use genre, mood, and all numerical values. The UserProfile stores the user's favorite genre, favorite mood, target energy, and whether they like acoustic. The Reccomender computes a score for each song by assigning weights to the respective categories (genre, mood, and numerical values). The genre and mood checks are binary, either a "yes" or a "no", whereas the numeric similarity serves as the fine tuning.*

### Algorithm Recipe
1. Initialize an empty list to hold the scored songs
2. Iterate through each song
3. For each song, initialize a score of 0
4. If the genre matches the user's favorite, add 2 points to score
5. If the mood matches the user's favorite, add 1 point to the score
6. Calculate the different in the user's target energy and the song energy. Add this to the score
7. Sort the list by descending score
8. Return first k items from the list of ranked songs


## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
``` -->

# 🎵 Taste Tuner

<!--
INSTRUCTIONS:
- This is a blank portfolio template.
- Do not leave placeholder text in your final version.
- Keep writing concise, specific, and evidence-based.
-->

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.
-->



---

## Architecture Overview

### System Diagram (Mermaid.js)

<!--
INSTRUCTIONS:
- Add a short Mermaid diagram here.
- Must include: main components (retriever/agent/evaluator/tester), data flow (input -> process -> output), and where humans/testing validate results.
- Keep diagram easy to read (5-8 nodes is enough).
-->

<img src="/assets/image.png"/>

### Short Explanation

<!--
INSTRUCTIONS:
- Explain the diagram in 3-5 sentences.
- Describe input, processing, output, testing, and human-in-the-loop checks.
-->

---

## Setup Instructions

<!--
INSTRUCTIONS:
- Provide step-by-step directions to run your code.
- Include environment setup, dependency install, run command, and test command.
- Keep commands copy-paste ready.
-->

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]

```bash
# Add setup and run commands here
```

---

## Sample Interactions

<!--
INSTRUCTIONS:
- Include at least 2-3 examples.
- Each example must show: input and resulting AI output.
- Use real outputs from your current system, not hypothetical text.
-->

### Example 1

<!--
INSTRUCTIONS:
- Input:
- Output:
-->

### Example 2

<!--
INSTRUCTIONS:
- Input:
- Output:
-->

### Example 3

<!--
INSTRUCTIONS:
- Input:
- Output:
-->

---

## Design Decisions

<!--
INSTRUCTIONS:
- Explain why you built it this way.
- Include key design choices and the trade-offs you accepted.
- Good answers include at least 2-3 concrete decisions.
-->

### Decision 1

<!--
INSTRUCTIONS:
- Why this decision:
- Trade-off:
-->

### Decision 2

<!--
INSTRUCTIONS:
- Why this decision:
- Trade-off:
-->

### Decision 3

<!--
INSTRUCTIONS:
- Why this decision:
- Trade-off:
-->

---

## Testing Summary

<!--
INSTRUCTIONS:
- Summarize what worked, what did not, and what you learned.
- Mention testing methods (unit tests, edge cases, consistency checks, etc.).
- Include current test status/results when available.
-->

### What Worked

<!--
INSTRUCTIONS:
- List validated behaviors.
-->

### What Did Not Work

<!--
INSTRUCTIONS:
- Note failures, bugs, or limitations encountered.
- Briefly explain how you addressed them (or why unresolved).
-->

### What I Learned

<!--
INSTRUCTIONS:
- Capture practical lessons about reliability/testing.
-->

---

## Reflection

<!--
INSTRUCTIONS:
- Write a short reflection on what this project taught you about AI and problem-solving.
- Focus on engineering judgment, iteration, and responsible AI behavior.
- Keep tone professional and portfolio-ready.
-->

