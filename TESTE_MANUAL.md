# Guia de Teste Manual - Sistema de Convites QR Code

## Objetivo
Testar o fluxo completo do sistema de convites: criar → enviar → validar

## Pré-requisitos

1. Servidor rodando: `python main.py` ou `uvicorn main:app --reload`
2. Acesso ao navegador: http://localhost:8000

## Credenciais de Teste

- **Admin**: `admin` / `admin123`
- **Usuário**: `user` / `user123`

## Casos de Teste

### 1. Teste de Login ✓

**Objetivo**: Verificar autenticação básica

**Passos**:
1. Acesse http://localhost:8000
2. Digite usuário: `admin`
3. Digite senha: `admin123`
4. Clique em "Entrar"

**Resultado Esperado**:
- ✓ Redirecionamento para dashboard
- ✓ Mensagem de boas-vindas com nome do usuário
- ✓ Botão "Sair" visível

**Critérios de Sucesso**:
- [ ] Login realizado em < 1s
- [ ] Interface clara e intuitiva
- [ ] Sem erros no console do navegador

---

### 2. Teste do Dashboard ✓

**Objetivo**: Verificar visualização de estatísticas

**Passos**:
1. Após login, observe o dashboard
2. Verifique os cards: "Criar Convite", "Validar Convite", "Listar Convites"
3. Verifique estatísticas: Total, Validados, Pendentes

**Resultado Esperado**:
- ✓ Cards bem formatados e responsivos
- ✓ Estatísticas carregadas corretamente
- ✓ Design limpo e profissional

**Critérios de Sucesso**:
- [ ] Estatísticas carregadas em < 1s
- [ ] Layout responsivo (testar em mobile)
- [ ] Dados sincronizados

---

### 3. Teste de Criação de Convite ✓

**Objetivo**: Criar convite e gerar QR Code

**Passos**:
1. No dashboard, clique em "Criar Novo Convite"
2. Preencha: "Festa de Teste - João Silva - 25/11/2025 - 20h"
3. Clique em "Gerar QR Code"
4. Aguarde o QR Code aparecer

**Resultado Esperado**:
- ✓ QR Code gerado e exibido
- ✓ Código do convite visível
- ✓ Informações corretas exibidas
- ✓ Botões "Baixar" e "Compartilhar" funcionais

**Critérios de Sucesso**:
- [ ] QR Code gerado em < 1s
- [ ] Download funciona corretamente
- [ ] Imagem PNG válida
- [ ] Código único gerado

**Ações Adicionais**:
- [ ] Clique em "Baixar QR Code" e verifique o arquivo
- [ ] Anote o código do convite: `_______________`

---

### 4. Teste de Validação de Convite ✓

**Objetivo**: Validar convite através do QR Code

**Passos**:
1. No dashboard, clique em "Validar Convite"
2. Faça upload da imagem do QR Code gerado anteriormente
3. Clique em "Validar Convite"
4. Verifique o resultado

**Resultado Esperado**:
- ✓ Convite validado com sucesso
- ✓ Badge "Validado" exibido
- ✓ Informações corretas exibidas
- ✓ Data/hora de validação registrada

**Critérios de Sucesso**:
- [ ] Validação realizada em < 1s
- [ ] Dados correspondem ao convite criado
- [ ] Interface clara de sucesso/erro
- [ ] Feedback visual adequado

---

### 5. Teste de Listagem de Convites ✓

**Objetivo**: Visualizar todos os convites criados

**Passos**:
1. No dashboard, clique em "Ver Todos"
2. Observe a lista de convites
3. Use o campo de busca para filtrar
4. Use o filtro de status (Validados/Pendentes)

**Resultado Esperado**:
- ✓ Lista completa de convites exibida
- ✓ Filtros funcionam corretamente
- ✓ Badges de status corretos
- ✓ Informações completas de cada convite

