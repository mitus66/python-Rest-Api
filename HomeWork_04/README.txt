Запуск:
docker build -t mywebapp .
docker run -p 3000:3000 -v $(pwd)/storage:/app/storage mywebapp

Або з docker-compose:
docker-compose up --build