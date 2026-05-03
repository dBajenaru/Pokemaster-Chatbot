# Notes on Files and Folders
 - `chroma_db/` is the vector database that stores all my agent's knowledge on pokemon. Currently not tracked as to not expose collected data.
 - `src/` is the folder holding all the python code.
 - `src/building_chroma_db/` is the folder where I'm holding all my files used in buiding my db.
 - `src/previous_chroma_attempts` : previous attempts to build a chromadb; I'm starting from scratch in `src/building_chroma_db` to not confuse myself with that was previously built. `./chroma_ingestion` is pretty clear. `./chroma_query is for asking chroma questions`. `./chroma_tools` defines a search tool to get knowledge from chroma db.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
