from __future__ import absolute_import
from ansible.plugins.callback import CallbackBase
from ansible import constants as C

import json
import pprint
from os.path import basename

# JSON Lines STDOUT callback module for Ansible.
# 
# This callback module prints Ansible events out to STDOUT as JSON Lines.
# The event consists of a type and data. The data has a different structure
# depending on the event type. 
class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'json-lines'

    # The following is a list of supported event types
    PLAYBOOK_START      = "PLAYBOOK_START"
    PLAY_START          = "PLAY_START"
    TASK_START          = "TASK_START"
    RUNNER_OK           = "RUNNER_OK"
    RUNNER_FAILED       = "RUNNER_FAILED"
    RUNNER_SKIPPED      = "RUNNER_SKIPPED"
    RUNNER_UNREACHABLE  = "RUNNER_UNREACHABLE"
    CLEANUP_TASK_START  = "CLEANUP_TASK_START"
    HANDLER_TASK_START  = "HANDLER_TASK_START"
    RUNNER_ITEM_OK      = "RUNNER_ITEM_OK"
    RUNNER_ITEM_FAILED  = "RUNNER_ITEM_FAILED"
    RUNNER_ITEM_SKIPPED = "RUNNER_ITEM_SKIPPED"
    RUNNER_ITEM_RETRY   = "RUNNER_ITEM_RETRY"

    def _new_event(self, eventType, eventData):
        return {
            'eventType': eventType,
            'eventData': eventData
        }

    def _new_task(self, task):
        return {
            'name':task.name,
            'id': str(task._uuid)
        }

    def _print_event(self, event):
        print(json.dumps(event, sort_keys = False))

    def __init__(self):
        super(CallbackModule, self).__init__()

    # def v2_on_any(self, *args, **kwargs):
    #     self.on_any(args, kwargs)

    # def v2_runner_on_no_hosts(self, task):
    #     self.runner_on_no_hosts()

    # def v2_runner_on_async_poll(self, result):
    #     host = result._host.get_name()
    #     jid = result._result.get('ansible_job_id')
    #     #FIXME, get real clock
    #     clock = 0
    #     self.runner_on_async_poll(host, result._result, jid, clock)

    # def v2_runner_on_async_ok(self, result):
    #     host = result._host.get_name()
    #     jid = result._result.get('ansible_job_id')
    #     self.runner_on_async_ok(host, result._result, jid)

    # def v2_runner_on_async_failed(self, result):
    #     host = result._host.get_name()
    #     jid = result._result.get('ansible_job_id')
    #     self.runner_on_async_failed(host, result._result, jid)

    # def v2_runner_on_file_diff(self, result, diff):
    #     print "v2_runner_on_file_diff"

    def v2_playbook_on_start(self, playbook):
        data = {
            'name': basename(playbook._file_name)
        }
        e = self._new_event(self.PLAYBOOK_START, data)
        self._print_event(e)

    # def v2_playbook_on_notify(self, result, handler):
    #     host = result._host.get_name()
    #     self.playbook_on_notify(host, handler)

    # def v2_playbook_on_no_hosts_matched(self):
    #     self.playbook_on_no_hosts_matched()

    # def v2_playbook_on_no_hosts_remaining(self):
    #     self.playbook_on_no_hosts_remaining()

    def v2_playbook_on_task_start(self, task, is_conditional):
        event_data = self._new_task(task)
        e = self._new_event(self.TASK_START, event_data)
        self._print_event(e)
        

    def _on_runner_result(self, event_type, result):
        event_data = {
            'host': result._host.name,
            'result': result._result
        }
        e = self._new_event(event_type, event_data)
        self._print_event(e)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._on_runner_result(self.RUNNER_FAILED, result)

    def v2_runner_on_ok(self, result):
        self._on_runner_result(self.RUNNER_OK, result)

    def v2_runner_on_skipped(self, result):
        self._on_runner_result(self.RUNNER_SKIPPED, result)

    def v2_runner_on_unreachable(self, result):
        self._on_runner_result(self.RUNNER_UNREACHABLE, result)

    def v2_playbook_on_cleanup_task_start(self, task):
        event_data = self._new_task(task)
        e = self._new_event(self.CLEANUP_TASK_START, event_data)
        self._print_event(e)

    def v2_playbook_on_handler_task_start(self, task):
        event_data = self._new_task(task)
        e = self._new_event(self.HANDLER_TASK_START, event_data)
        self._print_event(e)

    # def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
    #     self.playbook_on_vars_prompt(varname, private, prompt, encrypt, confirm, salt_size, salt, default)

    # def v2_playbook_on_setup(self):
    #     self.playbook_on_setup()

    # def v2_playbook_on_import_for_host(self, result, imported_file):
    #     host = result._host.get_name()
    #     self.playbook_on_import_for_host(host, imported_file)

    # def v2_playbook_on_not_import_for_host(self, result, missing_file):
    #     host = result._host.get_name()
    #     self.playbook_on_not_import_for_host(host, missing_file)

    def v2_playbook_on_play_start(self, play):
        data = {
            'name': play.name
        }
        e = self._new_event(self.PLAY_START, data)
        self._print_event(e)
        return

    # def v2_playbook_on_stats(self, stats):
    #     self.playbook_on_stats(stats)

    # def v2_on_file_diff(self, result):
    #     if 'diff' in result._result:
    #         host = result._host.get_name()
    #         self.on_file_diff(host, result._result['diff'])

    # def v2_playbook_on_include(self, included_file):
    #     print "v2_playbook_on_include"

    def v2_runner_item_on_ok(self, result):
        self._on_runner_result(self.RUNNER_ITEM_OK, result)

    def v2_runner_item_on_failed(self, result):
        self._on_runner_result(self.RUNNER_ITEM_FAILED, result)

    def v2_runner_item_on_skipped(self, result):
        self._on_runner_result(self.RUNNER_ITEM_SKIPPED, result)

    def v2_runner_retry(self, result):
        self._on_runner_result(self.RUNNER_ITEM_RETRY, result)

