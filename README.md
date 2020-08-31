# uniclub-back

tech:
    web_server: uwsgi
    app: django
    db: postgres
    back_tasks: celery, redis, rabbit
    monitoring_tasks: flower
    container: dockercompose

start:
    sudo docker-compose up -d --build
