# Ebédke

> There are two hard things in computer science, cache invalidation and deciding
> where to eat.

Ebédke is a Flask web crawler that collects the daily menu from
restaurants' webpages. The collected menus are cached in redis and can be viewed in
an HTML page or in JSON format.

## Development

[Pipenv](https://docs.pipenv.org) is the recommended tool to manage
dependencies. A locally installed and running redis server is required at the
moment.

First install the dependencies:

```
pipenv sync
```

Copy `config.py.example` as `config.py` and set the values. A [Facebook app
token](https://developers.facebook.com/docs/facebook-login/access-tokens#apptokens)
is required to read posts from Facebook pages.


Running `app.py` directly will run the Flask dev server. This is enough for testing
purposes but not ideal for production.

```
pipenv run python app.py
```

To test individual providers add their module name as an argument to `app.py`.
Adding an optional integer argument will offset the date, for example:

```
pipenv run python app.py provider -3
```

Note that running the scripts individually will skip the redis cache.


## Deployment

Using a production webserver with a wsgi server like gunicorn or uwsgi is
recommended. An example nginx config is included in the resources directory. It
can be used with this example uwsgi command.

```
uwsgi --plugin python3 --virtualenv /virtualenv/path/ -s /run/ebedke.sock --manage-script-name --mount /=app:app --threads=4 --chmod-socket=664 -T
```


## License


The source code in the repository is licensed under either of
  - Apache License, Version 2.0, (LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
  - MIT license (LICENSE-MIT or http://opensource.org/licenses/MIT)

at your option.

The page background pattern is freely available at [Heropatterns](http://www.heropatterns.com/),
licensed under [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/).
