# ProjetBDD

```Lien Rapport : ``` https://www.overleaf.com/2575596781dzpzqywnxrbz

```Lien diagramme : ``` https://lucid.app/lucidchart/674c140e-a4a1-4947-941c-0604ebc53ed2/edit?docId=674c140e-a4a1-4947-941c-0604ebc53ed2&shared=true&invitationId=inv_792710c9-f42c-4286-b3d7-2cd81bf38ae3&page=0_0#


lancer la bd postgres :  
   ```sudo -u postgres -i```  
    ```cd chemin/dossier```  
     ```psql```  
     ```DROP DATABASE dossier_medical;``` -- supprime la db  
     ```CREATE DATABASE dossier_medical;``` -- cree la db  
     ```psql -d dossier_medical -f dossier_medical.sql``` -- cree les tableau dans le db  
     ```psql -d dossier_medical``` -- acceder a la db
    ```\d``` -- permet de voir les tableau
