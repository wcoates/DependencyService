from Model.RequestModel import S3Access
from Model.Status import RequestState


class S3AccessSuccessful:
    def __init__(self, S3Access, RequestState):
        self.S3Access = S3Access
        self.RequestState = RequestState

    def run(self):
        print("Adding S3 access for: ", self.S3Access.user_id)


class S3AccessFailure:
    def __init__(self, S3Access, RequestState):
        self.S3Access = S3Access
        self.RequestState = RequestState

    def run(self):
        print("Adding S3 access for: ", self.S3Access.user_id)
        self.RequestState.set_fail_status()
        self.RequestState.add_problem("Something went wrong")
