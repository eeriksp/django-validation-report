# Contributing Guidelines

## Testing
For testing purposes a Django project with one extra test app have been added, both of them live under `test_project/`. All the tests are located in `test_project/test_app/tests.py`, although they are actually about the `validation_report` app, not about the `test_app`.

### Configuration
First of all we have to configure some settings. They should live in `test_project/test_project/secrets.py`, from there they will be automatically imported to `settings.py`. A template file has been created for you.

1. Create the file from template. Being in the root directory, type

```
cp test_project/test_project/excample_secrets.py test_project/test_project/secrets.py
```

2. Open the newly created file and fill it in.

### Running the tests
Being in the root directory, type

```
./test_project/manage.py test test_app
```