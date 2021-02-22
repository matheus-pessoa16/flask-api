# Project Hub - API

Project Hub is a system that makes it possible to create a project with a title and description that can be liked by users, growing up the engagement and support of the community. The idea came from this [gist](https://gist.github.com/exageraldo/79c9ed99bf3a02bfbde9c517caa2b478).

The entity-relationship diagram can be found [here](https://drive.google.com/file/d/1C4B3-WQz-oibIGj5i3DJdo3lGfHlnHZZ/view?usp=sharing).

If you want to try this project online, click [here](https://matheus-pessoa16.github.io/project-front/login). The backend is hosted at Heroku and the frontend on Github Pages.

To use this project on your own machine, you will need the frontend from this [repository](https://github.com/matheus-pessoa16/project-front). To execute the backend follow the steps described below to execute at localhost.

The database used is SQLite, just for demonstration. 

Install the dependencies

```pip install -r requirements.txt```

After the installation, you can run the application with the command

```python app.py```

To create an admin you'll need to create a common user first and just remove the comment from app.py

```# createAdmin()```

The application will restart and you can try to log in as admin.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)