# MythicMath

Repositório principal com backend e frontend (submódulo).

**Atualize o frontend**  
Para garantir que está testando a versão mais recente do app, atualize o submódulo:

```powershell
git submodule update --remote --merge
git add frontend
git commit -m "Update front submodule"
```

**Backend (FastAPI)**  
Se for testar no próprio celular usando o Expo Go, rode o backend exposto na rede local:

```powershell
.\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Isso permite acesso pela rede local (não apenas no PC). Garanta que celular e PC estejam na mesma rede.
