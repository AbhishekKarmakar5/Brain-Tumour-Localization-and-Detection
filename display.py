import cv2
import numpy as np

class colorSel:
    def __init__(self, image, hLow=0, sLow=0, vLow=0, hHigh=0, sHigh=0, vHigh=0):
        self.image = image
        self._hLow = hLow
        self._sLow = sLow
        self._vLow = vLow
        self._hHigh = hHigh
        self._sHigh = sHigh
        self._vHigh = vHigh

        def onchangeHLow(pos):
            self._hLow = pos
            self._render()

        def onchangeSLow(pos):
            self._sLow = pos
            self._render()

        def onchangeVLow(pos):
            self._vLow = pos
            self._render()

        def onchangeHHigh(pos):
            self._hHigh = pos
            self._render()

        def onchangeSHigh(pos):
            self._sHigh = pos
            self._render()

        def onchangeVHigh(pos):
            self._vHigh = pos
            self._render()

        cv2.namedWindow('cSel')
        cv2.createTrackbar('H low', 'cSel', self._hLow, 255, onchangeHLow)
        cv2.createTrackbar('S low', 'cSel', self._sLow, 255, onchangeSLow)
        cv2.createTrackbar('V low', 'cSel', self._vLow, 255, onchangeVLow)
        cv2.createTrackbar('H high', 'cSel', self._hHigh, 255, onchangeHHigh)
        cv2.createTrackbar('S hgh', 'cSel', self._sHigh, 255, onchangeSHigh)
        cv2.createTrackbar('V high', 'cSel', self._vHigh, 255, onchangeVHigh)
        
        self._render()

        print("Adjust the parameters as desired.  Hit any key to close.")
        cv2.waitKey(0)
        cv2.destroyWindow('cSel')

    def hLow(self):
        return self._hLow

    def sLow(self):
        return self._sLow

    def vLow(self):
        return self._vLow

    def hHigh(self):
        return self._hHigh

    def sHigh(self):
        return self._sHigh

    def vHigh(self):
        return self._vHigh

    def cSelImage(self):
        return self._hsv_img

    def _render(self):
        low = np.array([ self._hLow, self._sLow, self._vLow])
        high = np.array([ self._hHigh, self._sHigh, self._vHigh])
        mask = cv2.inRange(self.image, low, high)
        self._hsv_img = cv2.bitwise_and(self.image, self.image, mask=mask)
        cv2.imshow('cSel', cv2.cvtColor(self._hsv_img, cv2.COLOR_HSV2BGR))
