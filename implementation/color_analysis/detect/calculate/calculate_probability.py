from utils.tuples import Pixel


class ProbabilityCalculator:

    @staticmethod
    def calculate_for_pixel(pixel, bayes_spm_components):
        """
        Calculates the probability that the given pixel is a skin pixel
        """
        p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
        if p not in bayes_spm_components.appearances_as_skin or p not in bayes_spm_components.appearances:
            return 0

        return ProbabilityCalculator.__apply_bayes(bayes_spm_components.appearances[p],
                                                   bayes_spm_components.appearances_as_skin[p],
                                                   bayes_spm_components.skin_pixels,
                                                   bayes_spm_components.non_skin_pixels)

    @staticmethod
    def calculate_max_from_area(pixel, bayes_spm_components, area):
        """
        Calculates skin probability as a the maximum probability over an area
        """
        max_prob = 0
        for r_offset in range(-area, area, 1):
            for g_offset in range(-area, area, 1):
                for b_offset in range(-area, area, 1):
                    offset_pixel = [pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset]
                    prob = ProbabilityCalculator.calculate_for_pixel(offset_pixel, bayes_spm_components)
                    if prob > max_prob:
                        max_prob = prob
        return max_prob

    @staticmethod
    def calculate_sum_area(pixel, area, bayes_spm_components):
        """
        Calculates skin probability by treating all pixels in the area as part of the same bin
        """
        total_appearances = 0
        total_appearances_as_skin = 0

        for r_offset in range(-area, area, 1):
            for g_offset in range(-area, area, 1):
                for b_offset in range(-area, area, 1):
                    neighbour = [pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset]
                    p = Pixel(F1=neighbour[0], F2=neighbour[1], F3=neighbour[2])

                    if p not in bayes_spm_components.appearances_as_skin:
                        appearances_as_skin = 0
                    else:
                        appearances_as_skin = bayes_spm_components.appearances_as_skin[p]
                    total_appearances_as_skin += appearances_as_skin

                    if p not in bayes_spm_components.appearances:
                        appearances = 0
                    else:
                        appearances = bayes_spm_components.appearances[p]
                    total_appearances += appearances

        return ProbabilityCalculator.__apply_bayes(total_appearances,
                                                   total_appearances_as_skin,
                                                   bayes_spm_components.skin_pixels,
                                                   bayes_spm_components.non_skin_pixels)

    @staticmethod
    def __apply_bayes(pixel_appearances, pixel_appearances_as_skin, skin_pixels_nr, non_skin_pixels_nr):
        """
        Applies Bayes formula to check if a pixel is a skin pixel

        uses the formula p = P(X|S) * P(S) / P(X)
        where S represents the prob of a pixel being a skin pixel ; X the probability of getting the selected pixel
        and P(X|S) the prob of finding this pixel given skin
        """
        total_pixels_nr = skin_pixels_nr + non_skin_pixels_nr
        px = pixel_appearances / total_pixels_nr
        ps = skin_pixels_nr / total_pixels_nr
        pxs = pixel_appearances_as_skin / skin_pixels_nr
        if px == 0:
            return 0
        return (pxs * ps) / px
