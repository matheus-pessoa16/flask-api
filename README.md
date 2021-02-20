# Project Hub - API

Project Hub is a system that makes it possible to create a project with a title and description that can be liked by users, growing up the engagement and support of the community. The idea behind the code came from this [gist](https://gist.github.com/exageraldo/79c9ed99bf3a02bfbde9c517caa2b478).


To use this project on your own machine, you will need the frontend from this [repository](https://github.com/matheus-pessoa16/project-front). To execute the backend, follow the steps described bellow.

To execute on localhost, follow these steps. The database used is the SQLite, just for demonstration.

Install the dependencies

```pip install -r requirements.txt```

After the installation you can run the aplication with the command

```python app.py```

To create an admin you'll need to create a common user first and just remove the comment from app.py

```# createAdmin()```

The application will restart and you can try to log in as an admin.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)