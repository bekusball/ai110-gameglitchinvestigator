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
*Answer: I decided through red testing. Before changing any code I wrote a test that failed on purpose, and I made sure the failure message described the exact symptom I had seen while playing. If a test passed before I touched the code, then it was not testing the bug and I rewrote it. Only after I had a real red did I make the fix, and the bug counted as fixed when that same test went green and the rest of the suite stayed green. That order mattered, because it stopped me from writing a test that quietly agreed with whatever the code already did.*
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
*Answer: For the attempt counter I wrote test_normal_difficulty_allows_eight_real_guesses in tests/test_app_flow.py, which plays a Normal game through Streamlit's AppTest harness and submits eight wrong guesses, checking after each one that the game is still playing. It failed with "game ended after only 7 guesses", and a companion test failed with "Attempts left: 7" on a game that had not been played yet. That showed me the counter was not losing a guess somewhere during play, it was starting at 1 instead of 0, so every game began already one guess down. I also wrote tests for empty input and for "abc", and both failed because the counter was being incremented before the guess was ever validated, which is a bug I never would have found by clicking around, since a typo looks like nothing happened.*
- Did AI help you design or understand any tests? How?
*Answer: Yes. The clearest case was when I asked Claude to "look into the debug history lag (dont fix that the lag yet)", because I wanted to understand what was happening before anything changed. It explained that Streamlit runs the script top to bottom and that the debug panel is drawn before the submit handler updates the state, then it verified that by printing the real session state next to the displayed values so I could see the one-guess gap for myself. Claude also showed me why the starter tests in tests/test_game_logic.py were not protecting anything: they compared a tuple to a string, and once that was corrected they still only checked the outcome label and never the hint message, so they passed on code with backwards hints. After that I started asking what a test would still let through, not just whether it passed.*

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
*Answer: The habit I want to keep is staying in contact with the project at the moment I commit, instead of committing and moving on. I fixed one bug per commit, and before each one I asked questions about what had actually changed so I could see the difference and ask for an amend if it was not complete. That is exactly what happened with the hint bug: the first commit only swapped the message text, and because I asked about it I had it amended to also remove the string comparison, so the finished commit covers the whole problem instead of half of it. Underneath that habit are two smaller ones I want to keep, red testing before any fix, and writing prompts that are concise but still understandable.*
- What is one thing you would do differently next time you work with AI on a coding task?
*Answer: I would give more context up front and explain what I want more clearly. My prompts at the beginning of this project were short, and a few of them were short enough to be read the wrong way, which cost me work that had to be reverted. Being concise is still what I want, but concise is not the same as leaving out the part that says what is in scope and what is not. Next time I plan to say what I want changed, what I want left alone, and how I will know it worked, in the first message rather than the third.*
- In one or two sentences, describe how this project changed the way you think about AI generated code.
*Answer: This project changed how I work with Git more than anything else, because committing one verified fix at a time let me see each change reflected on its own and keep moving forward without getting distracted by code I had already confirmed was good. That turned out to be the thing that makes AI generated code manageable, since this app looked finished and even had passing tests while several parts of it were still wrong, and small verified commits are how I tell the working parts from the parts that only look working.*
