from typing import Any, Callable, Literal

FormError = dict[str, str]

ValidatorType = Callable[[Any], None]
ConverterType = Callable[[Any], Any]
ContextType = dict[str, Any]
EnvType = Literal['prod', 'dev']
FormatType = Literal['docx', 'odt']
