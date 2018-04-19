from utils import general

import cv2

from utils.log import LogFactory


class GridDetector:
    def __init__(self, model, grid_size, logger=LogFactory.get_default_logger()):
        self.model = model
        self.grid_size = grid_size
        self.logger = logger

    def detect(self, image):
        """
        Gets the skin regions from an image by iterating with a window over the original image

        The resulting image has rough edges but the computation time is faster than the alternatives
        """
        new_image = general.generate_overlay_image(image)

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        rows = gray.shape[0]
        cols = gray.shape[1]

        grid_size = self.grid_size

        # cut image in little pieces
        for r in range(0, rows - grid_size, grid_size):
            for c in range(0, cols - grid_size, grid_size):
                self.logger.print_progress_pixel(r, c, rows, cols)
                roi = gray[r:r + grid_size, c:c + grid_size]

                prediction = self.model.classify(roi)
                if prediction == self.model.skin_label:
                    cv2.rectangle(new_image, (c, r), (c + grid_size, r + grid_size), (0, 0, 0), -1)
        return new_image
