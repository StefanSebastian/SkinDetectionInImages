class Superpixel:
    def __init__(self, root_pixel_pos, image):
        self.image = image
        self.root_pixel_pos = root_pixel_pos
        self.pixels_pos = []

    def add_pixel(self, pixel_pos):
        self.pixels_pos.append(pixel_pos)

    def get_root_pixel_pos(self):
        return self.root_pixel_pos

    def get_pixels_pos(self):
        return self.pixels_pos

    def get_image(self):
        return self.image

    def __key(self):
        return self.root_pixel_pos

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.root_pixel_pos) + ' ' + str(self.pixels_pos)


