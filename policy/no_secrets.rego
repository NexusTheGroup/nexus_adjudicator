package nexus
violations[v] { v := msg }
suspect := {"AKIA[0-9A-Z]{16}","sk-[A-Za-z0-9]{20,}","AIza[0-9A-Za-z-_]{35}"}
msg := sprintf("potential secret pattern: %s", [r]) {
  some r; r := suspect[_]
  some f; f := input.changed[_]
  re_match(r, f)
}
allow { count(violations) == 0 }
