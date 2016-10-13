from st2actions.runners.pythonrunner import Action

class Greet(Action):

    def run(self, host_ip, port, total_memory=0, free_memory=0, user_name='root', password='fibranne'):
        self.logger.info("StackStorm\n")
        return True
