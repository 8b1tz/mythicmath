# MythicMath

Repositorio principal com backend e frontend (submodulo).

**Atualize o frontend**

Para garantir que esta testando a versao mais recente do app, atualize o submodulo:

```powershell
git -C frontend fetch origin
git -C frontend reset --hard origin/main
git add frontend
git commit -m "Update front submodule"
```

> Atencao: esse comando descarta alteracoes locais dentro da pasta `frontend`.

**Backend (FastAPI)**

Se for testar no proprio celular usando o Expo Go, rode o backend exposto na rede local:

```powershell
.\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Isso permite acesso pela rede local (nao apenas no PC). Garanta que celular e PC estejam na mesma rede.
