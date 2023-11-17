from typing import TYPE_CHECKING, Type
from .stext import SText
from .scombo_box import SComboBox
from .sdate import SDate
from .sfolder_pics import SFolderPics
from .scheck_box import SCheckBox
from .sspin_box import SSpinBox
from .sarray import SArray
from .svar_form import SVarForm
from .sfloat import SFloat
from .sfile_chooser import SFileChooser
from .sstring_list import SStringList
from .sbutton import SButton
from .sspacer import SSpacer


if TYPE_CHECKING:
    from .widget import Widget

__widgets__: list[Type['Widget']] = [
    SText,
    SComboBox,
    SDate,
    SFolderPics,
    SCheckBox,
    SSpinBox,
    SArray,
    SVarForm,
    SFloat,
    SFileChooser,
    SStringList,
    SButton,
    SSpacer
]
