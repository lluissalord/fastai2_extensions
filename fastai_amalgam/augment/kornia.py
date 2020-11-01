# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/07_augment_kornia.ipynb (unless otherwise specified).

__all__ = ['KorniaBase', 'MotionBlur', 'ColorJitter', 'RandomRotation', 'MedianBlur', 'HFlip', 'VFlip',
           'RandomGrayscale', 'RandomPerspective', 'RandomPerspective']

# Cell
from fastai.vision.all import *
import PIL
import kornia as K
import torchvision.transforms.functional as TTF
from PIL import Image

# Cell
class KorniaBase(RandTransform):
    '''
    Pass in a kornia function, module, list of modules, or nn.Sequential
    containers to `kornia_tfm`.
    If passing functions, you can pass in function arguments as keyword
    args (**kwargs), which can also be random number generators.

    Example
    =======
    * KorniaWrapper(kornia.adjust_hue, hue_factor=1.2)
    * KorniaWrapper(kornia.augmentation.ColorJitter(.2,.3,.1,.2))
    * KorniaWrapper(nn.Sequential(*[kornia.augmentation.ColorJitter()]))
    * KorniaWrapper([
        kornia.augmentation.ColorJitter(.2),
        kornia.augmentation.RandomMotionBlur(3, 5., 1.)
    ]))
    '''
    order = 10
    split_idx = 0
    def __init__(self, kornia_tfm=None,p=1., **kwargs):
        super().__init__(p=p)
        self.tfm = kornia_tfm
        self.input_kwargs = kwargs
        self.call_kwargs  = dict.fromkeys(kwargs)
        self._pipe = Pipeline([ToTensor(), IntToFloatTensor()])
        self.process_tfm()

    def before_call(self, b, split_idx, verbose=False):
        'Compute `p` of applying transform, process input kwargs if applicable'
        self.do = self.p==1. or random.random() < self.p
        for arg,value in self.input_kwargs.items():
            if hasattr(value, '__call__'): self.call_kwargs[arg] = value()
            else: self.call_kwargs[arg] = value

    def process_tfm(self):
        'Process the input `kornia_tfm` argument and make it callable'
        if hasattr(self.tfm, 'forward') and hasattr(self.tfm, '__iter__'):
            pass                                ## -- nn.Sequential

        elif hasattr(self.tfm, 'forward') and type(self.tfm) is not type:
            self.tfm = nn.Sequential(self.tfm)  ## -- Kornia module (called)

        elif hasattr(self.tfm, 'forward') and type(self.tfm) is type:
            #self.tfm = nn.Sequential(self.tfm)  ## -- Kornia module (uncalled)
            pass

        elif isinstance(self.tfm, list):
            self.tfm = nn.Sequential(*self.tfm) ## -- list of Kornia Modules

    def _encode(self, o:TensorImage): return TensorImage(self.tfm(o, **self.call_kwargs)) if self.do else o
    def encodes(self, o:torch.Tensor): return self._encode(o)
    def encodes(self, o:Image.Image):  return self._encode(self._pipe(PILImage(o)))
    def encodes(self, o:TensorImage):  return self._encode(o)
    def encodes(self, o:PILImage):     return self._encode(self._pipe(o))
    def encodes(self, o:(str,Path)):   return self._encode(self._pipe(PILImage.create(o)))
    def encodes(self, o:(TensorCategory,TensorMultiCategory)): return o

    def __repr__(self): return self.tfm.__repr__()

# Cell
class MotionBlur(KorniaBase):
    'kornia.augmentation.RandomMotionBlur'
    order=110
    def __init__(self, p=.2, kernel_size=(3,21), angle=(15., 15.), direction=(-1., 1.)):
        super().__init__(
            kornia_tfm = K.augmentation.RandomMotionBlur(kernel_size = kernel_size,
                                                         angle       = angle,
                                                         direction   = direction),
            p=p)

# Cell
class ColorJitter(KorniaBase):
    'kornia.augmentation.ColorJitter'
    order=20
    def __init__(self, p=.2, jitter_brightness=.1, jitter_contrast=.1, jitter_saturation=(.1, .9), jitter_hue=.2):
        super().__init__(
            kornia_tfm = K.augmentation.ColorJitter(brightness = jitter_brightness,
                                                    contrast   = jitter_contrast,
                                                    saturation = jitter_saturation,
                                                    hue        = jitter_hue),
            p=p
        )

# Cell
class RandomRotation(KorniaBase):
    'kornia.augmentation.RandomRotation'
    order=13
    def __init__(self, p=.2, rotate_degrees=10):
        super().__init__(
            kornia_tfm = K.augmentation.RandomRotation(rotate_degrees),
            p=p
        )

# Cell
class MedianBlur(KorniaBase):
    'kornia.filters.MedianBlur'
    order=14
    def __init__(self, p=.2, kernel_size=(5,5), p_median_blur=.2):
        super().__init__(
            kornia_tfm = K.filters.MedianBlur(kernel_size=kernel_size),
            p=p
        )

# Cell
class HFlip(KorniaBase):
    'kornia.augmentation.RandomHorizontalFlip'
    order=15
    def __init__(self, p=.5):
        super().__init__(
            kornia_tfm = K.augmentation.RandomHorizontalFlip(p=p)
        )

# Cell
class VFlip(KorniaBase):
    'kornia.augmentation.RandomVerticalFlip'
    order=16
    def __init__(self, p=.5):
        super().__init__(
            kornia_tfm = K.augmentation.RandomVerticalFlip(p=p)
        )

# Cell
class RandomGrayscale(KorniaBase):
    'kornia.augmentation.RandomGrayscale'
    order=17
    def __init__(self, p=.2):
        super().__init__(
            kornia_tfm=K.augmentation.RandomGrayscale(p=p)
        )

# Cell
class RandomPerspective(KorniaBase):
    'kornia.augmentation.RandomPerspective'
    order=18
    def __init__(self, p=.2, distortion_scale=0.5, interpolation='BILINEAR'):
        super().__init__(
            kornia_tfm=K.augmentation.RandomPerspective(
                p=p, distortion_scale=distortion_scale,
                interpolation=interpolation)
        )

# Cell
class RandomPerspective(KorniaBase):
    'kornia.augmentation.RandomPerspective'
    order=18
    def __init__(self, p=.2, distortion_scale=0.5, interpolation='BILINEAR'):
        super().__init__(
            kornia_tfm=K.augmentation.RandomPerspective(
                p=p, distortion_scale=distortion_scale,
                interpolation=interpolation)
        )