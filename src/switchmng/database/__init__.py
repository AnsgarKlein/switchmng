from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from switchmng.schema import *

class DatabaseConnection():
    def __init__(self, dbtype, dbstr, base):
        # Initialize db engine
        if dbtype == 'sqlite':
            if dbstr == '':
                # Warn when creating an in-memory sqlite database
                print('WARNING: Using an in-memory sqlite database!\n'
                    + '         Changes will not be persistent!')

                dbstr = 'sqlite://'
            else:
                dbstr = 'sqlite:///' + dbstr
        else:
            raise NotImplementedError('Databases other than sqlite are not yet supported')

        self.engine = create_engine(dbstr, echo = False)

        self.base = base
        self.base.metadata.create_all(self.engine)
        self.base.metadata.bin = self.engine

        # Initialize scoped sessions to support multi thread access to database
        self.sessionm = sessionmaker(bind = self.engine)
        self.Session = scoped_session(self.sessionm)

    def query_switch_model(self, resource_id):
        """
        Retrieve :class:`SwitchModel` object from database.

        Query the database for a :class:`SwitchModel` object with given resource
        identifier and return it.

        :param resource_id: Resource identifier uniquely identifying the
            switch model to return.
            (See :class:`SwitchModel` for what attribute is the resource identifier)
        :type resouce_id: str

        :return: The switch model object matching the given resource identifier
        :rtype: SwitchModel
        """

        if not isinstance(resource_id, str):
            raise TypeError('Cannot query switch model with resource id not of type str')

        session = self.Session()
        model = session.query(SwitchModel)
        model = model.filter_by(_name = resource_id)

        if len(model.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return model.first()

    def query_switch(self, resource_id):
        """
        Retrieve :class:`Switch` object from database.

        Query the database for a :class:`Switch` object with given resource
        identifier and return it.

        :param resource_id: Resource identifier uniquely identifying the
            switch to return.
            (See :class:`Switch` for what attribute is the resource identifier)
        :type resouce_id: str

        :return: The switch object matching the given resource identifier
        :rtype: Switch
        """

        if not isinstance(resource_id, str):
            raise TypeError('Cannot query switch with resource id not of type str')

        session = self.Session()
        sw = session.query(Switch)
        sw = sw.filter_by(_name = resource_id)

        if len(sw.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return sw.first()

    def query_port_type(self, resource_id):
        """
        Retrieve :class:`PortType` object from database.

        Query the database for a :class:`PortType` object with given resource
        identifier and return it.

        :param resource_id: Resource identifier uniquely identifying the
            port type to return.
            (See :class:`PortType` for what attribute is the resource identifier)
        :type resouce_id: str

        :return: The port type object matching the given resource identifier
        :rtype: PortType
        """

        if not isinstance(resource_id, str):
            raise TypeError('Cannot query port type with resource id not of type str')

        session = self.Session()
        pt = session.query(PortType)
        pt = pt.filter_by(_description = resource_id)

        if len(pt.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return pt.first()

    def query_vlan(self, resource_id):
        """
        Retrieve :class:`Vlan` object from database.

        Query the database for a :class:`Vlan` object with given resource
        identifier and return it.

        :param resource_id: Resource identifier uniquely identifying the
            vlan to return.
            (See :class:`Vlan` for what attribute is the resource identifier)
        :type resouce_id: str

        :return: The vlan object matching the given resource identifier
        :rtype: Vlan
        """

        if not isinstance(resource_id, int):
            raise TypeError('Cannot query vlan with resource id not of type int')

        session = self.Session()
        vl = session.query(Vlan)
        vl = vl.filter_by(_tag = resource_id)

        if len(vl.all()) > 1:
            raise TypeError('DB query resulted in multiple elements but only one was requested')

        return vl.first()

    def query_switch_models(self, **kwargs):
        """
        Retrieve multiple :class:`SwitchModel` objects from database.

        # TODO: Implement and document query_switch_models() correctly
        """

        # Check all arguments before querying
        SwitchModel.check_params(**kwargs)

        # Query
        session = self.Session()
        models = session.query(SwitchModel)

        # Filter with SQL
        for key, val in kwargs.items():
            if key == 'size':
                models = models.filter_by(_size = val)
            elif key == 'port_type':
                val = self.query_port_type(val)
                if val is None:
                    raise ValueError('Given port type does not exist')
            else:
                raise TypeError(
                    "Cannot query switch models with unexpected filter '{}'".format(key))

        models = models.all()

        # TODO: When querying switch models don't filter manually but let database do the work

        # Filter manually
        for key, val in kwargs.items():
            if key == 'size':
                pass
            elif key == 'port_type':
                new_models = list()
                pt = val
                for model in models:
                    for port in model.ports:
                        if port['port_type'] == pt:
                            new_models.append(model)
                            break
                models = new_models
            else:
                raise TypeError(
                    "Cannot query switch models with unexpected filter '{}'".format(key))

        return models

    def query_switches(self, **kwargs):
        """
        Retrieve multiple :class:`Switch` objects from database.

        # TODO: Implement and document query_switches() correctly
        """

        # Check all arguments before querying
        Switch.check_params(**kwargs)

        # Query
        session = self.Session()
        switches = session.query(Switch)

        # Filter with SQL
        for key, val in kwargs.items():
            if key == 'location':
                if not isinstance(val, int):
                    raise TypeError('Given location of switch is not of type int')
                switches = switches.filter_by(_location = val)
            elif key == 'model':
                kwargs['model'] = self.query_switch_model(val)
                if kwargs['model'] is None:
                    raise ValueError(
                        "Got invalid switch model '{}' - switch model does not exist")
                switches = switches.filter_by(_model = kwargs['model'])
            elif key == 'vlan':
                if not isinstance(val, int):
                    raise TypeError('Given vlan of port of switch is not of type int')
            else:
                raise TypeError(
                    "Cannot query switches with unexpected filter '{}'".format(key))

        switches = switches.all()

        # TODO: When querying switches don't filter manually but let database do the work

        # Filter manually
        for key, val in kwargs.items():
            if key == 'location':
                pass
            elif key == 'model':
                pass
            elif key == 'vlan':
                new_switches = list()
                vl = val
                for switch in switches:
                    for port in switch.ports:
                        if vl in port['vlans']:
                            new_switches.append(switch)
                            break
                switches = new_switches
            else:
                raise TypeError(
                    "Cannot query switches with unexpected filter '{}'".format(key))

        return switches

    def query_port_types(self, **kwargs):
        """
        Retrieve multiple :class:`PortType` objects from database.

        # TODO: Implement and document query_port_types() correctly
        """

        # Check all arguments before querying
        PortType.check_params(**kwargs)

        # Query
        session = self.Session()
        pts = session.query(PortType)

        # Filter
        for key, val in kwargs.items():
            if key == 'speed':
                pts = pts.filter_by(_speed = val)
            else:
                raise TypeError(
                    "Cannot query port types with unexpected filter '{}'".format(key))

        return pts.all()

    def query_vlans(self, **kwargs):
        """
        Retrieve multiple :class:`Vlan` objects from database.

        # TODO: Implement and document query_vlans() correctly
        """

        # Check all arguments before querying
        Vlan.check_params(**kwargs)

        # Query
        session = self.Session()
        vls = session.query(Vlan)

        # Filter
        for key, val in kwargs.items():
            if key == 'description':
                vls = vls.filter_by(_description = val)
            else:
                raise TypeError(
                    "Cannot query port types with unexpected filter '{}'".format(key))

        return vls.all()


    def delete_switch_model(self, resource_id):
        """
        Delete a switch model from the database.

        Can only delete a switch model from the database if it is not still
        in use by a switch. Will only delete switch model if there is not
        still a switch which uses the given switch model as its model.

        :param resource_id: Resource identifier uniquely identifying the
            switch model to delete.
            (See :class:`SwitchModel` for what attribute is the resource identifier)
        :type resouce_id: str
        """

        # Check switch model
        sm = self.query_switch_model(resource_id)
        if sm is None:
            raise ValueError('Given switch model does not exist')

        # Check if there are switches still using this model
        affected_sw = self.query_switches(model = resource_id)
        if not isinstance(affected_sw, list):
            raise TypeError('Expected list of switches to be of type list')
        if len(affected_sw) > 0:
            raise ValueError('Given switch model is still in use')

        # Delete switch model
        session = self.Session()
        session.delete(sm)
        session.commit()

    def delete_switch(self, resource_id):
        """
        Delete a switch from the database.

        :param resource_id: Resource identifier uniquely identifying the
            switch to delete.
            (See :class:`Switch` for what attribute is the resource identifier)
        :type resouce_id: str
        """

        # Check switch
        sw = self.query_switch(resource_id)
        if sw is None:
            raise ValueError('Given switch does not exist')

        # Delete switch
        session = self.Session()
        session.delete(sw)
        session.commit()

    def delete_port_type(self, resource_id):
        """
        Delete a port type from the database.

        Can only delete a port type from the database if it is not still
        in use by a port of a switch model.
        Will only delete port type if there is not still a switch model which
        uses the given port type on one of its ports.

        :param resource_id: Resource identifier uniquely identifying the
            port type to delete.
            (See :class:`PortType` for what attribute is the resource identifier)
        :type resouce_id: str
        """

        # Check port type
        pt = self.query_port_type(resource_id)
        if pt is None:
            raise ValueError('Given port type does not exist')

        # Check if there are switch models still using this port type
        affected_sm = self.query_switch_models(port_type = resource_id)
        if not isinstance(affected_sm, list):
            raise TypeError('Expected list of switch models to be of type list')
        if len(affected_sm) > 0:
            raise ValueError('Given port type is still in use')

        # Delete port type
        session = self.Session()
        session.delete(pt)
        session.commit()

    def delete_vlan(self, resource_id):
        """
        Delete a vlan from the database.

        Can only delete a vlan from the database if it is not still in use by a
        port of a switch.
        Will only delete vlan if there is not still a switch which uses the given
        vlan on one of its ports.

        :param resource_id: Resource identifier uniquely identifying the vlan to
            delete.
            (See :class:`Vlan` for what attribute is the resource identifier)
        :type resouce_id: str
        """

        # Check vlan
        vl = self.query_vlan(resource_id)
        if vl is None:
            raise ValueError('Given vlan does not exist')

        # Check if there are switch ports still using this vlan
        affected_sw = self.query_switches(vlan = resource_id)
        if not isinstance(affected_sw, list):
            raise TypeError('Expected list of switches to be of type list')
        if len(affected_sw) > 0:
            raise ValueError('Given vlan is still in use')

        # Delete vlan
        session = self.Session()
        session.delete(vl)
        session.commit()


    def modify_switch_model(self, resource_id, **kwargs):
        """
        Modify a :class:`SwitchModel` object in the database.

        All given attributes of switch model will be modified.
        Attributes not given will not be changed and will keep their current
        state.

        :param resource_id: Resource identifier uniquely identifying the
            switch model to modify.
            (See :class:`SwitchModel` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of switch model to change.
            Possible parameters are public attributes of :class:`SwitchModel` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified switch model
        :rtype: SwitchModel
        """

        # Check if switch model exists
        sm = self.query_switch_model(resource_id)
        if sm is None:
            raise ValueError("Given switch model '{}' does not exist"
                .format(resource_id))

        # Replace list of ports with list of port objects
        if 'ports' in kwargs:
            kwargs['ports'] = self._port_models_from_dict(kwargs['ports'])

        # Check all arguments before making any changes
        kwargs = SwitchModel.check_params(**kwargs)

        # Apply modifications
        if 'ports' in kwargs:
            ports = kwargs.pop('ports')
            sm.modify_ports(ports)
        for key, val in kwargs.items():
            setattr(sm, key, val)

        session = self.Session()
        session.add(sm)
        session.commit()

        return sm

    def modify_switch(self, resource_id, **kwargs):
        """
        Modify a :class:`Switch` object in the database.

        All given attributes of switch will be modified.
        Attributes not given will not be changed and will keep their current
        state.

        :param resource_id: Resource identifier uniquely identifying the
            switch to modify.
            (See :class:`Switch` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of switch to change.
            Possible parameters are public attributes of :class:`Switch` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified switch
        :rtype: Switch
        """

        # Check if switch exists
        sw = self.query_switch(resource_id)
        if sw is None:
            raise ValueError("Given switch '{}' does not exist"
                .format(resource_id))

        # Replace list of ports with list of port objects
        if 'ports' in kwargs:
            kwargs['ports'] = self._ports_from_dict(kwargs['ports'])

        # Replace switch model string with switch model object
        if 'model' in kwargs:
            kwargs['model'] = self.query_switch_model(kwargs['model'])

        # Check all arguments before making any changes
        Switch.check_params(**kwargs)

        # Apply modifications
        if 'ports' in kwargs:
            ports = kwargs.pop('ports')
            sw.modify_ports(ports)
        for key, val in kwargs.items():
            setattr(sw, key, val)

        session = self.Session()
        session.add(sw)
        session.commit()

        return sw

    def modify_port_type(self, resource_id, **kwargs):
        """
        Modify a :class:`PortType` object in the database.

        All given attributes of port type will be modified.
        Attributes not given will not be changed and will keep their current
        state.

        :param resource_id: Resource identifier uniquely identifying the
            port type to modify.
            (See :class:`PortType` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of port type to change.
            Possible parameters are public attributes of :class:`PortType` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified port type object
        :rtype: PortType
        """

        # Check if port type exists
        pt = self.query_port_type(resource_id)
        if pt is None:
            raise ValueError("Given port type '{}' does not exist"
                .format(resource_id))

        # Check all arguments before making any changes
        kwargs = PortType.check_params(**kwargs)

        # Apply modifications
        for key, val in kwargs.items():
            setattr(pt, key, val)

        session = self.Session()
        session.add(pt)
        session.commit()

        return pt

    def modify_vlan(self, resource_id, **kwargs):
        """
        Modify a :class:`Vlan` object in the database.

        All given attributes of vlan will be modified.
        Attributes not given will not be changed and will keep their current
        state.

        :param resource_id: Resource identifier uniquely identifying the
            vlan to modify.
            (See :class:`Vlan` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of vlan to change.
            Possible parameters are public attributes of :class:`Vlan` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified vlan object
        :rtype: Vlan
        """

        # Check if vlan exists
        vl = self.query_vlan(resource_id)
        if vl is None:
            raise ValueError("Given VLAN '{}' does not exist"
                .format(resource_id))

        # Check all arguments before making any changes
        kwargs = Vlan.check_params(**kwargs)

        # Apply modifications
        for key, val in kwargs.items():
            setattr(vl, key, val)

        session = self.Session()
        session.add(vl)
        session.commit()

        return vl


    def set_switch_model(self, resource_id, **kwargs):
        """
        Set a :class:`SwitchModel` corresponding to a given resource identifier
        to a given state.

        :class:`SwitchModel` identified by given resource identifier may already
        exist. If it does not already exist it will be created.

        All attributes of switch model will be set to given values.
        Attributes not given but present in already existing :class:`SwitchModel`
        will be set to None or [] or other representation of "not set".

        :param resource_id: Resource identifier uniquely identifying the
            switch model to modify.
            (See :class:`SwitchModel` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of switch model to change.
            Possible parameters are public attributes of :class:`SwitchModel` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified or created switch model
        :rtype: SwitchModel
        """

        # Replace list of ports with list of port objects
        if 'ports' in kwargs:
            kwargs['ports'] = self._port_models_from_dict(kwargs['ports'])

        # Check all arguments before making any changes
        SwitchModel.check_params(**kwargs)

        # Check if switch model exists
        source_sm = self.query_switch_model(resource_id)

        if source_sm is None:
            # Source switch model does not exist:
            # We are creating a new switch model

            # Switch model name is either resource specifier or not set at all
            # (in which case it will be set automatically)
            if 'name' in kwargs:
                if kwargs['name'] != resource_id:
                    raise ValueError('Resource identifier "name" of switch model is ambiguous')
            else:
                kwargs.update({'name': resource_id})

            target_sm = SwitchModel(**kwargs)
            session = self.Session()
            session.add(target_sm)
            session.commit()
            return target_sm
        else:
            # Source switch model exists

            # Source switch model exists so target switch model must not also exist
            if 'name' not in kwargs:
                raise KeyError('Missing necessary argument "name" for setting switch model')
            if resource_id != kwargs['name']:
                if self.query_switch(kwargs['name']) is not None:
                    raise ValueError(
                        'Cannot set switch model with name {} - switch model already exists'
                        .format(kwargs['name']))

            # Create new switch model object with given state
            # and replace old object with it
            target_sm = SwitchModel(**kwargs)

            session = self.Session()
            session.delete(source_sm)
            session.flush()
            session.add(target_sm)
            session.commit()
            return target_sm

    def set_switch(self, resource_id, **kwargs):
        """
        Set a :class:`Switch` corresponding to a given resource identifier
        to a given state.

        :class:`Switch` identified by given resource identifier may already
        exist. If it does not already exist it will be created.

        All attributes of switch will be set to given values.
        Attributes not given but present in already existing :class:`Switch`
        will be set to None or [] or other representation of "not set".

        :param resource_id: Resource identifier uniquely identifying the
            switch to modify.
            (See :class:`Switch` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of switch to change.
            Possible parameters are public attributes of :class:`Switch` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified or created switch
        :rtype: Switch
        """

        # Replace list of ports with list of port objects
        if 'ports' in kwargs:
            kwargs['ports'] = self._ports_from_dict(kwargs['ports'])

        # Replace switch model string with switch model object
        if 'model' in kwargs:
            kwargs['model'] = self.query_switch_model(kwargs['model'])

        # Check all arguments before making any changes
        Switch.check_params(**kwargs)

        # Check if switch exists
        source_sw = self.query_switch(resource_id)

        if source_sw is None:
            # Source switch does not exist:
            # We are creating a new switch

            # Switch name is either resource specifier or not set at all
            # (in which case it will be set automatically)
            if 'name' in kwargs:
                if kwargs['name'] != resource_id:
                    raise ValueError('Resource identifier "name" of switch is ambiguous')
            else:
                kwargs.update({'name': resource_id})

            target_sw = Switch(**kwargs)
            session = self.Session()
            session.add(target_sw)
            session.commit()
            return target_sw
        else:
            # Source switch exists

            # Source switch exists so target switch must not also exist
            if 'name' not in kwargs:
                raise KeyError('Missing necessary argument "name" for setting switch')
            if resource_id != kwargs['name']:
                if self.query_switch(kwargs['name']) is not None:
                    raise ValueError(
                        'Cannot set switch with name {} - switch already exists'
                        .format(kwargs['name']))

            # Create new switch object with given state
            # and replace old object with it
            target_sw = Switch(**kwargs)

            session = self.Session()
            session.delete(source_sw)
            session.flush()
            session.add(target_sw)
            session.commit()
            return target_sw

    def set_port_type(self, resource_id, **kwargs):
        """
        Set a :class:`PortType` corresponding to a given resource identifier
        to a given state.

        :class:`PortType` identified by given resource identifier may already
        exist. If it does not already exist it will be created.

        All attributes of port type will be set to given values.
        Attributes not given but present in already existing :class:`PortType`
        will be set to None or [] or other representation of "not set".

        :param resource_id: Resource identifier uniquely identifying the
            port type to modify.
            (See :class:`PortType` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of port type to change.
            Possible parameters are public attributes of :class:`PortType` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified or created port type
        :rtype: PortType
        """

        # Check all arguments before making any changes
        PortType.check_params(**kwargs)

        # Check if source port type exists
        source_pt = self.query_port_type(resource_id)

        if source_pt is None:
            # Source port type does not exist:
            # We are creating a new port type

            # Port type description is either resource specifier or not set at
            # all (in which case it will be set automatically)
            if 'description' in kwargs:
                if kwargs['description'] != resource_id:
                    raise ValueError('Resource identifier "description" of port type is ambiguous')
            else:
                kwargs.update({'description': resource_id})

            target_pt = PortType(**kwargs)
            session = self.Session()
            session.add(target_pt)
            session.commit()
            return target_pt
        else:
            # Source port type exists

            # Source port type exists so target port type must not also exist
            if 'description' not in kwargs:
                raise KeyError('Missing necessary argument "description" for setting port type')
            if resource_id != kwargs['description']:
                if self.query_port_type(kwargs['description']) is not None:
                    raise ValueError(
                        'Cannot set port type with description {} - port type already exists'
                        .format(kwargs['description']))

            # Create a new port type object with given state
            # and replace old object with it
            target_pt  = PortType(**kwargs)

            session = self.Session()
            session.delete(source_pt)
            session.flush()
            session.add(target_pt)
            session.commit()
            return target_pt

    def set_vlan(self, resource_id, **kwargs):
        """
        Set a :class:`Vlan` corresponding to a given resource identifier
        to a given state.

        :class:`Vlan` identified by given resource identifier may already
        exist. If it does not already exist it will be created.

        All attributes of vlan will be set to given values.
        Attributes not given but present in already existing :class:`Vlan`
        will be set to None or [] or other representation of "not set".

        :param resource_id: Resource identifier uniquely identifying the
            vlan to modify.
            (See :class:`Vlan` for what attribute is the resource identifier)
        :type resouce_id: str

        :param kwargs: Attributes of vlan to change.
            Possible parameters are public attributes of :class:`Vlan` object
            but in a json compatible representation (as nested dict structure)

        :return: The modified or created vlan
        :rtype: Vlan
        """

        # Check all arguments before making any changes
        Vlan.check_params(**kwargs)

        # Check if source vlan exists
        source_vl = self.query_vlan(resource_id)

        if source_vl is None:
            # Source vlan does not exist:
            # We are creating a new vlan

            # Vlan tag is either resource specifier or not set at all
            # (in which case it will be set automatically)
            if 'tag' in kwargs:
                if kwargs['tag'] != resource_id:
                    raise ValueError('Resource identifier "tag" of vlan is ambiguous')
            else:
                kwargs.update({'tag': resource_id})

            target_vl = Vlan(**kwargs)
            session = self.Session()
            session.add(target_vl)
            session.commit()
            return target_vl
        else:
            # Source vlan exists

            # Source vlan exists so target vlan must not also exist
            if 'tag' not in kwargs:
                raise KeyError('Missing necessary argument "tag" for setting vlan')
            if resource_id != kwargs['tag']:
                if self.query_vlan(kwargs['tag']) is not None:
                    raise ValueError(
                        'Cannot set vlan with tag {} - vlan already exists'
                        .format(kwargs['tag']))

            # Create a new vlan object with given state
            # and replace old object with it
            target_vl = Vlan(**kwargs)

            session = self.Session()
            session.delete(source_vl)
            session.flush()
            session.add(target_vl)
            session.commit()
            return target_vl


    def add_switch_model(self, **kwargs):
        """
        Create a new switch model and add it to the database.

        :param kwargs: Parameters for new switch model.
            Possible parameters are public attributes of :class:`SwitchModel` object
            but in a json compatible representation (as nested dict structure)

        :return: The newly added switch model
        :rtype: SwitchModel
        """

        # Check if switch model already exists
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for adding switch model')
        if self.query_switch_model(kwargs['name']) is not None:
            raise ValueError(
                'Cannot add switch model with name {} - switch model already exists'
                .format(kwargs['name']))

        # Replace list of port strings with list of port objects
        if 'ports' in kwargs:
            kwargs['ports'] = self._port_models_from_dict(kwargs['ports'])

        # Create switch model
        sm = SwitchModel(**kwargs)
        session = self.Session()
        session.add(sm)
        session.commit()
        return sm

    def add_switch(self, **kwargs):
        """
        Create a new switch and add it to the database.

        :param kwargs: Parameters for new switch.
            Possible parameters are public attributes of :class:`Switch` object
            but in a json compatible representation (as nested dict structure)

        :return: The newly added switch
        :rtype: Switch
        """

        # Check if switch already exists
        if 'name' not in kwargs:
            raise KeyError('Missing necessary argument "name" for adding switch')
        if self.query_switch(kwargs['name']) is not None:
            raise ValueError(
                'Cannot add switch with name {} - switch already exists'
                .format(kwargs['name']))

        # Replace list of port strings with list of port objects
        if 'ports' in kwargs:
            kwargs['ports'] = self._ports_from_dict(kwargs['ports'])

        # Replace switch model string with switch model object
        if 'model' in kwargs:
            kwargs['model'] = self.query_switch_model(kwargs['model'])

        # Create switch
        sw = Switch(**kwargs)
        session = self.Session()
        session.add(sw)
        session.commit()
        return sw

    def add_port_type(self, **kwargs):
        """
        Create a new port type and add it to the database.

        :param kwargs: Parameters for new port type.
            Possible parameters are public attributes of :class:`PortType` object
            but in a json compatible representation (as nested dict structure)

        :return: The newly added port tpye
        :rtype: PortType
        """

        # Check if port type already exists
        if 'description' not in kwargs:
            raise KeyError('Missing necessary argument "description" for adding port type')
        if self.query_port_type(kwargs['description']) is not None:
            raise ValueError(
                'Cannot add port type with description {} - port type already exists'
                .format(kwargs['description']))

        # Add port type
        pt = PortType(**kwargs)
        session = self.Session()
        session.add(pt)
        session.commit()
        return pt

    def add_vlan(self, **kwargs):
        """
        Create a new vlan and add it to the database.

        :param kwargs: Parameters for new vlan.
            Possible parameters are public attributes of :class:`Vlan` object
            but in a json compatible representation (as nested dict structure)

        :return: The newly added vlan
        :rtype: Vlan
        """

        # Check if vlan already exists
        if 'tag' not in kwargs:
            raise KeyError('Missing necessary argument "tag" for adding vlan')
        if self.query_vlan(kwargs['tag']) is not None:
            raise ValueError(
                'Cannot add vlan with tag {} - vlan already exists'
                .format(kwargs['tag']))

        # Add vlan
        vl = Vlan(**kwargs)
        session = self.Session()
        session.add(vl)
        session.commit()
        return vl


    def _port_models_from_dict(self, ports):
        """
        Convert port models from list of dict of strings to list of port model objects.
        """

        # Check structure before doing anything in order to reduce
        # database queries.
        if not isinstance(ports, list):
            raise TypeError('Given list of ports is not of type list')
        for port in ports:
            if not isinstance(port, dict):
                raise TypeError('Given port is not of type dict')

        # Convert
        port_objs = []
        for port in ports:
            # Convert port type from str to obj
            if 'port_type' in port and port['port_type'] is not None:
                port['port_type'] = self.query_port_type(port['port_type'])

            # Create port object with given parameter
            port_obj = PortModel(**port)
            port_objs.append(port_obj)

        return port_objs

    def _ports_from_dict(self, ports):
        """
        Convert ports from list of dict of strings to list of port objects.
        """

        # Check structure before doing anything in order to reduce
        # database queries.
        if not isinstance(ports, list):
            raise TypeError('Given list of ports is not of type list')
        for port in ports:
            if not isinstance(port, dict):
                raise TypeError('Given port is not of type dict')

        # Convert
        port_objs = []
        for port in ports:
            # Convert vlans from list of str to list of obj
            if 'vlans' in port:
                if not isinstance(port['vlans'], list):
                    raise TypeError('Given list of vlans of port is not of type list')
                port['vlans'] = [ self.query_vlan(v) for v in port['vlans'] ]

                if None in port['vlans']:
                    raise ValueError('Given vlan in list of vlans of port does not exist')


            # Create port object with given parameter
            port_obj = Port(**port)
            port_objs.append(port_obj)

        return port_objs

