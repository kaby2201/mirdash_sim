from app import *

user_model = api.model('users', {
    'guid': fields.String(description='The global unique id across robots that identifies this user'),
    'name': fields.String(required=False, description='The name of the user'),
    'url': fields.String(required=False, description='The URL of the resource'),
    'user_group': fields.String(required=False, description='Url for the user group this user is in'),
    'user_group_id': fields.String(required=False, description='Global id of the user group this user is in')
})

users = [
    {
        "guid": "mirconst-guid-0000-0001-users0000000",
        "name": "MiR",
        "url": "/v2.0.0/users/mirconst-guid-0000-0001-users0000000",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0001-user_groups0",
        "user_group_id": "mirconst-guid-0000-0001-user_groups0"
    },
    {
        "guid": "mirconst-guid-0000-0002-users0000000",
        "name": "Fleet",
        "url": "/v2.0.0/users/mirconst-guid-0000-0002-users0000000",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0001-user_groups0",
        "user_group_id": "mirconst-guid-0000-0001-user_groups0"
    },
    {
        "guid": "mirconst-guid-0000-0003-users0000000",
        "name": "Service",
        "url": "/v2.0.0/users/mirconst-guid-0000-0003-users0000000",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0002-user_groups0",
        "user_group_id": "mirconst-guid-0000-0002-user_groups0"
    },
    {
        "guid": "mirconst-guid-0000-0004-users0000000",
        "name": "Distributor",
        "url": "/v2.0.0/users/mirconst-guid-0000-0004-users0000000",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0003-user_groups0",
        "user_group_id": "mirconst-guid-0000-0003-user_groups0"
    },
    {
        "guid": "mirconst-guid-0000-0005-users0000000",
        "name": "Administrator",
        "url": "/v2.0.0/users/mirconst-guid-0000-0005-users0000000",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0004-user_groups0",
        "user_group_id": "mirconst-guid-0000-0004-user_groups0"
    },
    {
        "guid": "mirconst-guid-0000-0006-users0000000",
        "name": "User",
        "url": "/v2.0.0/users/mirconst-guid-0000-0006-users0000000",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0005-user_groups0",
        "user_group_id": "mirconst-guid-0000-0005-user_groups0"
    },
    {
        "guid": "59117c98-495f-11e9-ba1c-94c69118fd1e",
        "name": "Teknisk",
        "url": "/v2.0.0/users/59117c98-495f-11e9-ba1c-94c69118fd1e",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0005-user_groups0",
        "user_group_id": "mirconst-guid-0000-0005-user_groups0"
    },
    {
        "guid": "6b77aaab-3b7f-11ea-8610-94c69118fd1e",
        "name": "Halvor",
        "url": "/v2.0.0/users/6b77aaab-3b7f-11ea-8610-94c69118fd1e",
        "user_group": "/v2.0.0/user_groups/mirconst-guid-0000-0003-user_groups0",
        "user_group_id": "mirconst-guid-0000-0003-user_groups0"
    }
]


@api.doc(responses={202: 'Successfully retrieve the specified element'})
@api.route('/users')
class Status(Resource):
    @api.marshal_with(user_model)
    def get(self):
        return users

    @api.expect(user_model)
    def post(self):
        users.append(api.payload)
        return {"success": "true", "description": "Successfully added mission to mission queue", "id": "320"}, 201
