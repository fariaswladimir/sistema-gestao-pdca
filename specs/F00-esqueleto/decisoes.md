# F00-esqueleto – Decisões

| Data | Decisão | Motivo |
| --- | --- | --- |
| 2026-10-27 | Login na v1 com usuário e senha próprios do sistema, sem SSO corporativo. | Decisão do dono do produto na aprovação da F00. |
| 2026-10-27 | Keycloak como provedor de identidade também em homologação e produção, com usuários locais. | Mantém OIDC do plano; Keycloak já entrega hash de senha, redefinição e bloqueio por força bruta; federar com Entra ID depois não muda o código. |
| 2026-10-27 | Homologação e produção em servidor interno com Docker Compose. | Decisão do dono do produto na aprovação da F00. |
| 2026-10-27 | Tolerância padrão de 5% da meta confirmada. | Decisão do dono do produto na aprovação da F00. |
