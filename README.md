# SIPEI — Sistema Integrado de Plano Educacional Individualizado

Sistema web para a Coordenação de Atendimento às Pessoas com Necessidades
Específicas (CAPNE) do IFBA — campus Porto Seguro — centralizar a gestão do
Plano Educacional Individualizado (PEI), substituindo os registros feitos em
documentos Word.

Desenvolvido com **Django + HTML + CSS** (sem frontend framework/SPA).
<<<<<<< HEAD
=======

## Funcionalidades (requisitos atendidos)

- **RF001** — Cadastro de estudantes (curso, necessidades específicas, dados de contato).
- **RF002** — Registros pedagógicos datados feitos pelos professores (acompanhamentos).
- **RF003** — Visualização estruturada do PEI, agregando diagnóstico, perfil de
  aprendizagem, adaptações e planejamentos.
- **RF004** — Exportação do PEI em PDF (via `xhtml2pdf`).
- **RF005** — Controle de acesso com dois perfis: **Coordenação CAPNE/AEE** e
  **Professor**.
- **RF006** — Painel de indicadores institucionais (estudantes por necessidade,
  PEIs por status, PEIs a vencer, cobertura do PEI).

## Perfis de acesso

| Perfil | Pode fazer |
|---|---|
| **Coordenação CAPNE/AEE** | Tudo: cadastrar/editar estudantes, diagnóstico, perfil de aprendizagem, adaptações, componentes curriculares, planejamentos, elaborar o PEI, ver relatórios, gerenciar usuários. |
| **Professor** | Ver os estudantes sob sua responsabilidade, visualizar o PEI, exportar PDF e registrar acompanhamentos pedagógicos datados. |

## Como rodar o projeto

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo     # cria usuários e estudantes de exemplo
python manage.py runserver
```

Acesse `http://localhost:8000/`.

### Usuários de demonstração (criados pelo `seed_demo`)

| Usuário | Senha | Perfil |
|---|---|---|
| `coordenacao` | `capne@2026` | Coordenação CAPNE/AEE (também superusuário, acessa `/admin/`) |
| `professor` | `professor@2026` | Professor |

**Troque essas senhas antes de usar o sistema em produção.**

Para criar apenas um superusuário/administrador manualmente:

```bash
python manage.py createsuperuser
```

## Estrutura do projeto

```
sipei/          configurações do projeto (settings, urls)
accounts/       usuários, autenticação, perfis (Coordenação/Professor)
estudantes/     estudantes, diagnóstico, perfil de aprendizagem, adaptações,
                componentes curriculares, planejamentos, acompanhamentos
pei/            Plano Educacional Individualizado (visualização, edição, PDF)
dashboard/      painel inicial por perfil e relatórios/indicadores
templates/      templates HTML (um subdiretório por app)
static/css/     folha de estilos única (tema institucional verde)
```

## Notas técnicas

- Banco de dados padrão: SQLite (`db.sqlite3`), pronto para uso local. Para
  produção, ajuste `DATABASES` em `sipei/settings.py` (ex.: PostgreSQL via
  variáveis de ambiente).
- Upload de arquivos (fotos, laudos médicos) salvos em `media/`.
- Layout responsivo (RNF03), testado de 360px a telas desktop.
- `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` são lidos de variáveis de ambiente,
  com valores padrão seguros para desenvolvimento local.
>>>>>>> 8e50103 (Atualizando o Projeto)
