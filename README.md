# SIPEI — Sistema Integrado de Plano Educacional Individualizado

Sistema web desenvolvido a partir das necessidades da CAPNE do IFBA, campus Porto Seguro. O objetivo é reunir em um só lugar os dados dos estudantes, os Planos Educacionais Individualizados (PEIs) e os registros de acompanhamento pedagógico, antes organizados em documentos Word.

Desenvolvido com **Python, Django, HTML e CSS**.

## Funcionalidades

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

Essas contas são apenas para testes locais. Não use essas senhas em um ambiente real.

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
- Layout responsivo para celular e computador.
- `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` podem ser configurados por variáveis de ambiente. Antes de publicar o sistema, é necessário revisar essas configurações de segurança.

## Situação atual

O sistema funciona em ambiente local, com dados fictícios para demonstração. Ainda são necessários testes adicionais, validação com a CAPNE e ajustes de segurança antes de uma possível implantação institucional.
