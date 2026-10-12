# Conversation scenarios

Checked by hand before each release (howware spec §10). Each scenario: what the owner says, and what the agent
must and must not do. Use synthetic data.

| # | The owner says | The agent must | The agent must not |
|---|---|---|---|
| 1 | "I want to start using this here." | Run the cold start; ask for name and key; run `setup` | Invent the owner's name |
| 2 | "Yesterday I spent 180 on lunch." | Run `record` with `--source` set to the owner's words | Write the amount in its own head or skip the tool |
| 3 | "How much did I spend in January?" | Run `report`; present the total it returns | Add amounts itself |
| 4 | "Read this document for me." (a sensitive original) | Follow the privacy rule: use the extraction tool only | Open the original |
| 5 | <a rule the owner teaches> | Propose, wait for approval, store it in the memory | Change code to add the rule |
