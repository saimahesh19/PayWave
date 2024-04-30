# import cv2
# from pyzbar.pyzbar import decode

# def scan_qr_code():
#     cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device
    
#     while True:
#         _, frame = cap.read()
#         qr_codes = decode(frame)
        
#         if qr_codes:
#             qr_code = qr_codes[0]
#             url = qr_code.data.decode('utf-8')
#             print("Scanned URL:", url)
#             break
        
#         cv2.imshow("QR Code Scanner", frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# # Example usage
# scan_qr_code()


import cv2
from pyzbar.pyzbar import decode

def scan_qr_code():
    cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device
    
    while True:
        _, frame = cap.read()
        qr_codes = decode(frame)
        
        if qr_codes:
            qr_code = qr_codes[0]
            url = qr_code.data.decode('utf-8')
            print("Scanned URL:", url)
            cap.release()
            cv2.destroyAllWindows()
            return url
        
        cv2.imshow("QR Code Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scanned_url = scan_qr_code()
    with open("scanned_url.txt", "w") as f:
        f.write(scanned_url)
