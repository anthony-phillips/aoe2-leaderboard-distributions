from enum import IntEnum
import json
from math import floor, ceil
from requests import get
from scipy.stats import gaussian_kde
from matplotlib import pyplot as plt

LEADERBOARD_API = 'https://aoe2.net/api/leaderboard'

LEADERBOARD_IDS = {
   '1v1 death' : {'id':1, 'name':'1v1 Deathmatch'},
   'team death' : {'id':2, 'name':'Team Deathmatch'},
   '1v1 random' : {'id':3, 'name':'1v1 Random Map'},
   'team random' : {'id':4, 'name':'Team Random Map'}
}

BIN_SIZE = 100
LEADERBOARD_ID = LEADERBOARD_IDS['team random']

ratings = []

while True:
   params = {
      'game' : 'aoe2de',
      'leaderboard_id' : LEADERBOARD_ID['id'],
      'start' : len(ratings) + 1,
      'count' : 10000
   }

   api_response = get(LEADERBOARD_API, params=params)

   leaderboard = json.loads(api_response.text)

   if len(leaderboard['leaderboard']) == 0:
      break

   for player in leaderboard['leaderboard']: ratings.append(player['rating'])

ratings.sort(reverse=True)

bot_round = floor(ratings[-1] / BIN_SIZE) * BIN_SIZE
top_round = ceil(ratings[0] / BIN_SIZE) * BIN_SIZE

fig = plt.figure()
ax_hist = fig.add_subplot(111)
bins = range(bot_round, top_round+1, 100)
ax_hist.hist(ratings, bins=bins)
ax_hist.set_xticks(bins)
ax_hist.set_xlabel('Rating')
ax_hist.set_ylabel('Players')

ax_dist = ax_hist.twinx()
distribution = gaussian_kde(ratings)
xs = range(bot_round, top_round)
ax_dist.plot(xs, distribution(xs), c='tab:orange')
ax_dist.set_ylim(bottom=0)
ax_dist.set_ylabel('Probability')

plt.title('{} Ratings Distribution'.format(LEADERBOARD_ID['name']))
plt.show()