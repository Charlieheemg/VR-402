#!/bin/zsh
cd "${0:A:h}"
if curl --silent --fail http://127.0.0.1:8765/demo/ >/dev/null; then
  open http://127.0.0.1:8765/demo/
else
  open http://127.0.0.1:8765/demo/
  python3 serve.py
fi
