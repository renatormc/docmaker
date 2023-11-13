from typing import Any, Callable

FormError = dict[str, str]

ValidatorType = Callable[[Any], None]
ConverterType = Callable[[Any], Any]
Context = dict[str, Any]