# Retomada — CP-TCC-001

Leia `ESTADO_EXECUCAO.json`, `LOG_EXECUCAO.md` e a fila derivada do plano canônico.
Confira `git status`, `git log -5 --oneline` e o HEAD observado `d3c5c2c86e93c9c66fbc3f8062590d8359aa370e`.
Branch: `feat/tcc-camila-cardiovascular-2014-2024`. Não recriar branch nem repetir frentes concluídas.

Última unidade confirmada: Cadastro e barreira populacional integrados; POPSVS, pilotos CNES e SIH e domínios SIGTAP conferidos; investigação I50 executável.

Próxima unidade exata: **Restaurar as edições federais do SIM por hash, primeiro 2022; executar a dupla leitura. Prosseguir por competência com cobertura e edição verificadas.**.

Para o TCC, usar os quatro checkpoints e os dois volumes externos. Os comandos, hashes e condições de retomada estão em `docs/estudos/tcc_camila/README.md` e `config/estudos/`.
Não promover staging incompleto. Aprovação funcional está em `DECISOES_R15.md`.
Gate científico/humano não é substituído por teste sintético.

Checkpoint: `python scripts/registrar_checkpoint_implementacao.py --checkpoint CP-IMP-NNN --unidade 'resultado comprovado' --proxima 'ação concreta'`.
Atualize estados com `--estado ID=PARCIAL` e bloqueio com `--bloqueio 'ID=motivo'`.
