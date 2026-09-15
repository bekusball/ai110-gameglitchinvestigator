# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
*Answer: Looked like a put together guessing game* 
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
*Answer:*
  - *The hint was swapped. When I answered something smaller it told me to "Go LOWER!: and when I answered something higher it told me to "Go HIGHER!"*
  - *On Load, Normal mode promised 8 guesses, but it shows 7 left*

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 90 (secret was 91) | "Too Low" hint shown, telling player to go HIGHER | "Too Low" hint shown, but message said "Go LOWER!" (hint polarity swapped) | none |
| Guessed 90 when the secret was 50 (first guess), watching Score in "Developer Debug Info" | A wrong guess should cost points, so score goes from 0 to -5 | Score went from 0 to +5 — a "Too High" guess is rewarded +5 whenever the attempt counter is even, so six wrong guesses in a row net 0 points instead of -30. Wins are also short by 20 (a first-guess win pays 70, not 90) | none |
| Played Normal difficulty (sidebar says "Attempts allowed: 8") to the last guess | Should get 8 real guesses before "Out of attempts"; banner and game-over message should agree on the count | Game over fires after only 7 guesses, and on that final rerun the "Attempts left: 1" banner and "Out of attempts! Game over." error appear together on the same page (attempts counter starts at 1 instead of 0, so it's off by one throughout) | none |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
