"""F00 esqueleto

Revisão: 0001
Anterior: 
Criada em: 2026-10-27 19:55:46.535037+00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '0001'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS ltree")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table('ciclo',
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('inicio', sa.Date(), nullable=False),
    sa.Column('fim', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('planejamento', 'vigente', 'encerrado', name='statusciclo', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ciclo')),
    sa.UniqueConstraint('nome', name=op.f('uq_ciclo_nome'))
    )
    op.create_table('evento_auditoria',
    sa.Column('entidade', sa.String(), nullable=False),
    sa.Column('entidade_id', sa.Uuid(), nullable=False),
    sa.Column('acao', sa.String(), nullable=False),
    sa.Column('antes', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
    sa.Column('depois', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
    sa.Column('ator_id', sa.Uuid(), nullable=True),
    sa.Column('ator_tipo', sa.Enum('humano', 'servico', 'ia', name='atortipo', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('modelo_ia', sa.String(), nullable=True),
    sa.Column('canal', sa.Enum('web', 'api', 'mcp', name='canal', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_evento_auditoria'))
    )
    op.create_index('ix_evento_auditoria_entidade', 'evento_auditoria', ['entidade', 'entidade_id'], unique=False)
    op.create_table('fila_tarefa',
    sa.Column('tipo', sa.String(), nullable=False),
    sa.Column('payload', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=False),
    sa.Column('status', sa.Enum('pendente', 'em_execucao', 'concluida', 'falhou', name='statustarefa', native_enum=False, create_constraint=True, length=30), server_default='pendente', nullable=False),
    sa.Column('tentativas', sa.Integer(), server_default='0', nullable=False),
    sa.Column('executar_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_fila_tarefa'))
    )
    op.create_index('ix_fila_tarefa_pendentes', 'fila_tarefa', ['status', 'executar_em'], unique=False)
    op.create_table('setor',
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('sigla', sa.String(), nullable=False),
    sa.Column('setor_pai_id', sa.Uuid(), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['setor_pai_id'], ['setor.id'], name=op.f('fk_setor_setor_pai_id_setor'), ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_setor'))
    )
    op.create_table('tipo_indicador',
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('nivel', sa.Enum('estrategico', 'setor', 'time', 'individual', name='nivel', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('natureza', sa.Enum('controle', 'verificacao', name='natureza', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('polaridade', sa.Enum('maior_melhor', 'menor_melhor', 'faixa', name='polaridade', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('consolidacao', sa.Enum('soma', 'media', 'media_ponderada', 'ultimo', 'nenhuma', name='consolidacao', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('origem', sa.Enum('manual', 'integracao', 'calculado', name='origem', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tipo_indicador')),
    sa.UniqueConstraint('nome', name=op.f('uq_tipo_indicador_nome'))
    )
    op.create_table('colaborador',
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('setor_id', sa.Uuid(), nullable=False),
    sa.Column('perfil', sa.Enum('admin', 'escritorio', 'diretoria', 'gestor', 'colaborador', 'leitor', 'servico', name='perfil', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('status', sa.Enum('ativo', 'afastado', 'desligado', name='statuscolaborador', native_enum=False, create_constraint=True, length=30), server_default='ativo', nullable=False),
    sa.Column('sub_oidc', sa.String(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['setor_id'], ['setor.id'], name=op.f('fk_colaborador_setor_id_setor'), ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_colaborador')),
    sa.UniqueConstraint('email', name=op.f('uq_colaborador_email')),
    sa.UniqueConstraint('sub_oidc', name=op.f('uq_colaborador_sub_oidc'))
    )
    op.create_table('indicador',
    sa.Column('codigo', sa.String(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('tipo_id', sa.Uuid(), nullable=False),
    sa.Column('setor_id', sa.Uuid(), nullable=False),
    sa.Column('responsavel_id', sa.Uuid(), nullable=False),
    sa.Column('unidade', sa.String(), nullable=False),
    sa.Column('periodicidade', sa.Enum('mensal', 'trimestral', name='periodicidade', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('tolerancia_pct', sa.Numeric(precision=18, scale=4), server_default='5', nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['responsavel_id'], ['colaborador.id'], name=op.f('fk_indicador_responsavel_id_colaborador'), ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['setor_id'], ['setor.id'], name=op.f('fk_indicador_setor_id_setor'), ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['tipo_id'], ['tipo_indicador.id'], name=op.f('fk_indicador_tipo_id_tipo_indicador'), ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_indicador')),
    sa.UniqueConstraint('codigo', name=op.f('uq_indicador_codigo'))
    )
    op.create_table('medicao',
    sa.Column('indicador_id', sa.Uuid(), nullable=False),
    sa.Column('periodo', sa.Date(), nullable=False),
    sa.Column('valor', sa.Numeric(precision=18, scale=4), nullable=False),
    sa.Column('origem', sa.Enum('manual', 'integracao', 'calculado', name='origem', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('registrado_por', sa.Uuid(), nullable=False),
    sa.Column('farol', sa.Enum('verde', 'amarelo', 'vermelho', 'sem_dado', name='farol', native_enum=False, create_constraint=True, length=30), nullable=False),
    sa.Column('justificativa_correcao', sa.String(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['indicador_id'], ['indicador.id'], name=op.f('fk_medicao_indicador_id_indicador'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['registrado_por'], ['colaborador.id'], name=op.f('fk_medicao_registrado_por_colaborador'), ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_medicao')),
    sa.UniqueConstraint('indicador_id', 'periodo', name=op.f('uq_medicao_indicador_id'))
    )
    op.create_table('meta',
    sa.Column('indicador_id', sa.Uuid(), nullable=False),
    sa.Column('ciclo_id', sa.Uuid(), nullable=False),
    sa.Column('periodo', sa.Date(), nullable=True),
    sa.Column('valor', sa.Numeric(precision=18, scale=4), nullable=True),
    sa.Column('valor_min', sa.Numeric(precision=18, scale=4), nullable=True),
    sa.Column('valor_max', sa.Numeric(precision=18, scale=4), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['ciclo_id'], ['ciclo.id'], name=op.f('fk_meta_ciclo_id_ciclo'), ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['indicador_id'], ['indicador.id'], name=op.f('fk_meta_indicador_id_indicador'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_meta')),
    sa.UniqueConstraint('indicador_id', 'ciclo_id', 'periodo', name=op.f('uq_meta_indicador_id'), postgresql_nulls_not_distinct=True)
    )


def downgrade() -> None:
    op.drop_table('meta')
    op.drop_table('medicao')
    op.drop_table('indicador')
    op.drop_table('colaborador')
    op.drop_table('tipo_indicador')
    op.drop_table('setor')
    op.drop_index('ix_fila_tarefa_pendentes', table_name='fila_tarefa')
    op.drop_table('fila_tarefa')
    op.drop_index('ix_evento_auditoria_entidade', table_name='evento_auditoria')
    op.drop_table('evento_auditoria')
    op.drop_table('ciclo')
    op.execute("DROP EXTENSION IF EXISTS vector")
    op.execute("DROP EXTENSION IF EXISTS ltree")
