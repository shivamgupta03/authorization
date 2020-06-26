# authorization

- Create a virtual environment `virtualenv venv`
- Activate the virtual environment `source venv/bin/activate`
- Install django `pip install django`
- Install requests library `pip install requests`
- Create migration files `python manage.py makemigrations`
- Run migrations `python manage.py migrate`
- Run the server `python manage.py runserver 8080`
- View the oauth2 flow `http://localhost:8080/google/google_install`
- You may get a warning saying **This app isn't verified**. Please proceed with it.
- On completion of oauth you will be provided with a link to refresh the token and a curl command to verify the data is being pulled from your account. Here is the sample response

```json
{
  "access_token": "access_token",
  "refresh_token_link": "http://localhost:8080/google/refresh_token?id=3",
  "google_user_id": 3,
  "refresh_token": "refresh_token",
  "curl_command_for_contacts": "curl -X GET -H 'Authorization: Bearer access_token' 'https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses'"
}
```
