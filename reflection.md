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
*Answer: I used Claude Code (Opus 5) inside VS Code. I did not use it to hand me the answers. I played the game myself first and wrote down what looked wrong, then used Claude for four specific jobs: confirming whether a bug I suspected was actually a bug rather than normal Streamlit behavior, mapping the symptom back to the exact lines causing it, writing a failing test before any fix went in, and drafting the commit messages. Keeping it to those four jobs meant I stayed the one deciding what counted as broken and what order to fix things in.*
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
*Answer: I thought the "Developer Debug Info" panel and the "Attempts left" banner were two separate bugs, because both showed stale numbers. Claude said they were one bug, not two: both render above the submit handler, so Streamlit draws them on its way down the script before the guess is processed, and they always show the values from before my last guess. To verify it I drove the app with a pinned secret and printed the real session state next to what the page displayed, and the gap was exactly one guess every time: after guessing 10 the counter was 1 but the banner still said "Attempts left: 8", after guessing 20 it was 2 and the banner said 7. That confirmed the location (app.py lines 53 to 66, above the handler at line 97) rather than the counter logic itself, so I left it as a FIXME instead of touching code that was working.*
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
*Answer: For the swapped hints, Claude swapped the two message strings in check_guess, ran the tests, got 6 passed, and told me the hint system was fixed. It was not. check_guess still had a fallback that compared the guess and the secret as strings, so a guess of 9 against a secret of "50" came back "Too High", because "9" sorts after "50" alphabetically. I caught it by asking for the fix in its entirety and writing two cases as tests, check_guess(9, "50") and check_guess(100, "99"), and both failed against the supposedly fixed code. The real lesson was that the green test run was misleading: the starter tests only checked the outcome label and never the hint message, so they would have passed on the original broken code too, and a passing suite is not the same thing as a working feature.*

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
