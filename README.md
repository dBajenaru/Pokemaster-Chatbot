# Pokemaster Chatbot

This is a prototype project for personal learning.

## How to run

This project has two components: `frontend/` and `backend/`. Both of these have servers that need to be started seperately. The simplest way to do this is to view them as serperate projects.

### Linux

Start both command blocks in the project root `pokemaster/`. For the backend, you will need to fill in the `.env` file with AZURE\_PROJECT\_ENDPOINT and AZURE\_DEPLOYMENT\_NAME. You will also need to create your own chromadb to have specialized knowledge.

Starting the backend:
```{bash}
cd backend
touch .env
source poke/bin/activate
pip install requirements.txt
python3 -m src.api.api
```

Starting the frontend:
```{bash}
cd frontend
npm run dev
```

