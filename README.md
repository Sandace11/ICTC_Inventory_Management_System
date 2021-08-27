# Inventory Management System (Storage)

Inventory items can divided into categories having category-specific properties which can be custom-added by the user.

This is basicaly a CRUD system for Floor, Room, Category, Item and User.

It also has an advanced filter page with intuitive tables and add/edit/delete facility from the table itself.

CSV files are also available for download.

### Usage

- `pip install -r requirements.txt`
- Create a postgres database and fill the credentials in settings.py within DATABASES
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser` and add an admin user
- `python manage.py runserver`
- Open 127.0.0.1:8000 on your browser and login with admin credentials

### Screenshots


![Screen Shot 2019-11-06 at 23 06 00](https://user-images.githubusercontent.com/43087414/68321668-3765ff00-00ea-11ea-9b3e-ef5942e9a050.png)
![Screen Shot 2019-11-06 at 23 06 15](https://user-images.githubusercontent.com/43087414/68321670-3765ff00-00ea-11ea-9403-7610b4a1ede0.png)
![Screen Shot 2019-11-06 at 23 06 45](https://user-images.githubusercontent.com/43087414/68321671-37fe9580-00ea-11ea-8147-af2730ae17c5.png)
![Screen Shot 2019-11-06 at 23 06 58](https://user-images.githubusercontent.com/43087414/68321672-37fe9580-00ea-11ea-8f17-bf866140a06b.png)
![Screen Shot 2019-11-06 at 23 41 36](https://user-images.githubusercontent.com/43087414/68324235-0fc56580-00ef-11ea-97e5-0fd8df4d2b70.png)


