class BayesSpmComponents:
    """
    Class that encapsulates components of a Bayes Skin Probability Map
    """

    def __init__(self, skin_pixels, non_skin_pixels, appearances, appearances_as_skin):
        """
        Components of a Bayes spm

        :param skin_pixels: number of skin pixels in training set
        :param non_skin_pixels: number of nonskin pixels in training set
        :param appearances: map<Pixel, int> ; number of appearances of each pixel
        :param appearances_as_skin: map<Pixel, int> ; number of appearances of each pixel as a skin pixel
        """
        self.skin_pixels = skin_pixels
        self.non_skin_pixels = non_skin_pixels
        self.appearances = appearances
        self.appearances_as_skin = appearances_as_skin
