uvicorn app.main:app --reload --port 8080 & emacs --eval "(server-start)" && kill $!
