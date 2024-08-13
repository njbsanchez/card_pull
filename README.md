<a name="install"></a>
## Installation

To get started, clone Connectify by pasting below into your terminal.

```bash
git clone https://github.com/njbsanchez/Connectify.git
```


Separately, create developer accounts for both Spotify and Google Maps Javascript API. Once obtained, create a secrets.sh file and input the following:

```bash
export SPOTIPY_CLIENT_ID=<client_id_here>
export SPOTIPY_CLIENT_SECRET=<client_secret_here>
export GOOGLE_CLIENT_KEY=<google_key_here>      #due to nature of Google's API, there is no need for a client secret key.
```
Once you have Connectify opened in your preferred code editor, create and activate your virtual environment.

```bash

virtualenv env
source env/bin/activate


```
Install dependencies by installing requirements.txt file.

```bash

pip3 install -r requirements.txt

```

Source your API keys by applying secrets.sh to your virtual environment.

```bash

source secrets.sh

```

To start the application, run the following commands in your terminal.

```python
# if you would like to utilize test information to play with, run the following:

python3 -i seed_database.py

# starts up the server
python3 -i server.py
```
<a name="connect2"></a>
## Connectify 2.0

Some additional features and design factors I would like to add in the near future:
- add additional data points for comparison analysis feature (utilize track/artist metadata to build fuller music taste snapshot)
- add in messaging/commenting feature
- further develop out Connect page map (unify UI between map and list feature)
- improve geolocation feature

<a name="contribute"></a>
## Contributing

Pull requests are welcome. As I continue to build out features and improve UX/UI design of the app, feel free to comment or reach out with any suggestions, refactoring advice, or feature requests I can try and add to the application.

<a name="aboutme"></a>
## About Me

"After completing her B.S. in Accounting at the University of San Francisco, Nicole began her career as an auditor at Deloitte. Hungry for the opportunity to build, she joined Pinterest as a Deals Program Manager on the Operational Excellence team, strengthening work flows for international sales teams and  establishing key foundations for the Annual Deals Program. Nicole found herself drawn to the excitement that came with each new product launch, especially the new tools that supported small businesses on the platform. In participating in bug bashes and volunteering for feature testing, she realized that she, too, could build these awesome tools, leading her to a new path in software engineering."

<a name="connectme"></a>
## Lets Connect!

You can reach me here on [Github](https://github.com/njbsanchez/Connectify) or connect with me on [LinkedIn](https://www.linkedin.com/in/njbsanchez/) at njbsanchez.
