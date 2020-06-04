from app import *

getMission_model = api.model('GetMission', {
    'guid': fields.String,
    'name': fields.String,
    'url': fields.String
})

putMission_model = api.model('PutMission', {
    'description': fields.String(max_length=255),
    'group_id': fields.String,
    'hidden': fields.Boolean,
    'name': fields.String(min_length=1, max_length=255),
    'session_id': fields.String
})

getMissionSpecific_model = api.model('GetMissionSpecific', {
    'actions': fields.String,
    'created_by': fields.String,
    'created_by_id': fields.String,
    'description': fields.String,
    'group_id': fields.String,
    'guid': fields.String,
    'has_user_parameters': fields.Boolean,
    'hidden': fields.Boolean,
    'name': fields.String,
    'session_id': fields.String,
    'valid': fields.Boolean,
    'allowed_methods': fields.List(fields.String)
})


class SingleMission:
    def __init__(self, guid, name, allowed_methods, hidden):
        self.guid = guid
        self.name = name
        self.allowed_methods = allowed_methods
        self.created_by_id = 'mirconst-guid-0000-0001-users0000000'
        self.created_by = '/v2.0.0/users/{}'.format(self.created_by_id)
        self.created_by_name = 'MiR'
        self.description = ''
        self.group_id = None
        self.has_user_parameters = True
        self.session_id = None
        self.valid = True
        self.hidden = hidden

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

    def get_url(self):
        return '/missions/{}'.format(self.guid)

    url = property(get_url)

    def get_actions(self):
        return '/v2.0.0/missions/{}/actions'.format(self.guid)

    actions = property(get_actions)

    def get_definition(self):
        return '/v2.0.0/missions/{}/definition'.format(self.guid)

    definition = property(get_definition)


class MissionsDAOClass:
    def __init__(self, mission_arr):
        self.arr = mission_arr
        self.mission_i = {}
        for i, v in enumerate(self.arr):
            self.mission_i[v.guid] = i

    def get(self, guid):
        if guid in self.mission_i:
            return self.arr[self.mission_i[guid]]
        else:
            api.abort(404, "Mission with guid {} doesn't exist".format(guid))

    def put(self, guid, data):
        if guid in self.mission_i:
            i = self.mission_i[guid]
            if 'PUT' in self.arr[i].allowed_methods:
                if 'description' in data:
                    self.arr[i].description = data['description']
                if 'group_id' in data:
                    self.arr[i].group_id = data['group_id']
                if 'hidden' in data:
                    self.arr[i].hidden = data['hidden']
                if 'name' in data:
                    self.arr[i].name = data['name']
                if 'session_id' in data:
                    self.arr[i].session_id = data['session_id']
            else:
                api.abort(403, "Mission with guid {} doesn't allow PUT".format(guid))
        else:
            api.abort(404, "Mission with guid {} doesn't exist".format(guid))

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)


const_mission_methods = ['GET']
mission_methods = ['GET', 'PUT', 'DELETE']
missionsDAO = MissionsDAOClass([
    SingleMission('mirconst-guid-0000-0001-actionlist00', 'Move', const_mission_methods, True),
    SingleMission('mirconst-guid-0000-0003-actionlist00', 'GoToPositionPrototype', const_mission_methods, True),
    SingleMission('mirconst-guid-0000-0004-actionlist00', 'ChargeAtStation', const_mission_methods, True),
    SingleMission('mirconst-guid-0000-0006-actionlist00', 'StageAtPosition', const_mission_methods, True),
    SingleMission('mirconst-guid-0000-0005-actionlist00', 'Dock', const_mission_methods, True),
    SingleMission('mirconst-guid-0000-0007-actionlist00', 'PickupCart', const_mission_methods, True),
    SingleMission('mirconst-guid-0000-0008-actionlist00', 'PlaceCart', const_mission_methods, True),
    SingleMission('1727f99d-1671-11ea-a892-94c69118fd1e', 'Frem og tilbake', mission_methods, False),
    SingleMission('42d851ba-40fa-11ea-a313-94c69118fd1e', 'Tute tur', mission_methods, False),
    SingleMission('9aca0130-82fc-11ea-8e4d-94c69118fd1e', 'Test2', mission_methods, False),
    SingleMission('74c6adc6-839f-11ea-bfdf-94c69118fd1e', 'A til B', mission_methods, False),
    SingleMission('a784d483-83a7-11ea-bfdf-94c69118fd1e', 'Kont', mission_methods, False),
    SingleMission('f6d6607a-845d-11ea-a732-94c69118fd1e', 'Gruppe 5 hall 3', mission_methods, False),
    SingleMission('1a29c894-8463-11ea-a732-94c69118fd1e', 'Hall 3 gruppe 5', mission_methods, False),
    SingleMission('5566ea90-848a-11ea-856f-94c69118fd1e', 'Lagersjefen', mission_methods, False)
])


@api.route('/api/v2.0.0/missions')
class Missions(Resource):
    @auth_required
    @ns.marshal_with(getMission_model)
    def get(self):
        return missionsDAO.arr, 200


@api.route('/api/v2.0.0/missions/<string:guid>')
@ns.param('guid', 'Mission guid')
class MissionsGuid(Resource):
    @auth_required
    @ns.marshal_with(getMissionSpecific_model)
    def get(self, guid):
        return missionsDAO.get(guid), 200

    @auth_required
    @ns.expect(putMission_model)
    @ns.marshal_with(getMissionSpecific_model)
    def put(self, guid):
        if api.payload is not None:
            return missionsDAO.put(guid, api.payload), 200
        else:
            api.abort(400, 'Request body needs to be application/json')
