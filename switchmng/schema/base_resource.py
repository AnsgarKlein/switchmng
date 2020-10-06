from typing import Any
from typing import Dict

from switchmng.typing import JsonDict

class BaseResource():
    """
    Represents the base for all REST resources.

    This class only provides the skeleton for other resources
    and cannot be instantiated.
    Every implementing class should overwrite
    `_Attributes` and `ResourceIdentifier`.
    """

    ResourceIdentifier = 'name'
    """*Name* of the attribute that is this resource's identifier"""

    _Attributes: Dict[str, Dict[str, Any]] = {}

    def __init__(self, **kwargs):
        cls = type(self)

        # Check if all required arguments are available
        for key in cls._Attributes:
            # Set optional arguments to default value
            if cls._Attributes[key]['optional']:
                setattr(self, key, cls._Attributes[key]['null'])
                continue

            # Check if all required arguments are given
            if key not in kwargs:
                raise TypeError("Missing attribute '{}' for resource {}".format(
                    key,
                    cls))

        # Check if all given arguments are valid
        self.check_params(**kwargs)
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __setattr__(self, name, val) -> None:
        # If attribute is not a resource attribute set it normally
        if name not in type(self)._Attributes:
            super().__setattr__(name, val)
            return

        # Check resource attribute before setting
        self.check_param(name, val)

        attr = type(self)._Attributes[name]
        super().__setattr__(attr['private'], val)

        # Run post hooks after setting resource attribute
        if 'post_hooks' in attr:
            for hook in attr['post_hooks']:
                hook(self)

    def __getattribute__(self, name):
        # If attribute is not a resource attribute get it normally
        attrs = type(self)._Attributes
        if name not in attrs:
            return super().__getattribute__(name)
        return getattr(self, attrs[name]['private'])

    def __str__(self) -> str:
        # Represent this resource as a string of resource identifier
        return str(getattr(self, type(self).ResourceIdentifier))

    def __repr__(self) -> str:
        return self.__str__()

    def jsonify(self) -> JsonDict:
        """
        Represent this resource as a json-ready dict.

        That is a dict which completely consists of json-compatible structures
        like:

        * dict
        * list
        * string
        * int
        * bool
        * None / null
        """

        Attributes = type(self)._Attributes

        # Create json dictionary
        json_dict: JsonDict = {}
        # Add every resource attribute to dictionary
        for key in Attributes:

            # If necessary jsonify attribute before adding it
            var = getattr(self, key)
            if 'jsonify' in Attributes[key]:
                var = Attributes[key]['jsonify'](var)

            json_dict[key] = var

        return json_dict

    @classmethod
    def check_param(cls, key, val) -> None:
        """
        Check given parameter.

        Check if given parameter has the correct type and is a valid
        attribute for this resource.

        These checks get executed when trying to assign a value to a
        resource attribute but can be called when needing to check parameters
        before making changes.

        :raises TypeError: When type of given parameter does not match
            expectation
        :raises ValueError: When value of given parameter does not match
            expectation
        """

        # Check if attribute is valid for this resource at all
        if key not in cls._Attributes:
            raise TypeError("Unexpected attribute '{}' for resource '{}'".format(
                key,
                cls))

        Attribute = cls._Attributes[key]

        # Check if attribute is null and is allowed to be null
        if Attribute['optional'] and val is None:
            return

        # Check if attribute has correct type
        if Attribute['list']:
            msg = "Attribute '{}' of resource {} has to be of type list of '{}'".format(
                key,
                cls,
                Attribute['type'])
            if not isinstance(val, list):
                raise TypeError(msg)
            for item in val:
                if not isinstance(item, Attribute['type']):
                    raise TypeError(msg)
        else:
            msg = "Attribute '{}' of resource {} has to be of type '{}'".format(
                key,
                cls,
                Attribute['type'])
            if not isinstance(val, Attribute['type']):
                raise TypeError(msg)

        # Check all checks
        if 'checks' in Attribute:
            msg = "Illegal value '{}' for attribute '{}' of resource {}".format(
                val,
                key,
                cls)
            for value_check in Attribute['checks']:
                if value_check(cls, val) is False:
                    raise ValueError(msg)

    @classmethod
    def check_params(cls, **kwargs) -> None:
        """
        Check all given parameter.

        Check if given parameters have the correct type and are valid
        attributes for this resource.

        These checks get executed when trying to assign a value to a
        resource attribute but can be called when needing to check multiple
        parameters at once in order to prevent inconistent states.

        :raises TypeError: When type of given parameter does not match
            expectation
        :raises ValueError: When value of given parameter does not match
            expectation
        """

        for key, val in kwargs.items():
            cls.check_param(key, val)
