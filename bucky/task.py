from nio import exceptions


async def send(client, room_id, message):
    try:
        await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message
            }
        )
    except exceptions.OlmUnverifiedDeviceError as err:
        # verify untrusted device
        client.verify_device(err.device)
        await send(client, room_id, message)
