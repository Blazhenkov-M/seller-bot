docker run --name seller_bot_db \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=seller_bot_db \
-p 5434:5432 \
-d postgres:latest


docker run -d -p 6379:6379 redis


https://t.me/Finsell_consult_bot/
