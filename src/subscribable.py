import logging

class Subscribable():
    """
    Mixin for handling subscriptions to messages.

    The standard format of messages is as follows:
    >>> {
    >>>     "command_id": "some_command",
    >>>     "arguments": []
    >>> }

    Subscribable.notify dispatches messages to the subscriber, they are dispatched
    to the handle_{command_id} method on the subscriber, if it is there.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subscriptions = {'_all': []}
        self._logger = logging.getLogger(__name__)

    def _debug_subscribers(self, msg="Subscriber list"):
        self._logger.info(msg)
        for key, value in self._subscriptions.items():
            sub_id_list = "".join(map(lambda o: str(id(o)), value))
            self._logger.info("Subscribers for {key}: {subs}".format(key=key,
                                                                     subs=sub_id_list))

    def subscribe(self, receiver, command_ids=None):
        """
        Subscribe to messages from this GameConnection
        :param receiver: object to receive messages
        :param command_ids: Optional list of command_ids to subscribe to
        :return: None
        """
        print("{} ADDING SUBSCRIBER {}".format(self, receiver))
        print(self, self._subscriptions, id(self))
        if not command_ids:
            command_ids = ['_all']
        for i in command_ids:
            if i in self._subscriptions:
                self._subscriptions[i].append(receiver)
            else:
                self._subscriptions[i] = [receiver]
        print("SUBSCRIBER ADDED")
        print(self, self._subscriptions, id(self))

    def notify(self, message):
        """
        Notify subscribers that a message of interest arrived
        :param message:
        :return:
        """
        print("NOTIFYING SUBS ON {}".format(id(self)))
        command_id = message.get("command_id")
        arguments = message.get("arguments", [])
        assert isinstance(command_id, str)
        cmd_name = 'handle_{cmd_id}'.format(cmd_id=command_id)
        print(self, self._subscriptions)
        if command_id in self._subscriptions:
            for sub in self._subscriptions[command_id]:
                if hasattr(sub, cmd_name):
                    getattr(sub, cmd_name)(arguments)
                else:
                    self._logger.info("Subscriber {sub} does not have {cmd_name}".format(
                        sub=sub,
                        cmd_name=cmd_name
                    ))
        for sub in self._subscriptions['_all']:
            if hasattr(sub, cmd_name):
                getattr(sub, cmd_name)(arguments)

    def unsubscribe(self, receiver, command_ids=None):
        """
        Unusubscribe a given function from given message ids.

        Be careful to unsubscribe from exactly the messages that the receiver
        has subscribed to.
        :param receiver: function to unsubscribe
        :param command_ids: Command identifiers to unsubscribe from
        :return: None
        """
        self._logger.debug("Unsubscribing {receiver} from {commands} on {self}".format(
            receiver=receiver,
            commands=command_ids,
            self=self
        ))
        if not command_ids:
            command_ids = ['_all']
        for i in command_ids:
            if i in self._subscriptions and receiver in self._subscriptions[i]:
                self._subscriptions[i].remove(receiver)
