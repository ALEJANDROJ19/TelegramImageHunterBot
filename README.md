# Telegram Image Hunter Bot

> A simple playground bot that generates and stores a `sha256` hash of the image sent by the user, and if the same hash is found, it notifies the user.

Project under development.

##TODO:

- Hashes for each chat/user
- SQlite instead textfile
- Avoid tmp file storage if possible (reduce disk usage - useful for AWS)
- Delete duplicated images (if admin permission granted)