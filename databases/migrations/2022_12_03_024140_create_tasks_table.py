"""CreateTasksTable Migration."""

from masoniteorm.migrations import Migration


class CreateTasksTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("tasks") as table:
            table.increments("id")
            table.string("title")
            table.string("description", nullable=True)
            table.boolean("done")
            table.boolean("favorite")
            table.integer('owner_id').unsigned()
            table.foreign('owner_id').references('id').on('users')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("tasks")
