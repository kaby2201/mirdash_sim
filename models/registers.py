from app import *

registers_model = api.model('register', {
    'id': fields.Integer,
    'label': fields.String,
    'url': fields.String,
    'value': fields.Float
})


class SingleRegister:
    def __init__(self, i, label, value):
        self.id = i
        self.label = label
        if i > 200:
            self.value = value
        else:
            self.value = float(int(value))
        self.url = '/api/v2.0.0/registers/{}'.format(i)

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)


class RegisterDAOClass:
    def __init__(self):
        self.dict = {}
        for i in range(1, 201):
            self.dict[i] = SingleRegister(i, '', 0.0)

    def get(self, i):
        if i in self.dict:
            return self.dict[i]
        else:
            api.abort(404, "Register {} doesn't exist".format(i))

    def set(self, i, data):
        if i in self.dict:
            if 'label' in data:
                self.dict[i].label = data['label']
            if 'value' in data:
                self.dict[i].value = data['value']
            return self.dict[i]
        else:
            api.abort(404, "Register {} doesn't exist".format(i))

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)


RegisterDAO = RegisterDAOClass()


@api.route('/api/v2.0.0/registers')
class Register(Resource):
    @auth_required
    @ns.marshal_with(registers_model)
    def get(self):
        return list(RegisterDAO.dict.values()), 200


@api.route('/api/v2.0.0/registers/<int:i>')
@ns.param('i', 'Register id')
class RegisterID(Resource):
    @auth_required
    @ns.marshal_with(registers_model)
    def get(self, i):
        return RegisterDAO.get(i), 200

    @auth_required
    @ns.expect(registers_model)
    @ns.marshal_with(registers_model)
    def put(self, i):
        return RegisterDAO.set(i, api.payload), 200

    @auth_required
    @ns.expect(registers_model)
    @ns.marshal_with(registers_model)
    def post(self, i):
        return RegisterDAO.set(i, api.payload), 201
