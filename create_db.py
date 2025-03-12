from app import app, db
from sqlalchemy import inspect

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

    # Additional code to check if tables exist and create them if they don't maybe for PostgreSQL
    # binds = app.config.get("SQLALCHEMY_BINDS", {})
    # for bind_key, uri in binds.items():
    #     engine = db.engines[bind_key]
    #     db.metadata.create_all(engine)

    
    
    # default_engine = db.engine
    # default_inspector = inspect(default_engine)


    # # Gather tables that belong to the default bind (i.e. without a bind_key).
    # default_tables = [t for t in db.metadata.sorted_tables if t.info.get('bind_key') is None]
    # for table in default_tables:
    #     if default_inspector.has_table(table.name):
    #         print(f"Table '{table.name}' already exists on the default bind.")
    #     else:
    #         table.create(default_engine)
    #         print(f"Table '{table.name}' created on the default bind.")


    # binds = app.config.get('SQLALCHEMY_BINDS', {})
    # for bind_key in binds.keys():
    #     engine = db.engines[bind_key]
    #     inspector = inspect(engine)
    #     # Gather tables that are assigned to this bind_key.
    #     bind_tables = [t for t in db.metadata.sorted_tables if t.info.get('bind_key') == bind_key]
    #     for table in bind_tables:
    #         if inspector.has_table(table.name):
    #             print(f"Table '{table.name}' already exists on bind '{bind_key}'.")
    #         else:
    #             table.create(engine)
    #             print(f"Table '{table.name}' created on bind '{bind_key}'.")
    
    # print("Database table check/creation completed!")





    