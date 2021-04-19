from nio import AsyncClient


async def login(config):
    timeout = int(config.timeout)

    # establish connection
    client = AsyncClient(
        'https://' + config.server,
        config.username,
        store_path=config.store_path)

    # avoid creating new session each login
    access_token, device_id = config.get_session()
    if access_token != '':
        client.access_token = access_token
        client.device_id = device_id
        client.user_id = config.username
        await client.login(config.password)
    else:
        # create new session if not exists
        resp = await client.login(config.password)
        config.set_session(resp.access_token, resp.device_id)

    # join room just in case haven't
    await client.join(config.room_id)

    # sync before adding callback to prevent reading old messages
    await client.sync(timeout=timeout)

    # trust room participants
    if client.room_contains_unverified(config.room_id):
        trust_participants(client, config.room_id)

    return client


def trust_participants(client, room_id):
    # trust all
    for user in client.room_devices(room_id):
        for device_id, olm_device in \
                client.room_devices(room_id)[user].items():
            client.unverify_device(olm_device)  # prevent duplicate entries
            client.verify_device(olm_device)
