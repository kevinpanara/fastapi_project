"""model added

Revision ID: e2cf5976c48e
Revises: 
Create Date: 2024-01-04 14:19:52.158564

"""
import sqlalchemy as sa
from alembic import op

from app.libs.utils import generate_id
from app.models import AdminUserModel, AdminUserRoleModel, OperationModel, RoleModel
from app.routers.admin.crud.admin_users.admin_users import create_password
from app.seeds import data

# revision identifiers, used by Alembic.
revision = "e2cf5976c48e"
down_revision = None
branch_labels = None
depends_on = None


def seed():
    for operation in data.operations:
        operation_id = generate_id()
        db_operation = OperationModel(
            id=operation_id,
            slug=operation["name"],
            name=operation["name"],
            order_index=operation["index"],
        )
        op.bulk_insert(OperationModel.__table__, [db_operation.__dict__])

        for sub_operation in operation["sub_operations"]:
            sub_operation_id = generate_id()
            db_sub_operation = OperationModel(
                id=sub_operation_id,
                slug=sub_operation["slug"],
                name=sub_operation["name"],
                order_index=sub_operation["index"],
                parent_id=operation_id,
            )
            op.bulk_insert(OperationModel.__table__, [db_sub_operation.__dict__])

    super_user = data.super_user
    admin_user_id = generate_id()
    db_user = AdminUserModel(
        id=admin_user_id,
        name=super_user["name"],
        email=super_user["email"],
        password=create_password(super_user["password"]),
    )
    op.bulk_insert(AdminUserModel.__table__, [db_user.__dict__])

    role_id = generate_id()
    db_role = RoleModel(
        id=role_id,
        slug="Super Admin",
        name="Super Admin",
        editable=False,
    )
    op.bulk_insert(RoleModel.__table__, [db_role.__dict__])

    user_role_id = generate_id()
    db_user_role = AdminUserRoleModel(
        id=user_role_id,
        admin_user_id=admin_user_id,
        role_id=role_id,
    )
    op.bulk_insert(AdminUserRoleModel.__table__, [db_user_role.__dict__])

    role_id = generate_id()
    db_role = RoleModel(
        id=role_id,
        slug="Admin",
        name="Admin",
        editable=True,
    )
    op.bulk_insert(RoleModel.__table__, [db_role.__dict__])


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "admin_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_admin_users_email"), "admin_users", ["email"], unique=False
    )
    op.create_index(
        op.f("ix_admin_users_is_deleted"), "admin_users", ["is_deleted"], unique=False
    )
    op.create_table(
        "module_types",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_module_types_is_deleted"), "module_types", ["is_deleted"], unique=False
    )
    op.create_table(
        "operations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("slug", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_operations_order_index"), "operations", ["order_index"], unique=False
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("slug", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("editable", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_roles_is_deleted"), "roles", ["is_deleted"], unique=False)
    op.create_table(
        "admin_user_otps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("otp", sa.String(length=6), nullable=False),
        sa.Column("is_redeemed", sa.Boolean(), nullable=False),
        sa.Column("admin_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["admin_user_id"],
            ["admin_users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_admin_user_otps_is_redeemed"),
        "admin_user_otps",
        ["is_redeemed"],
        unique=False,
    )
    op.create_table(
        "admin_user_roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("admin_user_id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["admin_user_id"],
            ["admin_users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PLANNING",
                "INPROGRESS",
                "COMPLETED",
                "ONHOLD",
                "CANCELLED",
                name="projectstatusenum",
            ),
            nullable=False,
        ),
        sa.Column("manager_id", sa.String(length=36), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["manager_id"],
            ["admin_users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_projects_is_deleted"), "projects", ["is_deleted"], unique=False
    )
    op.create_table(
        "role_operations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("operation_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["operation_id"],
            ["operations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "modules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("module_type_id", sa.String(length=36), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["module_type_id"],
            ["module_types.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_modules_is_deleted"), "modules", ["is_deleted"], unique=False
    )
    op.create_table(
        "project_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("admin_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["admin_user_id"],
            ["admin_users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.Enum("PENDING", "INPROGRESS", "COMPLETED", name="taskstatusenum"),
            nullable=False,
        ),
        sa.Column("module_id", sa.String(length=36), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["modules.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_is_deleted"), "tasks", ["is_deleted"], unique=False)
    op.create_table(
        "issues",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column(
            "status", sa.Enum("OPEN", "CLOSED", name="issuestatusenum"), nullable=False
        ),
        sa.Column(
            "priority",
            sa.Enum("LOW", "MEDIUM", "HIGH", name="issuepriorityenum"),
            nullable=False,
        ),
        sa.Column("task_id", sa.String(length=36), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_issues_is_deleted"), "issues", ["is_deleted"], unique=False
    )
    op.create_table(
        "issue_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("issue_id", sa.String(length=36), nullable=False),
        sa.Column("admin_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["admin_user_id"],
            ["admin_users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["issue_id"],
            ["issues.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###

    seed()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("issue_users")
    op.drop_index(op.f("ix_issues_is_deleted"), table_name="issues")
    op.drop_table("issues")
    op.drop_index(op.f("ix_tasks_is_deleted"), table_name="tasks")
    op.drop_table("tasks")
    op.drop_table("project_users")
    op.drop_index(op.f("ix_modules_is_deleted"), table_name="modules")
    op.drop_table("modules")
    op.drop_table("role_operations")
    op.drop_index(op.f("ix_projects_is_deleted"), table_name="projects")
    op.drop_table("projects")
    op.drop_table("admin_user_roles")
    op.drop_index(op.f("ix_admin_user_otps_is_redeemed"), table_name="admin_user_otps")
    op.drop_table("admin_user_otps")
    op.drop_index(op.f("ix_roles_is_deleted"), table_name="roles")
    op.drop_table("roles")
    op.drop_index(op.f("ix_operations_order_index"), table_name="operations")
    op.drop_table("operations")
    op.drop_index(op.f("ix_module_types_is_deleted"), table_name="module_types")
    op.drop_table("module_types")
    op.drop_index(op.f("ix_admin_users_is_deleted"), table_name="admin_users")
    op.drop_index(op.f("ix_admin_users_email"), table_name="admin_users")
    op.drop_table("admin_users")
    # ### end Alembic commands ###
