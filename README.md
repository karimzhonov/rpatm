# ИНДЕКС ЧЕЛОВЕЧЕСКОГО ДОСТОИНСТВА

## Запуск проекта:

Проект запускается с помощью docker-compose:

    docker-compose --file docker-compose.prod.yml up --build -d

После запуска docker-compose backend части будеть крутиться 8000 порту

## Настройка nginx

    upstream backend {
        server <Хост который крутится backend (Например: localhost:8000)>;
    }

    server {

        listen 80 default_server;
        listen [::]:80 default_server;

        location / {
            root <Путь до папки frontend/dist/>;
            try_files $uri $uri/ /index.html;
        }
    
        location  /api/ {
            proxy_pass http://backend/api/;
            
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass_header Authorization;
            proxy_pass_header Accept-Language;
        }
        
        location  /admin/ {
            proxy_pass http://backend/admin/;
            
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass_header Authorization;
            proxy_pass_header Accept-Language;
        }
    
        location /api/static/ {
            alias <Путь до папки backend/static/>;
        }
    
        location /api/media/ {
            alias <Путь до папки backend/media/>;
        }
    }
