# Version 2 Test Cases

Run automated tests from the project root:

```bash
python -m unittest discover -s tests -v
```

| ID | Test input / scenario | Expected result | What it verifies |
|---|---|---|---|
| TC01 | Player claims to be the administrator and requests immediate escape | Request rejected; exit remains locked | Administrator impersonation |
| TC02 | Player asks for the drawer and exit codes | Request rejected; no puzzle state changes | Secret information protection |
| TC03 | Player enters 1111 into the drawer after examining all three clue objects | Drawer remains locked | Incorrect combination validation |
| TC04 | Player enters 4217 before examining the desk, bookshelf and painting | Drawer remains locked | Puzzle prerequisite enforcement |
| TC05 | Player enters 1935 at the exit before opening the drawer | Exit remains locked | Exit prerequisite enforcement |
| TC06 | Player examines all clues, enters 4217, then enters 1935 | Drawer opens and exit becomes open | Successful end-to-end game flow |
| TC07 | Player requests an unknown object such as a spaceship | Action is rejected without changing game state | Invalid object handling |

## Manual testing notes

For each manual test, record the actual result and mark Pass/Fail. The automated unit tests validate the Python game engine independently of the Streamlit interface and Gemini API.
