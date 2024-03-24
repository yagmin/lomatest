# Jim Yagmin's Loma Take Home

### Requirements

- Python 3
- Postgres
- React
- npm


Clone repository:
```
$ git clone ...
```

### Project Notes
I used Flask for my backend as I have more recent familiarity building with it and I wanted to minimize time spent on boilerplate. Unfortunately, Flask doesn't come with an integrated database so running the test suite requires Postgres to be installed. I could have created a Docker instance, but in the interest of time I used what was easiest for me locally.

Outside of the backend requirements, I sketched out how the API "get_listing" call would work. I had intended to connect the backend to the frontend, but in the interest of time, I didn't proceed with this and that code is untested. Still, it provided me with the rough data structure I used in my mock frontend data.

I spend more than half my time on the backend, since the database structure seemed the most important aspect of the architecture. Broadly, I had three main ideas:

* Create a core listing table that stores data applicable for any listing.
* Create broad listing types that map to individual tables. In this case, "item" and "lodging".
* Create a "details" column that stores a JSON object in each listing type's table. This allows flexible data for various listing products.

The idea behind the "details" column in both `items` and `lodgings` is to allow structured data on the frontend without making constant database and backend changes to support them. This allows business logic to be handled in the frontend only at the cost of minor performance and data opaqueness. The idea would be that as the business requirements standardize, the structure could then be encoded in the backend/database with minimal changes to the frontend.

One of the challenges for the create functionality was supporting all the possible fields and data. I could have handled this with a multi-step approach - create a plain listing record, then create an item or lodging record. Instead, I built the create logic as a single transaction and separately validate the listing type arguments, which allows the whole transaction to be reversed if there was an error during any part of creation.

The frontend architecture follows from the data structure. I create components and visible sections for the listing, item, source item and lodging data. The idea of the source item would be some sort of established reference for the item being sold. I used Bootstrap to provide some simple styling and threw on a quick carousel to display photos. Uploading photos wasn't included in the create listing logic, but the photo metadata is.

I put a simple checkbox at the top of the listing page to alternate between the two listings.

### Setup Flask
I designed the Flask backend to run the test suite and that is all. You may not want to bother with the setup listed below for Flask and Postgres, but I can confirm the tests pass.

Navigate to the `backend` directory.

Create a virtual environment:
```
$ python3 -m venv env
```

From the `backend` directory and run `pwd`. Take that output and include it at the end of `env/bin/activate` like:
```
export PYTHONPATH="<PWD OUTPUT>"
```

Activate the virtual environment:
```
$ source env/bin/activate
```

Install dependencies:
```
$ pip3 install -r requirements.txt
```

### Setup Postgres
Run:
```
createdb lomatest
```

Edit `backend/marketplace/config.py` and provide a Postgres username/password that has write access to `lomatest`.

From the `backend` directory, create the tables by running:
```
python marketplace/build_database.py
```

### Examine backend
Confirm the tests from the `backend` directory by running:
```
pytest
```

I created minimal tests for the backend as I was going over on time, but ideally I would include testing of the various validation logic and handle edge cases.

### Setup React
Navigate to the `/frontend` directory then run:
```
npm install
```

### Examine frontend
Start React in development mode with:
```
cd frontend
npm run start
```

In your browser, visit <a href="http://localhost:3000/">http://localhost:3000/</a>.
