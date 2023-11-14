from typing import Any, Callable

FormError = dict[str, str]

ValidatorType = Callable[[Any], None]
ConverterType = Callable[[Any], Any]
ContextType = dict[str, Any]
