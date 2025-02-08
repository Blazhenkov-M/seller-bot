

# async def get_admins():
#     async with aiosqlite.connect("database.db") as db:
#         async with db.execute("SELECT tg_id FROM admins") as cursor:
#             return {row[0] async for row in cursor}  # Возвращаем set ID
