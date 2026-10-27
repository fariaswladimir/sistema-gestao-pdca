---
description: Escrever ou revisar a spec de uma fatia (o quê e por quê), sem decidir tecnologia.
---

1. Pergunte qual fatia (F00 a F10) se não foi informada. Leia @specs/README.md e a pasta da fatia.
2. Leia @specs/_glossario.md, @specs/_modelo-dados.md e @specs/_perfis-permissoes.md.
3. Se `spec.md` já existe, revise; senão, crie a partir de @specs/_templates/spec.md.
4. Garanta que a spec tenha: objetivo, perfis envolvidos, histórias, regras de negócio numeradas,
   fora do escopo, impacto em API/MCP, critério de pronto e questões em aberto.
5. Escreva ou revise `acceptance.feature` em Gherkin (português, `# language: pt`).
   Todo cenário deve ser verificável por teste automático. Inclua ao menos um cenário de permissão negativa.
6. Liste as questões em aberto marcadas com [DECIDIR] e PARE. Peça ao humano para responder e aprovar.
7. Só após aprovação explícita, mude o status para `Aprovada` e atualize a tabela em @specs/README.md.