**Critérios de Sucesso**:
- [ ] Lista carregada em < 1s
- [ ] Busca funciona instantaneamente
- [ ] Filtros aplicam corretamente
- [ ] Paginação/scroll suave

---

### 6. Teste de Responsividade 📱

**Objetivo**: Verificar design responsivo

**Passos**:
1. Teste em diferentes tamanhos de tela:
   - Desktop (1920x1080)
   - Tablet (768x1024)
   - Mobile (375x667)
2. Verifique todas as telas

**Resultado Esperado**:
- ✓ Layout se adapta corretamente
- ✓ Texto legível em todos os tamanhos
- ✓ Botões acessíveis
- ✓ Sem scroll horizontal

**Critérios de Sucesso**:
- [ ] Todas as funcionalidades acessíveis em mobile
- [ ] Design consistente
- [ ] Sem elementos quebrados

---

### 7. Teste de Performance ⚡

**Objetivo**: Verificar tempos de resposta

**Passos**:
1. Abra DevTools (F12) → Network
2. Execute as operações principais
3. Observe os tempos de resposta

**Critérios de Sucesso**:
- [ ] Criar convite: < 1s
- [ ] Validar convite: < 1s
- [ ] Listar convites: < 1s
- [ ] Carregar página: < 2s

**Registros**:
- Criar convite: _______ ms
- Validar convite: _______ ms
- Listar convites: _______ ms

---

### 8. Teste de Fluxo Completo 🔄

**Objetivo**: Executar o fluxo completo sem falhas

**Passos**:
1. Login → Dashboard → Criar Convite
2. Baixar QR Code gerado
3. Validar o QR Code baixado
4. Verificar na lista que está validado
5. Logout

**Resultado Esperado**:
- ✓ Fluxo completo sem erros
- ✓ Dados consistentes em todas as telas
- ✓ Experiência fluida

**Critérios de Sucesso**:
- [ ] Zero falhas críticas
- [ ] Dados sincronizados
- [ ] Navegação intuitiva
- [ ] Tempo total < 3 minutos

---

### 9. Teste de Erros e Edge Cases ⚠️

**Objetivo**: Verificar tratamento de erros

**Passos**:
1. Tente validar um QR Code inválido (imagem aleatória)
2. Tente criar convite com campo vazio
3. Tente acessar convite inexistente
4. Teste com internet lenta (DevTools → Network → Slow 3G)

**Resultado Esperado**:
- ✓ Mensagens de erro claras
- ✓ Sistema não quebra
- ✓ Feedback apropriado ao usuário
- ✓ Loading states visíveis

**Critérios de Sucesso**:
- [ ] Erros bem tratados
- [ ] Mensagens compreensíveis
- [ ] Sistema continua funcional

---

## Checklist de Feedback do Usuário

Por favor, avalie cada aspecto de 1 a 5:

### Funcionalidade
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Sistema funciona conforme esperado
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Fluxo de criação de convites
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Fluxo de validação de convites

### Usabilidade
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Interface intuitiva
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Facilidade de navegação
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Clareza das informações

### Design
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Aparência visual
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Responsividade
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Consistência

### Performance
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Velocidade de resposta
- [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  - Fluidez da navegação

---

## Comentários e Sugestões

**O que você mais gostou?**
_____________________________________________
_____________________________________________

**O que precisa melhorar?**
_____________________________________________
_____________________________________________

**Bugs encontrados:**
_____________________________________________
_____________________________________________

**Sugestões de novas funcionalidades:**
_____________________________________________
_____________________________________________

---

## Meta de Aprovação

**Objetivo**: Feedback positivo de pelo menos 70% dos testadores

- Total de testadores: _____
- Aprovações (nota ≥ 4): _____
- Taxa de aprovação: _____%

✅ Meta atingida: [ ] SIM  [ ] NÃO

---

## Assinatura do Testador

Nome: _______________________________
Data: _______________________________
Versão testada: 1.0.0
