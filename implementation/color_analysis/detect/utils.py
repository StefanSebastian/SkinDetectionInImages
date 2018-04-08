from utils.tuples import Pixel


def calculate_pixel_probability(pixel, bayes_spm_components):
    return __calculate_simple(pixel, bayes_spm_components)


def __calculate_simple(pixel, bayes_spm_components):
    return __calculate_skin_probability(pixel, bayes_spm_components)


def __calculate_as_ratio(pixel, bayes_spm_components):
    sp = __calculate_skin_probability(pixel, bayes_spm_components)
    nsp = __calculate_non_skin_probability(pixel, bayes_spm_components)
    if nsp == 0:  # most commonly no appearances for the pixel so we treat it by default as nonskin
        return 0
    return sp / nsp


def __calculate_skin_probability(pixel, bayes_spm_components):
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


def __calculate_non_skin_probability(pixel, bayes_spm_components):
    """
    Calculates the probability that the given pixel is a non skin pixel

    uses the formula p = P(X|NS) * P(NS) / P(X)
    where NS represents the prob of a pixel being a non skin pixel ; X the probability of getting the selected pixel
    and P(X|NS) the prob of finding this pixel given nonskin
    """
    p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])

    if p not in bayes_spm_components.appearances:
        return 0

    px = bayes_spm_components.appearances[p] / (
        bayes_spm_components.skin_pixels + bayes_spm_components.non_skin_pixels)
    pns = bayes_spm_components.non_skin_pixels / (
        bayes_spm_components.skin_pixels + bayes_spm_components.non_skin_pixels)

    if p not in bayes_spm_components.appearances_as_skin:
        appearanceas_as_ns = bayes_spm_components.appearances[p]
    else:
        appearanceas_as_ns = bayes_spm_components.appearances[p] - bayes_spm_components.appearances_as_skin[p]

    pxns = appearanceas_as_ns / bayes_spm_components.non_skin_pixels
    return (pxns * pns) / px
