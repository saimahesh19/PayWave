import qrcode

def generate_qr_code(url, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_img.save(filename)

if __name__ == "__main__":
    website_url = input("Enter the URL of the website: ")
    output_filename = input("Enter the output filename (with .png extension): ")
    
    generate_qr_code(website_url, output_filename)
    print(f"QR code generated and saved as '{output_filename}'")
