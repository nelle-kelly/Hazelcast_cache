<h1>Comment Django interagit avec le cache?</h1>

<p>Nous allons tester ce que fait Django avec le cache lorsqu'un queryset est executé et chercher un element specifique dans une structure de données Hazelcast en utilisant PostgreSQL.
<br/>
Nous allons principalement utiliser la structure Map
<br/>

</p>

<p>Nous allons creer un model "Person"(first_name, last_name,phone, email) et inserer des objects dans la base de données :
<br/>

<img src="capture/image2.png"> <br/>
Ce code fait l'insertion des données dans la base et specifit à chaque fois l'objet ajouté.
<img src="capture/image1.png"> 
<br/>
<h3> nous allons Récupérer la liste des objets insérés et manipuler le comportement du cache de Django lors de l'exécution du queryset Person.objects(). </h3> 

 <br/>
 Alors Django propose le QuerySet caching. Cependant le systeme de cache des Queryset n'est pas activé par defaut dans Django et il n'existe pas de méthode native directement disponible. <br/>
 Donc si nous recuperons les données de notre base en executons le queryset Person.object(), il y'aura juste un deplacement vers notre base de données sans passer par le cache </p>

 <p>Nous allons utiliser le systeme de cache de Django pour faire un cache des Queryset avec le module cache de django.core.cache; et utiliser notre cache personnaliser.
<br/>
 <img src="capture/image3.png"> <br>
 le parametre LOCATION specifie l'adresse où se trouve le server de cache auquel notre application Django va se connecter pour stocker et récupérer des données en cache.
 <br/>
Nous allons stocker les elements dans le cache de Django lors de l'execution du queryset Person.objec()<br>
<img src="capture/image4.png"> <br>

Les codes qui suivents permettent de recupérer la liste des objets à partir du cache et cacher des élements dans le cache Hazelcast: <br>
<img src="capture/image5.png">
 