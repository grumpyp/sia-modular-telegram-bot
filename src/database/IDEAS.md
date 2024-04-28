User can sign up and then subscribe to events for example alert1,..


# Create Events table
```
c.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    event_description TEXT,
    event_date TEXT
)
''')
```
# Create Subscriptions table
```
c.execute('''
CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER,
    event_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    PRIMARY KEY (user_id, event_id)
)
''')
```