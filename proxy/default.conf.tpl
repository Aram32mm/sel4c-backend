server {
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {
        if ($scheme = http) {
            return 301 https://$server_name$request_uri;
        }
        add_header Cache-Control private;
        add_header Cache-Control no-cache;
        add_header Cache-Control no-store;
        add_header Cache-Control must-revalidate;
        add_header Pragma no-cache;
        uwsgi_pass unix:///tmp/uwsgi.sock;
        include    /etc/nginx/uwsgi_params;
        proxy_read_timeout 1800;
        uwsgi_read_timeout 1800;

        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            #
            # Om nom nom cookies
            #
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, PUT, DELETE, OPTIONS';
            #
            # Custom headers and headers various browsers *should* be OK with but aren't
            #
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
            #
            # Tell client that this pre-flight info is valid for 20 days
            #
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            add_header Access-Control-Allow-Headers "Authorization";
            add_header Access-Control-Allow-Credentials "true";
            return 204;
        }
        if ($request_method = 'PUT') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }
        if ($request_method = 'PATCH') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }
        if ($request_method = 'POST') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }
        if ($request_method = 'GET') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }


        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }
}