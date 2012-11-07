import sys
import multiprocessing
import threading
from pinder import Campfire
import results

election_results = {}


def do_election_updates(room):
    global election_results

    print 'Checking feed...'
    update = results.fresh_data()

    changes = []

    states = update.keys()
    states.sort()
    for state in states:
        if (update[state] is not None) and (
                election_results[state] is None or
                election_results[state]['summary'] !=
                update[state]['summary']):
            changes.append(update[state]['summary'])
            election_results[state] = update[state]
    if len(changes):
        room.paste('\n'.join(changes))

    # Start a new timer
    t = threading.Timer(900, do_election_updates, args=(room,))
    t.start()


def handle_message(message):
    if message[u'type'] != u'TextMessage':
        return
    return


def handle_exception(ex):
    print 'Received exception %s' % ex
    sys.exit(1)


def manage_campfire():
    import json
    f = open('config.json', 'r')
    config = json.load(f)
    f.close()

    cf = Campfire(config['campfire_prefix'], config['auth_token'])
    room = cf.find_room_by_name(config['room_name'])
    room.join()
    print 'Ready'

    do_election_updates(room)

    # Block forever
    room.listen(handle_message, handle_exception)


def main():
    global election_results
    election_results = results.fresh_data()
    #election_results['Vermont'] = {'summary': 'test'}

    keep_running = True
    while keep_running:
        print 'Starting campfire process'
        p = multiprocessing.Process(target=manage_campfire)
        p.start()
        p.join()
        if p.exitcode == 1:
            keep_running = False
            print 'Not restarting campfire process'
        else:
            import time
            time.sleep(3)
    print 'Terminating'
    return 0

if __name__ == '__main__':
    sys.exit(main())
