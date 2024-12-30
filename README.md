# Frontend UI

![Screenshot (104)](https://github.com/user-attachments/assets/5f33def9-9edf-40b7-88c1-a04f329c763b)

### You can type `help` to see how you can filter the products. 

![Screenshot (106)](https://github.com/user-attachments/assets/dd63c621-6536-478d-a1a8-d918ae1bfef7)

# Installation and Execution

## Backend

1. Ensure pipenv is installed and it is added to `PATH`.

```
pip install pipenv
```

2. Ensure that you are in the directory with `pipfile.lock`. Install the dependencies required for the Backend.

```
pipenv sync
cd backend
```

3. Run migrations to set up the database schema

```
python manage.py makemigrations
python manage.py migrate
```

4. Use the provided script to populate the database with mock product entries

```
python manage.py shell
>>> from ecommerce.scripts import populate_products
>>> populate_products()
```

Run the script.

```
python manage.py runserver
```

## Frontend

1. Go to the frontend directory and install dependencies with `npm`. 

```
cd frontend
npm install
```

2. Run the script.

```
npm run dev
```

