from models.mission import *
from threading import Semaphore, Thread
from ThreadedHeap import ThreadedHeap
from datetime import datetime
from main import mainvars

getMissionQueues_model = api.model('GetMissionQueue', {
    'id': fields.Integer,
    'state': fields.String,
    'url': fields.String
})

postMissionQueues_model = api.model('PostMissionQueue', {
    'fleet_schedule_guid': fields.String(max_length=36),
    'message': fields.String(max_length=200),
    'mission_id': fields.String(min_length=1),  # REQUIRED
    'parameters': fields.Wildcard,
    'priority': fields.Float
})

getMissionQueuesSpecific_model = api.model('GetMissionQueueSpecific', {
    'actions': fields.String,
    'control_posid': fields.String,
    'control_state': fields.Integer,
    'created_by': fields.String,
    'created_by_id': fields.String,
    'description': fields.String,
    'finished': fields.DateTime,
    'fleet_schedule_guid': fields.String,
    'id': fields.Integer,
    'message': fields.String,
    'mission': fields.String,
    'mission_id': fields.String,
    'ordered': fields.DateTime,
    'parameters': fields.List(fields.Arbitrary),
    'priority': fields.Integer,
    'started': fields.DateTime,
    'state': fields.String,
    'allowed_methods': fields.List(fields.String)
})

# TODO: find the real values
state_aborted = 'Aborted'
state_done = 'Done'
state_pending = 'Pending'
state_running = 'Running'


class MissionQueueItem:
    def __init__(self, i, priority, fleet_schedule_guid, message, mission_id, parameters):
        self.id = i
        self.priority = priority
        self.fleet_schedule_guid = fleet_schedule_guid
        self.message = message
        self.mission_id = mission_id
        self.state = state_pending
        self.control_state = 0  # TODO: change to 1 when the mission waits for something
        self.parameters = parameters
        self.control_posid = None
        self.started = None
        self.finished = None
        self.ordered = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        self.allowed_methods = ['PUT', 'GET', 'DELETE']
        self.aborted_callback = None

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

    def __lt__(self, other):
        return self.priority > other.priority if self.priority != other.priority else self.id < other.id

    def stop(self):
        if self.state in [state_pending[0], state_running[0]]:
            self.state = 'Aborted'
            self.finished = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            if self.aborted_callback is not None:
                try:
                    self.aborted_callback()
                except TypeError:
                    pass

    def done(self):
        self.state = state_done

    def get_actions(self):
        return '/v2.0.0/mission_queue/{}/actions'.format(self.id)

    actions = property(get_actions)

    def get_mission(self):
        return '/v2.0.0/missions/{}'.format(self.mission_id)

    mission = property(get_mission)

    def set_aborted_callback(self, callback):
        self.aborted_callback = callback

    def run(self):
        self.state = state_running
        self.started = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    def get_url(self):
        return '/v2.0.0/mission_queue/{}'.format(self.id)

    url = property(get_url)


class MissionQueueDAOClass:
    def __init__(self):
        self.pending_queue = ThreadedHeap()
        self.all_queue = []
        self.current_i = 0
        self.running_i = 0

    def add(self, post_data):
        if 'mission_id' not in post_data:
            api.abort(400, 'mission_id is required')
            return
        self.current_i += 1
        item = MissionQueueItem(
            self.current_i,
            post_data.get('priority', 0),
            post_data.get('fleet_schedule_guid', ''),
            post_data.get('message', ''),
            post_data['mission_id'],
            post_data.get('parameters', []))
        self.pending_queue.heappush(item)
        self.all_queue.append(item)
        return item.__dict__

    def stop_all(self):
        # TODO: if the missions do something, stop them
        map(lambda item: item.stop(), self.all_queue)

    def stop(self, i):
        # TODO: if the missions do something, stop them
        self.all_queue[i-1].stop()

    def get(self, i):
        if 0 <= i <= self.current_i:
            return self.all_queue[i-1]
        else:
            api.abort(404, "Mission with id {} doesn't exist".format(i))


missionQueueDAO = MissionQueueDAOClass()


def mission_runner_func():
    timer_semaphore = Semaphore(value=0)
    while True:
        item = missionQueueDAO.pending_queue.heappop()
        if item is None:
            break
        if item.state != state_pending:
            continue
        if mainvars.state_id == 4:
            mainvars.unpause_mutex.acquire()
            mainvars.unpause_mutex.release()
        item.set_aborted_callback(lambda: timer_semaphore.release())
        item.run()
        missionQueueDAO.running_i = item.id
        aborted = timer_semaphore.acquire(timeout=20)
        item.set_aborted_callback(None)
        if not aborted:
            item.done()
        timer_semaphore.acquire(blocking=False)


mission_runner = Thread(target=mission_runner_func)
mission_runner.daemon = True
mission_runner.start()


@api.route('/api/v2.0.0/mission_queue')
class MissionQueue(Resource):
    @auth_required
    @ns.marshal_with(getMissionQueues_model)
    def get(self):
        return missionQueueDAO.all_queue

    @auth_required
    @ns.expect(postMissionQueues_model)
    @ns.marshal_with(getMissionSpecific_model)
    def post(self):
        if api.payload is not None:
            return missionQueueDAO.add(api.payload)
        api.abort(400, 'Request body needs to be application/json')



@api.route('/api/v2.0.0/mission_queue/<int:i>')
@ns.param('i', 'Mission id')
class MissionQueueSpecific(Resource):
    @auth_required
    @ns.marshal_with(getMissionQueuesSpecific_model)
    def get(self, i):
        return missionQueueDAO.get(i)
