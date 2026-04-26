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

## Summary

Taste Tuner is a music recommender that ranks songs from a small catalog using user preferences for genre, mood, and target energy. It separates ranking scores from confidence scores, so high-ranked recommendations can be revealed as uncertain if the system doesn't trust them. The confidence score detects when context is missing or when the recommendation is based on weak matches.

<img src="/assets//preview.gif">

---

## Architecture Overview

### System Diagram (Mermaid.js)

<img src="/assets/image.png"/>

### Short Explanation

The system takes user preferences and runs them through a scoring algorithm that ranks all songs. Each song gets both a ranking score and a confidence score. The confidence score is lower when user input is invalid or when matches are weak. Testing uses 5 edge-case profiles to stress-test the system. Results show the system isn't perfect, especially with incomplete input, but it's honest about what it doesn't know.


---

## Setup Instructions

1. Clone the repository and navigate to the directory.
2. Create and activate a virtual environment (recommended).

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Run the recommender with confidence scores and test summary.

```bash
python .\src\main.py
```

5. Run tests to verify scoring and confidence behavior.

```bash
pytest -v
```

---

## Sample Interactions

<!--
INSTRUCTIONS:
- Include at least 2-3 examples.
- Each example must show: input and resulting AI output.
- Use real outputs from your current system, not hypothetical text.
-->

### Example 1: Strong Match
**Input:** `{"genre": "pop", "mood": "happy", "energy": 0.8}`

**Output:**
```
Sunrise City - Score: 3.96, Confidence: 0.95
Because: genre match (typo-tolerant)! (+1.0); mood match (typo-tolerant)! (+1.0); energy similarity (+1.96)
```

### Example 2: Typo Tolerance Works
**Input:** `{"genre": "lo-fi", "mood": "chill", "energy": 0.30}`

**Output:**
```
Library Rain - Score: 3.90, Confidence: 0.90
Because: genre match (typo-tolerant)! (+1.0); mood match (typo-tolerant)! (+1.0); energy similarity (+1.90)
```
Note: "lo-fi" was matched against "lofi" in the dataset using similarity detection.

### Example 3: Invalid Input Reduces Confidence
**Input:** `{"genre": "rock", "mood": "intense", "energy": 1.8}` (energy out of range)

**Output:**
```
Storm Runner - Score: 3.82, Confidence: 0.72
Because: genre match (typo-tolerant)! (+1.0); mood match (typo-tolerant)! (+1.0); energy similarity (+1.82); user energy normalized from 1.80 to 1.00
```
Note: Confidence is lower even though rank is high, signaling the recommendation is risky.

---

## Design Decisions

<!--
INSTRUCTIONS:
- Explain why you built it this way.
- Include key design choices and the trade-offs you accepted.
- Good answers include at least 2-3 concrete decisions.
-->

### Decision 1: Separate Ranking Score from Confidence Score
**Why:** A single score hides the system's uncertainty. High ranking could mean a genuinely good match or just lucky alignment on one factor. Splitting them makes uncertainty visible.

**Trade-off:** More complex API. But this forces code that uses the recommender to think about certainty, not just ranking.

### Decision 2: Typo-Tolerant Matching
**Why:** Real users mistype. The system detects similarity instead of demanding exact matches, so "lo-fi" and "lofi" are treated as the same.

**Trade-off:** Occasional false positives are possible. Accept noise to be forgiving to users.

### Decision 3: Confidence Penalty for Invalid Input
**Why:** Out-of-range energy or missing context indicates incomplete user data. The system should signal it's less sure rather than pretending the recommendation is solid.

**Trade-off:** Recommendations with invalid input still get returned. Current approach is more forgiving but requires users to read confidence.

---

## Testing Summary

<!--
INSTRUCTIONS:
- Summarize what worked, what did not, and what you learned.
- Mention testing methods (unit tests, edge cases, consistency checks, etc.).
- Include current test status/results when available.
-->

### What Worked

Data loading, scoring logic, typo-tolerant matching, energy normalization, and confidence scoring all function as intended. Tests pass for strong matches (confidence 0.95+), weak matches (confidence near 0.0), and the critical case of missing context (confidence drops significantly). The system correctly penalizes invalid input without crashing.

### What Did Not Work

Initial tests assumed an OOP API but the codebase uses functional dictionaries; resolved by rewriting tests to match the implementation. Early typo logic only did exact matching; upgraded to SequenceMatcher. Confidence wasn't displayed in the CLI at first. These weren't critical failures—they were catching misalignments between intended design and actual code.

### What I Learned

Reliability testing is most valuable when it catches the system struggling. The test suite found that confidence averages 0.53 on edge cases, which isn't a failure. It's evidence the system is working correctly by being honest. The most helpful insight was normalizing user preferences and detecting similarity to handle typos, but this system is not perfect. It's serviceable for most cases, which is exactly what you want from a small simulation: good enough to prove the concept, transparent about limitations.

---

## Reflection

<!--
INSTRUCTIONS:
- Write a short reflection on what this project taught you about AI and problem-solving.
- Focus on engineering judgment, iteration, and responsible AI behavior.
- Keep tone professional and portfolio-ready.
-->

The limitations of the AI include its low confidence in handling typos, which it attempts to handle by detecting similarity, but isn't always accurate. It's likely that the AI can be misused, as a prominent bias is that it reccomend songs that largely match exact preferences and never exposes users to new genres/moods. This can be addressed by adding a diversity constraint, which also randomly samples diverse songs. I was surprised at the AI's effectiveness in generating test cases, although there were some test cases it designed which failed. The most helpful suggestion the AI gave was to normalize user preferences with known genres and detect similarity to handle typos, but this system is not perfect and does not always exhibit accurate reccomendations. However, it's serviceable for the most part

