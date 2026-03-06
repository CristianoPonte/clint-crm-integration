# Aprendizados para Próximas Execucoes

## O que eu gostaria de saber antes de iniciar
- Qual e o payload real mais recente do Manychat (amostra completa de producao).
- Qual campo e fonte de verdade para telefone (ex.: `whatsapp_phone`) e quais fallbacks estao permitidos.
- Se o Manychat envia ou nao token de autenticacao/header para o webhook.
- Qual estrategia oficial de token Clint no n8n (credential, env, ou header temporario).
- Qual workflow com mesmo webhook path ja esta ativo (para evitar conflito na ativacao).
- Quais codigos HTTP precisam ser retornados para o sistema chamador em cada tipo de erro.
- Se execucoes com erro de negocio devem aparecer como `error` no n8n (alem da resposta HTTP).
- Quais campos customizados do Manychat mudaram de nome desde o ultimo deploy.
- Qual regra de deduplicacao vigente (email primeiro, telefone depois, outras excecoes).
- Quais testes de smoke sao obrigatorios apos deploy (novo contato, contato existente, payload invalido).
