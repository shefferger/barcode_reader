from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

#vs = VideoStream(usePiCamera=True).start()
vs = VideoStream().start()
time.sleep(2.0)
csv = open("bc.csv", "w")
found = set()
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    height, width = frame.shape[:2]
    barcodes = pyzbar.decode((frame[:, :, 0].astype('uint8').tobytes(), width, height))

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.datetime.now(),
                                       barcodeData))
            csv.flush()
            found.add(barcodeData)

    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

csv.close()
cv2.destroyAllWindows()
vs.stop()