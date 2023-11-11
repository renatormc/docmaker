from .celular.form import CelularForm
from .test.form import TestForm
from doctpl.gui.form import BaseForm

forms: list[BaseForm] = [
    CelularForm,
    TestForm
]