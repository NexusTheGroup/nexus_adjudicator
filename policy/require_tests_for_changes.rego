package nexus
violations[v] { v := msg }
msg := "changes under src/ without corresponding tests/" {
  some f
  f := input.changed[_]
  startswith(f, "src/")
  not input.has_tests_change
}
allow { count(violations) == 0 }
