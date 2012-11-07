import requests
import json

stats = {}


def fresh_data():
    update = {}
    url = ('https://pollinglocation.googleapis.com/results?'
           'electionid=2820&_=45075009')
    r = requests.get(url)
    if r.ok:
        d = json.loads(r.text[12:-15])
        vote_data = d['table']['rows']
        for item in vote_data:
            state_name = item[64]

            votes_obama = item[0]
            votes_romney = item[4]
            votes_total = item[65]

            if votes_total == 0:
                update[state_name] = None  # no data
            else:
                pct_obama = 100.0 * votes_obama / votes_total
                pct_romney = 100.0 * votes_romney / votes_total

                if votes_obama > votes_romney:
                    winner = "Obama"
                else:
                    winner = "Romney"

                ballot_boxes_num = item[66]
                ballot_boxes_counted = item[67]
                pct_counted = 100.0 * ballot_boxes_counted / ballot_boxes_num

                summary = ('%s: %s leading (%.1f%% O vs %.1f%% R, %.1f%% '
                           'votes counted)') % (state_name,
                                                winner,
                                                pct_obama,
                                                pct_romney,
                                                pct_counted)
                state_data = {'summary': summary,
                              'pct_obama': pct_obama,
                              'pct_romney': pct_romney,
                              'pct_counted': pct_counted,
                              }

                update[state_name] = state_data

    return update
