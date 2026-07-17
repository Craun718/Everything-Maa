# Recovery Policy

Use this contract for every failed observation, tool call, edit, or test:

```yaml
failure: concise symptom
root cause: confirmed cause or bounded hypothesis
safe retry: one action that changes the conditions or gathers new evidence
evidence_expected: result that would confirm or reject the hypothesis
retry_limit: finite count
stop condition: condition that forbids another retry
fallback: replan | use-another-tool | request-user | stop
```

## Rules

- Re-observe before retrying after navigation, scrolling, timing changes, or unexpected UI output.
- Change one relevant condition per retry so the result is attributable.
- Do not repeat an unchanged failed action.
- Do not retry a resource-consuming or destructive action when its outcome is unknown.
- Use a non-mutating probe before retrying a click, confirmation, purchase, battle, or item consumption.
- Replan when observed states contradict the designed state machine.
- Request user input when a material product or safety decision cannot be inferred.
- Stop when the retry limit is reached, no safe observation is available, or the next action would cross the task's authority boundary.

Report the latest stable state, attempted recoveries, preserved artifacts, and the smallest action that could unblock the task.
