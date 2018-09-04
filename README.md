# VMware branding bot

## Scope

This is a simple branding bot for VMware. This periodically checks a few subreddits then comments when someone spells VMware as `VMWare`.

## Running via Python

1. First create an app as a "script" here: https://www.reddit.com/prefs/apps

1. Run the command with these ENV variables:

    ```
    PASSWORD='VMware123!' \
    CLIENT_ID='my_client_id1' \
    CLIENT_SECRET='atotallysecretclientthingy2' \
    SUBREDDITS='a_subreddit anotehr_subreddit' \
    REDDIT_USERNAME='your_reddit_username' \
    BOT_REPLY_MESSAGE='The message you'd like to use as the reply' \
    python3 vmware_reddit_bot.py
    ```

## Running via Habitat

1. First create an app as a "script" here: https://www.reddit.com/prefs/apps
1. Setup Habitat (see: [https://www.habitat.sh/docs/install-habitat/](https://www.habitat.sh/docs/install-habitat/))
1. Run `hab pkg build .`
1. Create `/hab/user/vmware_reddit_bot/config/user.toml` based on `habitat/default.toml`
1. Run `hab run results/yourorigin-vmware_reddit_bot*`

> For running as a service see: [https://www.habitat.sh/docs/best-practices/#running-habitat-servers](https://www.habitat.sh/docs/best-practices/#running-habitat-servers)

## Testing via Habitat

### Unit Tests

1. Setup Habitat (see: [https://www.habitat.sh/docs/install-habitat/](https://www.habitat.sh/docs/install-habitat/))
1. Run `hab studio enter`
1. Run `python -m unittest tests/vmware_reddit_bot_tests.py`

### Lint Tests

1. Setup Habitat (see: [https://www.habitat.sh/docs/install-habitat/](https://www.habitat.sh/docs/install-habitat/))
1. Run `hab studio enter`
1. Run `python -m pylint path_to_file.py`

## License and Author
Author:: JJ Asghar <jjasghar@gmail.com>
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
