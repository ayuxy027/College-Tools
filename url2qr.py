
import qrcode
import uuid

def url_to_qr(url: str):
    # File name format: aiccimages_<unique_id>.png
    filename = f"aiccimages_{uuid.uuid4().hex}.png"

    # Generate QR code for the given URL
    qr = qrcode.make(url)

    # Save the QR code image
    qr.save(filename)

    print(f"QR code for '{url}' saved as {filename}")

# Example usage
url_to_qr("https://drive.google.com/drive/folders/1jeSLfdM_Bb8Ld8e9JCovUo2ZrdSP7szc?usp=sharing")
