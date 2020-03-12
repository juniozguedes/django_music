## Features

-  [Docker](https://www.docker.com/docker-community)

-  [PostgreSQL](https://www.postgresql.org/)

-  [Django](https://www.djangoproject.com/)


## Requerimentos
-  [Docker](https://www.docker.com/)

#### Subindo imagem Docker:

  

```bash

sudo docker-compose up --build

```

  

#### Rodando Migrations

  

```bash

sudo docker-compose run web python manage.py migrate

sudo docker-compose up -d --build

```
  <h4><i>A aplicação rodará em:</i> http://0.0.0.0:8000/</h4>


## Rotas
<h3> A idéia é que a API procure sempre no banco local por resultados, ao não encontrar, a mesma varre a API do deezer e cadastra no nosso banco os resultados encontrados</h3>
<p>Foram inseridos métodos de GET para que a API possa ser usada também pelo navegador para usuários que não possuem Postman</p>
<p>Os modelos possuem id extra de acordo com o id usado pelo Deezer para unificação de dados</p>

### CRUD Artistas

  

* Rota apenas para Artistas. Podem ser executadas pelo navegador ou Postman <strong>{{local}} = 0.0.0.0:8000</strong>

Método | URI | Params | Descrição | Ex.:
--- | --- | --- | --- | ---
*GET* | `{{local}}/artists/all` | NA | Retorna todos os artistas cadastrados no bd | ****
*GET* | `{{local}}/artists/getname/{{artist_name}}` | NA | Retorna artista por nome | `{{local}}/artists/getname/Black Sabb`
*GET* | `{{local}}/artists/getid/{{artist_id}}` | NA | Retorna artista por id | `{{local}}/artists/getid/15844`
*GET* | `{{local}}/artists/add/?name={{artist_name}}` | **name** | Adiciona artista por nome do artista | `{{local}}/artists/add/?name=Lil Peep`
*GET* | `{{local}}/artists/update/?name={{artist_name}}&artist_id={{artist_id}}` | **name** // **artist_id** | Atualiza nome do artista ao passar novo nome e ID do artista | `{{local}}/artists/update/?name=Banda do Menino&artist_id=OWFGYSBRV6D8LTJD9UMLY6C2QR0`
*GET* | `{{local}}/artists/delete/?artist_id={{artist_id}}` | **artist_id** | Deleta artista por ID do artista | `{{local}}/artists/delete/?artist_id=OWFGYSBRV6D8LTJD9UMLY6C2QR0`

### CRUD Albums

  

* Rota apenas para Albums. Podem ser executadas pelo navegador ou Postman <strong>{{local}} = 0.0.0.0:8000</strong>

Método | URI | Params | Descrição | Ex.:
--- | --- | --- | --- | ---
*GET* | `{{local}}/albums/all` | NA | Retorna todos os albums cadastrados no bd | ****
*GET* | `{{local}}/albums/getname/{{album_name}}` | NA | Retorna album por nome | `{{local}}/albums/getname/Random Access`
*GET* | `{{local}}/albums/getid/{{album_id}}` | NA | Retorna album por id | `{{local}}/albums/getid/299827`
*GET* | `{{local}}/albums/add/?name={{album_name}}&artist_id={{artist_id}}` | **name** // **artist_id** | Adiciona album por nome do album e id do artista | `{{local}}/albums/add/?name=Aerodynamic&artist_id=27`
*GET* | `{{local}}/albums/update/?name={{album_name}}&album_id={{album_id}}` | **name** // **album_id** | Atualiza nome do album ao passar novo nome e ID do album | `{{local}}/albums/update/?name=Freakyyy  Styleyy&album_id=299827`
*GET* | `{{local}}/albums/delete/?album_id={{album_id}}` | **album_id** | Deleta album por ID do album | `{{local}}/albums/delete/?album_id=90949`


  

## :memo: License
  
Feito com ♥ por Wellington Guedes :wave: [Linkedin](https://www.linkedin.com/in/wellington-guedes-6321b249/)