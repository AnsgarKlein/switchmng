from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

# Sadly mypy does not support recursive types (See mypy github issue #731)
# Otherwise this would be the correct way:
#
# JsonPrimitive = Union[str, int, None]
# JsonDict = Dict[str, Union[JsonPrimitive, JsonDict, Dict[str, JsonDict], List[JsonDict]]]

# This is a terrible hack:
_JsonPrimitive = Union[str, int, None]
_JsonItem2 = Union[_JsonPrimitive,             Dict[str, Any],        List[Any]]
_JsonItem1 = Union[_JsonPrimitive, _JsonItem2, Dict[str, _JsonItem2], List[_JsonItem2]]
JsonDict   = Dict[str, _JsonItem1]


FlaskResponse = Tuple[JsonDict, int]
