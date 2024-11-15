def print_sql(stmt):
    print(stmt.compile(compile_kwargs={"literal_binds": True}))
