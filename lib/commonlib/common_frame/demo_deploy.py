# coding=utf-8
from commonlib.common_frame import frame_runner
from commonlib.common_frame.deploy_frame import DeployFrame


class DemoDeploy(DeployFrame):

    def __aa(self):
        pass

    def get_inner_deploy(self):
        out = self

        class InnerDemoDeploy(DeployFrame):

            def step(self, retry=False):
                print("runner id " + str(self._runner_id) + " step")
                out.__aa()
                return frame_runner.NEXT_TYPE_CONTINUE, ""

            def check(self, retry=False):
                return frame_runner.NEXT_TYPE_CONTINUE, ""

    def step(self, retry=False):
        tmp = []
        for a in range(10, 20):
            tmp.append(DemoDeploy.InnerDemoDeploy("aaa", str(a)))
        return self.runner(tmp, retry, )

    def check(self, retry=False):
        print("_check")
        return frame_runner.NEXT_TYPE_CONTINUE, ""


if __name__ == '__main__':
    DemoDeploy("172.28.100.111", "demo_deploy").env_deploy(True)
