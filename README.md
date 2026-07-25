# HoYoWiki-Exchange

A platform to organize exchange events for HoYoWiki collaborators.

![hoyowiki_exchange_thumbnail](https://github.com/user-attachments/assets/92e899e1-b1d5-4fe5-a752-aa3f9a007190)

<details>

<summary>UI Preview & Functionalities</summary>

![hoyowiki_exchange_streamlit](https://github.com/user-attachments/assets/35f52714-1b9d-4497-869b-256e29769bb2)

### Currently available pages

* **Login/logout:** Authenticates the user with the help of the Discord API.
* **Inventory:** Displays available items with an option to add to cart.
* **Order:** Allows for balance checking as well as order registration and update.

</details>

## Local Installation (Windows, macOS, Linux)

Follow the steps below if you want to run HoYoWiki-Exchange locally on your own machine. Note that you will need both a [Discord](https://discord.com/) and [Neon](https://neon.com/) account for the authentication and external database features to work out of the box.

### Step 1: Install Python

To run HoYoWiki-Exchange locally, you will need [Python](https://www.python.org/downloads/) installed on your computer. You can check for an existing installation by running the following command in a terminal:
```sh
python --version
```

> [!NOTE]
> HoYoWiki-Exchange has been developed and tested on `v3.13.7` of Python.

### Step 2: Download the latest version of the app's code

Here, you can choose between two methods:

1. If you have [Git](https://www.git-scm.com/) installed on your computer, you can clone this repository by running `git clone https://github.com/Antasma245/HoYoWiki-Exchange.git` in the folder where you want the code to be stored.

2. On the main page of the repository, go to `Code` and press `Download ZIP` (or click [here](https://github.com/Antasma245/HoYoWiki-Exchange/archive/refs/heads/main.zip)). Then, extract the downloaded ZIP archive where you want the code to be stored.

### Step 3: Create a secrets file

In the `.streamlit` folder of the installed application, create a file named `secrets.toml` with the following content:
```toml
[connections.neon]
url = ""

[discord]
client_id = ""
client_secret = ""
redirect_uri = ""
wiki_guild_id = ""

[other]
exchange_open = true
```

Please refer to the sections below for information about each value.

<details>

<summary>connections.neon</summary>

In this step, you will use Neon to set up an external database connection to store user, order and item data.

First, open the [Neon Console](https://console.neon.tech/), create a (free) organization if not already done and create a new project within that organization (you do not need to enable Neon Auth).

Because the free tier of Neon comes with strict usage limits and the app does not need much computing power, changing the following is recommended to save resources:
1. Under **Dashboard**, locate the **Primary compute** of the default branch and limit the autoscaling to `0.25 CU`.
2. Under **Settings**, locate the **Compute defaults** section and cap the default compute settings to `0.25 CU`.

Then, go to the **SQL Editor** of the project and run the following query:
```sql
CREATE TABLE users (
    hoyolab_id TEXT PRIMARY KEY,
    balance INTEGER NOT NULL
);

CREATE TABLE items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    category TEXT,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    discord_id TEXT NOT NULL UNIQUE,
    hoyolab_id TEXT NOT NULL REFERENCES users(hoyolab_id) ON DELETE CASCADE,
    comment TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    item_id TEXT REFERENCES items(id),
    PRIMARY KEY (order_id, item_id)
);
```

This will create all the necessary tables and relations. You can then add users with their balance in the `users` table as well as item details in the `items` table (with `image_url` a public Google Drive link). You can do so manually under **Tables** or in bulk with SQL queries.

The final step is to create a separate database user role for improved security. Head to **Overview**, **Roles & Databases** and create a new role with the name `app_user`. Once the role has been created, go back to **SQL Editor** and run the following query:
```sql
REVOKE ALL ON SCHEMA public FROM app_user;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM app_user;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM app_user;

GRANT SELECT ON users TO app_user;
GRANT SELECT ON items TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO app_user;
GRANT SELECT, INSERT, DELETE ON order_items TO app_user;
GRANT USAGE ON SEQUENCE orders_id_seq TO app_user;
```

Finally, at the very top of the sidebar, click on `Connect`. In the newly opened menu, change the role to the `app_user` one we just created. You can also enable **Connection pooling**. Then, click on `Copy snippet` and paste the Postgres connection string in the `secrets.toml` file.

</details>

<details>

<summary>discord</summary>

In this step, you will use Discord to set up user authentication for the app.

First, head over to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application. Give it an explicit name so users know it is linked to the exchange website.

Then, under **OAuth2**, copy the Client ID and Client Secret (you might have to click on `Reset Secret`) and paste both values in their respective fields in the `secrets.toml` file.

Still under **OAuth2**, add your redirect URI under **Redirects**. This should point to the app's login page wherever you are hosting it. For example, if the app is hosted on the Streamlit Community Cloud, your redirect URI will be `https://your-app-name.streamlit.app/login`. During development, you will also likely be using your Streamlit local URI (`http://localhost:XXXX/login`). Whatever you choose, you can then paste the URI in the `secrets.toml` file.

Finally, in Discord, right click on the collaborator server and go down to `Copy Server ID`. Paste the guild ID in the `secrets.toml` file. If you do not see the button, make sure Developer Mode is enabled in your **User Settings**.

Note that since the Discord authentication system does not require a bot user, it is recommended to set **Install Link** as **None** (under **Installation**) and to disable the **Public Bot** toggle under **Bot**.

</details>

<details>

<summary>other</summary>

The `exchange_open` key allows you to control whether users can register and edit their orders using the `Register Order` button. It has to be either `true` or `false`.

</details>

### Step 4: Set up a virtual environment

*This step is optional but highly recommended.*

In the folder where you extracted the app's code, open a terminal and run the following commands:

#### Step 4a: Initialize virtual environment
```sh
python -m venv venv
```

#### Step 4b: Activate virtual environment
For Windows users:
```sh
venv\Scripts\activate
```

> [!TIP]
> If you get an error saying the execution of scripts is disabled on your system, run the following command and try again.
> ```sh
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

For macOS/Linux users:
```sh
source venv/bin/activate
```

### Step 5: Install requirements

In the same terminal, run:
```sh
python -m pip install -r requirements.txt
```

### Step 6: Run the app

Finally, launch the app by running:
```sh
python -m streamlit run app.py
```

<details>

<summary>Updating your Installation</summary>

1. If you installed HoYoWiki-Exchange using Git, open a terminal in the folder where you extracted the app's code and run `git pull`. Then, follow the installation steps starting from **Step 4b**.

2. If you installed HoYoWiki-Exchange manually, follow the installation steps from the beginning to get a new version of the app you will put in a new folder (don't forget to delete the other folder containing the old installation afterwards).

</details>

## Developer notes

This application is meant to be used by HoYoWiki collaborators, but is by no means officially affiliated or endorsed by HoYoverse.

This program uses the Streamlit library, which is open sourced under the Apache 2.0 license. A copy of the aforementioned license document can be found in the [`appendix`](appendix) folder of the application or on Streamlit's [GitHub page](https://github.com/streamlit/streamlit?tab=Apache-2.0-1-ov-file).
