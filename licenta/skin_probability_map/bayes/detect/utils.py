from utils.utils import Pixel


def calculate_pixel_probability(pixel, bayes_spm_components):
    """
    Calculates the probability that the given pixel is a skin pixel

    uses the formula p = P(X|S) * P(S) / P(X)
    where S represents the prob of a pixel being a skin pixel ; X the probability of getting the selected pixel
    and P(X|S) the prob of finding this pixel given skin
    """
    p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])

    if p not in bayes_spm_components.appearances_as_skin:
        return 0

    px = bayes_spm_components.appearances[p] / (
        bayes_spm_components.skin_pixels + bayes_spm_components.non_skin_pixels)
    ps = bayes_spm_components.skin_pixels / (
        bayes_spm_components.skin_pixels + bayes_spm_components.non_skin_pixels)
    pxs = bayes_spm_components.appearances_as_skin[p] / bayes_spm_components.skin_pixels
    return (pxs * ps) / px
