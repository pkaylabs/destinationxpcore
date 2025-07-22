from pyfcm import FCMNotification
from .models import FCMDevice

# push_service = FCMNotification(api_key="YOUR_SERVER_KEY")
push_service = FCMNotification(
    service_account_file="notifications/dxpmobile.json",
    project_id="dxpmobile"
)

def send_push_notification(user, title, message):
    devices = FCMDevice.objects.filter(user=user)
    registration_ids = [device.token for device in devices]

    if not registration_ids:
        return "No devices"

    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        message_title=title,
        message_body=message,
    )

    return result
