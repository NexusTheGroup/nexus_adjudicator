package nexus
default allow = false
violations[v] { v := msg }

required_dirs := {"policy","tools",".github"}
forbidden_paths := {".env","id_rsa","secrets.yaml"}

allow { count(violations) == 0 }

msg := sprintf("missing required dir: %s", [d]) { d := required_dirs[_]; not input_has_dir(d) }
msg := sprintf("forbidden file path present: %s", [p]) { p := forbidden_paths[_]; input_has_path(p) }

input_has_dir(d) { some f; f := input.changed[_]; startswith(f, d) }
input_has_path(p){ some f; f := input.changed[_]; f == p }
