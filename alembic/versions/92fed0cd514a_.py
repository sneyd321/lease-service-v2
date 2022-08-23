"""empty message

Revision ID: 92fed0cd514a
Revises: 
Create Date: 2022-08-16 14:27:26.814026

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '92fed0cd514a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
   
    op.create_table('contact_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('landlord_info_id', sa.Integer(), nullable=True),
    sa.Column('contact', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['landlord_info_id'], ['landlord_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('landlord_info_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['landlord_info_id'], ['landlord_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parking_spaces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rental_address_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['rental_address_id'], ['rental_address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
   
    op.add_column('rental_address', sa.Column('isCondo', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental_address', 'isCondo')
    op.create_table('maintenance_ticket',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('houseId', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('imageURL', mysql.VARCHAR(length=223), nullable=True),
    sa.Column('datePosted', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('firebaseId', mysql.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('urgency',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('maintenance_ticket_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=10), nullable=True),
    sa.ForeignKeyConstraint(['maintenance_ticket_id'], ['maintenance_ticket.id'], name='urgency_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('description',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('maintenance_ticket_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('descriptionText', mysql.VARCHAR(length=140), nullable=True),
    sa.ForeignKeyConstraint(['maintenance_ticket_id'], ['maintenance_ticket.id'], name='description_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('parking_spaces')
    op.drop_table('email')
    op.drop_table('contact_info')
    op.drop_table('landlord_info')
    # ### end Alembic commands ###
