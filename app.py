# streamlit run app.py

#packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings


# Ignore all warnings
warnings.filterwarnings("ignore")

hunter = {}
pet = {}

# Initialize session state
if 'prev_sims' not in st.session_state:
    st.session_state.prev_sims = []

########################################################
      #### Below code from flori's notebook ####
########################################################

#@title Hunter Setup
def make_hunter(weapons, attributes):

    hunter = {}

    # attributes
    hunter['str'] = attributes['str']
    hunter['agi'] = attributes['agi']
    hunter['spirit'] = attributes['spirit']
    hunter['int'] = attributes['int']
    hunter['base_mana'] = hunter['int'] * 15

    race_agi_bonuses = {'tauren':0,'dwarf':1,'orc':2,'troll':7,'night elf':8}
    hunter['agi'] = hunter['agi'] - 8 # normalize racial bonuses to prevent double dipping from selector
    hunter['agi'] = hunter['agi'] + race_agi_bonuses[race_wid]

    if raid_buffs2['druid'] == True:
      hunter['str'] = hunter['str'] + 8
      hunter['agi'] = hunter['agi'] + 8

    if raid_buffs1['palahorn'] == True:
      hunter['str'] = hunter['str'] + 6
      hunter['agi'] = hunter['agi'] + 6

    if raid_buffs2['shamstr'] == True:
      hunter['str'] = hunter['str'] + 6

    #if raid_buffs1['shamagi'] == True:
    #  hunter['agi'] = hunter['agi'] + 6

    try:
      talent_points = attributes['spec'].split('hunter/')[1]
    except ValueError:
      print('Use a wowhead classic hunter url.')

    talents = {}
    try:
      talents['bm'] = [int(x) for x in talent_points.split('-')[0]]
    except:
      talents['bm'] = [0]
    try:
      talents['mm'] = [int(x) for x in talent_points.split('-')[1]]
    except:
      talents['mm'] = [0]
    try:
      talents['sv'] = [int(x) for x in talent_points.split('-')[2]]
    except:
      talents['sv'] = [0]

    hunter['spec'] = talents
    hunter['hit'] = attributes['hit']

    try:
      if hunter['spec']['sv'][10] != 0:
          hunter['hit'] += int(hunter['spec']['sv'][10])
    except:
      pass

    # weapon
    hunter['spd'] = weapons['spd']


    if (enchant_wid == True):

      if (twoh_wid == True) | (weapons['spd'][1] == 0):
        hunter['wep'] = ((weapons['dmg'][0][0] + 5, 0), (weapons['dmg'][1][0] + 5, 0))

      else:

        if oh_stone == False:
          hunter['wep'] = ((weapons['dmg'][0][0] + 3, weapons['dmg'][0][1] + 3), (weapons['dmg'][1][0] + 3, weapons['dmg'][1][1] + 3))
        else:
          hunter['wep'] = ((weapons['dmg'][0][0] + 3, weapons['dmg'][0][1] + 11), (weapons['dmg'][1][0] + 3, weapons['dmg'][1][1] + 11))

    else:

      if (twoh_wid == True) | (weapons['spd'][1] == 0):
        hunter['wep'] = weapons['dmg']

      else:

        if oh_stone == False:
          hunter['wep'] = weapons['dmg']
        else:
          hunter['wep'] = ((weapons['dmg'][0][0], weapons['dmg'][0][1] + 8), (weapons['dmg'][1][0], weapons['dmg'][1][1] + 8))

    if agi_elixir == True:
      hunter['agi'] = hunter['agi'] + 25

    if str_elixir == True:
      hunter['str'] = hunter['str'] + 25

    # lion
    lion_buff = 1

    if chest_runes == 'lion':
      lion_buff = 1.21

    elif raid_buffs2['hunterlion'] == True:
      lion_buff = 1.1

    hunter['str'] *= lion_buff
    hunter['int'] *= lion_buff
    hunter['spirit'] *= lion_buff

    agi_lion_buff = 1

    if chest_runes == 'lion':
      try:
        if hunter['spec']['sv'][14] != 0:
          agi_lion_buff += (int(hunter['spec']['sv'][14]) * 0.03) + 0.21
      except:
        pass

    elif raid_buffs2['hunterlion'] == True:
      try:
        if hunter['spec']['sv'][14] != 0:
          agi_lion_buff += (int(hunter['spec']['sv'][14]) * 0.03) + 0.1
      except:
        pass

    else:
      try:
        if hunter['spec']['sv'][14] != 0:
          agi_lion_buff += (int(hunter['spec']['sv'][14]) * 0.03)
      except:
        pass

    hunter['agi'] *= agi_lion_buff

    # dont know new base stats at 40 yet
    hunter['mana'] = ((attributes['int'] - 34) * 15) + 1000

    if mana_pot == True:
      hunter['mana'] = hunter['mana'] + np.random.randint(700,901)

      if hunter['spd'][1] != 0:
        hunter['hit'] = hunter['hit'] + 2

    # melee stats
    hunter['crit'] = (hunter['agi'] - 160 + 0.8 * 200) * 0.052
    hunter['ap'] = (level * 2) + hunter['str'] + hunter['agi'] - 20 + ex_ap

    #if world_buffs['gnomer'] == True:
    #  hunter['spd'] = (hunter['spd'][0] / 1.2, hunter['spd'][1] / 1.2)

    if raid_buffs1['palamight'] == True:
      hunter['ap'] = hunter['ap'] + 85

    if raid_buffs1['warr'] == True:
      hunter['ap'] = hunter['ap'] + 85

    if raid_buffs1['mage'] == True:
      hunter['mana'] = hunter['mana'] + (15 * 15)

    if race_wid == 'orc':
      base_ap =  hunter['str'] +  hunter['agi'] + (level * 2) - 20
      orc_bonus = (base_ap * 0.25) * 15 / duration # ap is in units of dps so we can transform it to get orc bonus ap over the whole fight -- cleans up later calcs
      hunter['ap'] = hunter['ap'] + orc_bonus

    hunter['rap'] = (2 * hunter['agi']) + (level * 2) - 10 + ex_ap + ex_rap + 70

    if raid_buffs2['hunterap'] == True:
      hunter['ap'] = hunter['ap'] + 50
      hunter['rap'] = hunter['rap'] + 50

    if chest_runes == 'master marksman':
      hunter['crit'] += 5

    try:
      if hunter['spec']['sv'][12] != 0:
        hunter['crit'] += int(hunter['spec']['sv'][12])
    except:
      pass

    hunter['crit'] = hunter['crit'] + ex_crit - 2 # crit suppression 1% per level diff

    if raid_buffs3['feralcrit'] == True:
      hunter['crit'] = hunter['crit'] + 3

    return hunter

#@title Pet Setup
def make_pet():
  pet = {'spd': pett_spd,
         'ap': 0.22 * hunter['rap'],
         'type': pett}

  if str_scroll == True:
    pet['ap'] += 26 # pets get 2 ap for 1 str

  if raid_buffs2['druid'] == True:
    pet['ap'] = pet['ap'] + 16

  if raid_buffs1['palahorn'] == True:
    pet['ap'] = pet['ap'] + 12

  if raid_buffs2['shamstr'] == True:
    pet['ap'] = pet['ap'] + 12

  if raid_buffs2['hunterap'] == True:
    pet['ap'] = pet['ap'] + 50

  if raid_buffs1['palamight'] == True:
    pet['ap'] = pet['ap'] + 85

  if raid_buffs1['warr'] == True:
    pet['ap'] = pet['ap'] + 85

  if (chest_runes == 'lion') or (raid_buffs2['hunterlion'] == True):
    pet['ap'] += 20 #lion/kings only increases pet base str

  pet['dmg'] = (pet['ap'] * 0.273 * 1.25, pet['ap'] * 0.327 * 1.25)

  return pet

#@title Auto Attack
def melee(mh):

    if mh == True:

        min_dmg = hunter['ap']/14 * hunter['spd'][0] + hunter['wep'][0][0]
        max_dmg = hunter['ap']/14 * hunter['spd'][0] + hunter['wep'][1][0]

    else:

        oh_dmg_penalty = 0.5

        if boot_runes == 'dual wield spec':
          oh_dmg_penalty = 0.75

        min_dmg = ((hunter['ap']/14 * hunter['spd'][1]) + hunter['wep'][0][1]) * oh_dmg_penalty
        max_dmg = ((hunter['ap']/14 * hunter['spd'][1]) + hunter['wep'][1][1]) * oh_dmg_penalty

    return (min_dmg, max_dmg)

#@title Windfury Attack
def windfury_proc(wf_mod = 1.2):

    min_dmg = (hunter['ap'] * wf_mod)/14 * hunter['spd'][0] + hunter['wep'][0][0]
    max_dmg = (hunter['ap'] * wf_mod)/14 * hunter['spd'][0] + hunter['wep'][1][0]

    return (min_dmg, max_dmg)

#@title Pet Auto Attack
def pet_auto():

    min_dmg = pet['dmg'][0] + (pet['ap'] * pet['spd'] / 14)
    max_dmg = pet['dmg'][1] + (pet['ap'] * pet['spd'] / 14)

    return (min_dmg, max_dmg)

#@title Melee Attack Table
def attack_table(roll, mh, hit = 0, pet = False, spell = ''):

    if pet == True:

      crit = 5

      if raid_buffs3['feralcrit'] == True:
        crit += 3

      try:
        if hunter['spec']['bm'][10] != 0:
          crit += int(hunter['spec']['bm'][10]) * 3
      except:
        pass

    else:
      crit = hunter['crit']

    if spell == 'wc':
      crit_mod = 1.0
    else:
      crit_mod = 2.0

      try:
        if hunter['spec']['sv'][1] != 0:
          crit_mod += int(hunter['spec']['sv'][1]) * 0.01
      except:
        pass

    if (mh_race_wep_wid == True) and (twoh_wid == True):
      miss_upper = np.max(50 - hit * 10,0)
    elif (mh_race_wep_wid == False) and (twoh_wid == True):
      miss_upper = np.max(60 - hit * 10,0)
    elif (mh_race_wep_wid == True) and (mh == True):
      miss_upper = np.max(240 - hit * 10,0)
    elif (mh_race_wep_wid == False) and (mh == True):
      miss_upper = np.max(250 - hit * 10,0)
    elif (oh_race_wep_wid == True) and (mh == False):
      miss_upper = np.max(240 - hit * 10,0)
    elif (oh_race_wep_wid == False) and (mh == False):
      miss_upper = np.max(250 - hit * 10,0)

    miss = (0, miss_upper) # 6% 2h and 25% dw base for +2 levels and no wep skill

    if (mh_race_wep_wid == True) and ((twoh_wid == True) | (mh == True)):
      base = 55 # 5.5% base
    elif (mh_race_wep_wid == False) and ((twoh_wid == True) | (mh == True)):
      base = 60 # 6% base

    if (oh_race_wep_wid == True) and (twoh_wid == False) and (mh == False):
      base = 55 # 5.5% base
    elif (oh_race_wep_wid == False) and (twoh_wid == False) and (mh == False):
      base = 60 # 6% base

    dodge = (miss_upper + 1, miss_upper+(base - 1))

    if (spell != 'rs') & (spell != 'wc') & (spell != 'fs') & (spell != 'carve'):
        glance = (miss_upper+base, miss_upper+base+299) # 30% base at 15% reduced dmg
        crit_lower = miss_upper+base+300
    else:
        glance = (0, 0) # no glance for yellow hits
        crit_lower = miss_upper+base


    if spell == 'rs':

      try:
        if hunter['spec']['sv'][4] != 0:
          crit_range = np.round((crit + (int(hunter['spec']['sv'][4]) * 10))/100 * 1000)
      except:
        crit_range = np.round(crit/100 * 1000)

    else:
      crit_range = np.round(crit/100 * 1000)

    crit = (crit_lower, crit_lower + crit_range)
    hit = (crit_lower + crit_range + 1, 1000)

    if spell == 'wf':
        dmg = windfury_proc()

    elif pet == True:
        dmg = pet_auto()

    elif spell == 'rs':
        if boot_runes == 'dual wield spec':
          mh_dmg = melee(mh=True)
          oh_dmg = melee(mh=False)
          dmg = (mh_dmg[0] + oh_dmg[0] + 80, mh_dmg[1] + oh_dmg[1] + 80)
        else:
          dmg = melee(mh)
          dmg = (dmg[0] + 80, dmg[1] + 80)

    else:
        dmg = melee(mh)

    if (spell != 'wc') and (spell != 'fs') and (spell != 'carve'):
        dmg = dmg[0] + (np.random.random() * (dmg[1] - dmg[0]))

    elif spell == 'fs':

        fs_roll = hunter['wep'][0][0] + (np.random.random() * (hunter['wep'][1][0] - hunter['wep'][0][0]))
        dmg = (hunter['ap']/14 * hunter['spd'][0] + fs_roll) * 0.9

    elif spell == 'carve':

        mh_carve_roll = 0.25 * hunter['wep'][0][0] + (np.random.random() * (hunter['wep'][1][0] - hunter['wep'][0][0]))

        if twoh_wid != True:
          oh_carve_roll = 0.125 * hunter['wep'][0][1] + (np.random.random() * (hunter['wep'][1][1] - hunter['wep'][0][1]))
          dmg = (hunter['ap']/14 * hunter['spd'][0] + mh_carve_roll + oh_carve_roll)

        else:
          dmg = (hunter['ap']/14 * hunter['spd'][0] + mh_carve_roll)

    elif spell == 'wc':
        dmg = 5

    if ((wep_proc_wid1 == 'shadowfang') and (mh == True)):
        dmg = dmg + np.random.randint(4,9)

    if (mh_race_wep_wid == True) and ((twoh_wid == True) | (mh == True)):
      gb_penalty = 0.95
    elif (mh_race_wep_wid == False) and ((twoh_wid == True) | (mh == True)):
      gb_penalty = 0.85 # 30% base at 15% reduced dmg

    if (oh_race_wep_wid == True) and (twoh_wid == False) and (mh == False):
      gb_penalty = 0.95
    elif (oh_race_wep_wid == False) and (twoh_wid == False) and (mh == False):
      gb_penalty = 0.85

    hand = {True: 'mh', False: 'oh'}

    if miss[0] <= roll <= miss[1]: res = (' miss', 0)
    if dodge[0] <= roll <= dodge[1]: res = (' dodge', 0)
    if glance[0] <= roll <= glance[1]: res = (' glance', gb_penalty * dmg)
    if crit[0] <= roll <= crit[1]: res = (' crit', crit_mod * dmg)
    if hit[0] <= roll <= hit[1]: res = (' hit', dmg)

    if spell == 'wf':
        res = (hand[mh] + res[0] + ' wf', res[1])

    elif pet == True:
        res = ('pet' + res[0], res[1])

    elif spell == 'rs':
        if (same_type_wid == True) & (boot_runes == 'dual wield spec'):
          res = ('rs' + res[0], res[1] * 1.3)
        else:
          res = ('rs' + res[0], res[1])

    elif spell == 'wc':
        res = ('wc' + res[0], res[1])

    elif spell == 'fs':
        res = ('fs' + res[0], res[1])

    elif spell == 'carve':
        res = ('carve' + res[0], res[1])

    else:
        res = (hand[mh] + res[0], res[1])

    return res

#@title Sim Auto Attacks
def sim_autos(duration):

  n_mh = int(np.floor(duration / hunter['spd'][0]))

  try:
      n_oh = int(np.floor(duration / hunter['spd'][1]))
  except:
      n_oh = 0

  mh_speed = hunter['spd'][0]

  bonus_haste = 1

  if race_wid == 'troll':
    bonus_haste += 0.1

  if lw_wid == 'haste gloves':
    bonus_haste += 0.1

  if lw_wid == 'haste helm':
    bonus_haste += 0.2

  mh_speed = mh_speed / bonus_haste

  mh_hits = []
  mh_time = 0
  for attack in np.arange(0,n_mh):
      event = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'])
      mh_hits += [(mh_time,) + event]
      mh_time += mh_speed

      if (mh_time >= 10) and (mh_speed != hunter['spd'][0]):
        mh_speed = hunter['spd'][0]

  if twoh_wid == True:
    log = pd.DataFrame(mh_hits)

  else:

      oh_speed = hunter['spd'][1]

      oh_speed = oh_speed / bonus_haste

      oh_hits = []
      oh_time = 0
      for attack in np.arange(0,n_oh):
          event = attack_table(roll = np.random.randint(0,1001), mh = False, hit = hunter['hit'])
          oh_hits += [(oh_time,) + event]
          oh_time += oh_speed

          if (oh_time >= 10) and (oh_speed != hunter['spd'][1]):
            oh_speed = hunter['spd'][1]

      log = pd.DataFrame(mh_hits + oh_hits)

  log.columns = ['time','attack','dmg']
  log = log.sort_values('time').reset_index(drop=True)
  log.time = log.time.round(1)

  return log

#@title Sim Raptor Strike Placements
def sim_raptor_strikes(white, duration):

    mh_hits = white[white.attack.str.contains('mh')]
    mh_hits.time = mh_hits.time.round(1)

    raptor = {'state': 'ready', 'cd': 0}
    raptor_cd = 6
    raptor_strikes = []
    ix = []

    for i,event in mh_hits.iterrows():

        dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'rs')

        if (event.time >= raptor['cd']) & (dmg[1] > 0):

            raptor_strikes += [(event.time,dmg[0],dmg[1])]
            ix += [i]

            raptor['cd'] = event.time + raptor_cd

    raptor_strikes = pd.DataFrame(raptor_strikes, columns = ['time','attack','dmg'], index = ix)

    mh_hits = mh_hits[~mh_hits.index.isin(ix)]

    log = pd.concat([mh_hits, raptor_strikes, white[~white.attack.str.contains('mh')]]).drop_duplicates().sort_values(['time','attack'])

    return log

#@title Sim Flankings Strike Resets
def sim_flankings(raptors):

  raptor_strikes = raptors[raptors.attack.str.contains('rs')].reset_index(drop=True)
  events = []

  for i,row in raptor_strikes.iterrows():

    if i == 0:
      dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'fs')
      events += [(0.0, dmg[0], dmg[1])]

      pet_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
      if ('miss' not in pet_roll[0]) and ('dodge' not in pet_roll[0]):
        if 'crit' in pet_roll[0]:
          pet_crit_fs_mod = 2
        else:
          pet_crit_fs_mod = 1

        pet_dmg = (0.0, 'pet fs ' + pet_roll[0].split(' ')[1].replace('glance','hit'), 0.35 * pet['spd'] * np.random.randint(int(pet_auto()[0]), int(pet_auto()[1])) * pet_crit_fs_mod)
      else:
        pet_dmg = (0.0, 'pet fs miss', 0)

      events += [pet_dmg]

    else:

      fs_reset_roll = np.random.randint(0,1001)
      if fs_reset_roll <= 200:

        dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'fs')
        events += [(row.time + 0.1, 'reset ' + dmg[0], dmg[1])]

        pet_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
        if ('miss' not in pet_roll[0]) and ('dodge' not in pet_roll[0]):
          if 'crit' in pet_roll[0]:
            pet_crit_fs_mod = 2
          else:
            pet_crit_fs_mod = 1

          pet_dmg = (row.time + 0.1, 'pet fs ' + pet_roll[0].split(' ')[1].replace('glance','hit'), 0.35 * pet['spd'] * np.random.randint(int(pet_auto()[0]), int(pet_auto()[1])) * pet_crit_fs_mod)
        else:
          pet_dmg = (row.time + 0.1, 'pet fs miss', 0)

        events += [pet_dmg]

  flanking_strikes = pd.DataFrame(events)
  flanking_strikes.columns = ['time','attack','dmg']

  flankings = pd.concat([raptors, flanking_strikes]).drop_duplicates().sort_values(['time','attack'])

  return flankings

#@title Sim Rotation
def sim_rotation(flankings):

  fs = flankings[flankings.attack.str.contains('fs')]
  fs = fs[~fs.attack.str.contains('pet')]
  fs = fs.time.drop_duplicates().to_list()

  fs_times = []
  fs_cd = []
  fs_ix = 0

  for t in fs:

    if t == 0.0:
      fs_times += [t]
      fs_cd = t + 30

    else:

      if t <= fs_cd:
        fs_times += [t]
        fs_cd = t + 30

      else:

        while t >= fs_cd:

          fs_times += [fs_cd]
          fs_cd = fs_cd + 30

        fs_cd = t

    fs_ix += 1

  fs_times += [fs_cd]

  extra_fs_casts = list(set(fs_times) - set(fs))
  fs_casts = []

  for t in extra_fs_casts:

    dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'fs')
    dmg = (t, dmg[0], dmg[1])
    pet_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
    if ('miss' not in pet_roll[0]) and ('dodge' not in pet_roll[0]):
      if 'crit' in pet_roll[0]:
        pet_crit_fs_mod = 2
      else:
        pet_crit_fs_mod = 1

      pet_dmg = (t, 'pet fs ' + pet_roll[0].split(' ')[1].replace('glance','hit'), 0.35 * pet['spd'] * np.random.randint(int(pet_auto()[0]), int(pet_auto()[1])) * pet_crit_fs_mod)
    else:
      pet_dmg = (t, 'pet fs miss', 0)

    fs_casts += [dmg]
    fs_casts += [pet_dmg]

  fs_casts = pd.DataFrame(fs_casts, index = np.arange(len(fs_casts)), columns = ['time','attack','dmg'])

  fs_casts = pd.concat([flankings, fs_casts]).drop_duplicates().sort_values(['time','attack'])

  fs_times_quantized = [np.ceil(x*2)/2 for x in fs_times]
  fs_times_quantized = fs_times_quantized + list(np.ravel([[x, x - (x % (1.5))] for x in fs_times_quantized if x % (1.5) != 0])) + list(np.ravel([[x, x + (x % (1.5))] for x in fs_times_quantized if x % (1.5) != 0]))

  wc_times = np.arange(0,duration,1.5)

  window = {}
  window['0'] = set(fs_times_quantized)
  window['0.5'] = set([x + 0.5 for x in fs_times_quantized])
  window['-0.5'] = set([x - 0.5 for x in fs_times_quantized])
  window['1'] = set([x + 1 for x in fs_times_quantized])
  window['-1'] = set([x - 1 for x in fs_times_quantized])

  cast_times = list(set(wc_times) - window['0'] - window['0.5'] - window['-0.5'] - window['1'] - window['-1'])

  if hand_runes != 'carve':

    last_immo_cast = 0

    if boot_runes != 'trap launcher':
      immo_cd = 30
    else:
      immo_cd = 15

    events = []
    for t in cast_times:

      if t - last_immo_cast >= immo_cd:
        dmg = prepull()
        dmg = dmg[dmg.attack == 'immo trap']
        events += [(t, dmg['attack'].iloc[0], dmg['dmg'].iloc[0])]

        last_immo_cast = t

      else:
        dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'wc')
        events += [(t, dmg[0], dmg[1])]

    casts = pd.DataFrame(events, index = np.arange(len(cast_times)), columns = ['time','attack','dmg'])

  else:

    events = []
    carve_prio = 1
    last_immo_cast = 0

    if boot_runes != 'trap launcher':
      immo_cd = 30
    else:
      immo_cd = 15

    for t in cast_times:

      if carve_prio == 5: carve_prio = 1

      if carve_prio == 1:

        dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'carve')
        events += [(t, dmg[0], dmg[1] * 0.5)]

      else:

        if t - last_immo_cast >= immo_cd:
          dmg = prepull()
          dmg = dmg[dmg.attack == 'immo trap']
          events += [(t, dmg['attack'].iloc[0], dmg['dmg'].iloc[0])]

          last_immo_cast = t

        else:
          dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'wc')
          events += [(t, dmg[0], dmg[1] * 0.5)]

      carve_prio += 1


    casts = pd.DataFrame(events, index = np.arange(len(cast_times)), columns = ['time','attack','dmg'])

  yellow = pd.concat([fs_casts, casts]).drop_duplicates().sort_values(['time','attack'])

  return yellow

#@title Sim Flanking Strike Buff
def sim_flanking_buff(yellow):

  flankings = yellow[(yellow.attack.str.contains('fs')) & (~yellow.attack.str.contains('miss')) & (~yellow.attack.str.contains('dodge') & (~yellow.attack.str.contains('pet')))].sort_values('time').time.to_list()

  raptor_strikes = yellow[yellow.attack.str.contains('rs')]

  if len(flankings) > 0:

      for i in np.arange(0, len(flankings)):

          raptor_strikes['buff_end'] = flankings[i] + 10

          raptor_strikes['buff_remaining'] = raptor_strikes['buff_end'] - raptor_strikes['time']

          raptor_strikes[f'fs_buff_active{i}'] = [1 if 0 < x <= 10 else 0 for x in raptor_strikes['buff_remaining']]

      raptor_strikes['fs_buff_stacks'] = raptor_strikes[[f'fs_buff_active{i}' for i in np.arange(0, len(flankings))]].sum(axis=1)
      raptor_strikes['dmg'] = [x * (1 + (y * 0.1)) if y >= 1 else x for x,y in zip(raptor_strikes['dmg'], raptor_strikes['fs_buff_stacks'])]
      raptor_strikes = raptor_strikes.drop(['buff_end','buff_remaining','fs_buff_stacks'] + [f'fs_buff_active{i}' for i in np.arange(0, len(flankings))], axis = 1)

  log = pd.concat([yellow[~yellow.attack.str.contains('rs')], raptor_strikes]).drop_duplicates().sort_values(['time','attack'])

  return log

#@title Sim Priority Rotation
def sim_priority_rotation(duration):

  globals = np.floor(duration / 1.5)

  # define cds
  cooldown = {}
  cooldown['fs'] = 30 / 1.5
  cooldown['rs'] = 3 / 1.5
  cooldown['trap'] = 30 / 1.5

  if boot_runes == 'trap launcher':
    cooldown['trap'] = 15 / 1.5

  # define starting states
  flanking = {'state': 'ready', 'cd': 0}
  flanking_buff = {'state': 'down','cd':0,'duration': 10,'stacks':0}
  raptor = {'state': 'ready', 'cd': 0}
  trap = {'state': 'down', 'cd': 15 / 1.5}

  if hand_runes == 'carve':
    cooldown['carve'] = 6 / 1.5
    carve = {'state': 'ready', 'cd': 0}

  events = []

  for gcd in np.arange(0, globals):

    # check states
    if flanking_buff['cd'] <= gcd: flanking_buff['state'] = 'down'
    if flanking['cd'] <= gcd: flanking['state'] = 'ready'
    if raptor['cd'] <= gcd: raptor['state'] = 'ready'
    if trap['cd'] <= gcd: trap['state'] = 'ready'

    if hand_runes == 'carve':
      if carve['cd'] <= gcd: carve['state'] = 'ready'

    # define spell behavior and rotation priority

    # flanking strike
    if flanking['state'] == 'ready':

      dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'fs')
      events += [(gcd * 1.5, dmg[0], dmg[1])]

      pet_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
      if ('miss' not in pet_roll[0]) and ('dodge' not in pet_roll[0]):
        if 'crit' in pet_roll[0]:
          pet_crit_fs_mod = 2
        else:
          pet_crit_fs_mod = 1

        pet_dmg = (gcd*1.5, 'pet fs ' + pet_roll[0].split(' ')[1].replace('glance','hit'), 0.35 * pet['spd'] * np.random.randint(int(pet_auto()[0]), int(pet_auto()[1])) * pet_crit_fs_mod)
      else:
        pet_dmg = (gcd*1.5, 'pet fs miss', 0)

      events += [pet_dmg]

      flanking['state'] = 'down'
      flanking['cd'] = gcd + cooldown['fs']

      if flanking_buff['state'] == 'down':
        flanking_buff['state'] = 'active'
        flanking_buff['stacks'] = 1
        flanking_buff['cd'] = gcd + flanking_buff['duration']
      else:
        flanking_buff['stacks'] += 1
        flanking_buff['stacks'] = np.min([flanking_buff['stacks'], 3])
        flanking_buff['cd'] = gcd + flanking_buff['duration']
      continue

    # trap
    if (trap['state'] == 'ready') and (globals - gcd >= (15/1.5)):

      dmg = prepull()
      dmg = dmg[dmg.attack == 'immo trap']
      events += [(gcd*1.5, dmg['attack'].iloc[0], dmg['dmg'].iloc[0])]

      trap['state'] = 'down'
      trap['cd'] = gcd + cooldown['trap']
      continue

    # raptor
    if raptor['state'] == 'ready':

      dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'rs')
      buffed_dmg = dmg[1] * (1 + (flanking_buff['stacks'] * 0.1))
      events += [(gcd * 1.5, dmg[0], buffed_dmg)]

      rs_reset_roll = np.random.randint(0,1001)
      fs_reset_roll = np.random.randint(0,1001)

      if rs_reset_roll <= 300:
        raptor['state'] = 'ready'
      else:
        raptor['state'] = 'down'
        raptor['cd'] = gcd + cooldown['rs']

      if fs_reset_roll <= 200:
        flanking['state'] = 'ready'
      continue

    # carve
    if hand_runes == 'carve':
      if carve['state'] == 'ready':

        dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'carve')
        events += [(gcd * 1.5, dmg[0], dmg[1])]

        carve['state'] = 'down'
        carve['cd'] = gcd + cooldown['carve']
        continue

    # wingclip
    dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'wc')
    events += [(gcd * 1.5, dmg[0], dmg[1])]

  log = pd.DataFrame(events)
  log.columns = ['time','attack','dmg']

  return log

#@title Sim Windfury Procs
def sim_windfury(combat_log):

    valid_hits = combat_log[(combat_log.attack.str.contains('fs')) |
                            (combat_log.attack.str.contains('wc')) |
                            (combat_log.attack.str.contains('mh')) |
                            (combat_log.attack.str.contains('carve')) |
                            (combat_log.attack.str.contains('rs'))]

    valid_hits = valid_hits[~valid_hits.attack.str.contains('pet')]

    windfury = {'state': 'ready', 'cd': 0}
    windfury_cd = 1
    wf_procs = []

    for i,event in valid_hits.iterrows():

        if windfury['cd'] <= event.time: windfury['state'] = 'ready'

        roll = np.random.randint(0,1001)

        if (roll <= 200) & (windfury['state'] == 'ready') & (event.dmg > 0):
            dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'wf')
            wf_procs += [(event.time, dmg[0], dmg[1])]
            windfury['state'] = 'down'
            windfury['cd'] = event.time + windfury_cd
        else:
            if windfury['cd'] <= event.time:
                windfury['state'] = 'ready'
                windfury['cd'] = 0

    wf_procs = pd.DataFrame(wf_procs, index = np.arange(0,len(wf_procs)), columns = ['time','attack','dmg'])

    return wf_procs

#@title Sim Weapon Procs
def sim_weapon_procs(combat_log, mh, proc):

    if (mh == True) | (twoh_wid == True):
        valid_hits = combat_log[(combat_log.attack.str.contains('fs')) | (combat_log.attack.str.contains('wc')) | (combat_log.attack.str.contains('mh') | (combat_log.attack.str.contains('carve')))]
    else:
        valid_hits = combat_log[combat_log.attack.str.contains('oh')]

    valid_hits = valid_hits[~valid_hits.attack.str.contains('pet')]

    procs = {'shadowfang': {'state': 'ready', 'cd': 0, 'dmg': 30, 'rate': 5.5, 'icd':0},
             'gust': {'state': 'ready', 'cd': 0, 'dmg': 15, 'rate': 7.5, 'icd': 0},
             'talwar': {'state': 'ready', 'cd': 0, 'dmg': 30, 'rate': 15, 'icd': 0},
             'meteor': {'state': 'ready', 'cd': 0, 'dmg': 37.5, 'rate': 3, 'icd': 0},
             'hydra': {'state': 'ready', 'cd': 0, 'dmg': 120, 'rate': 3.5, 'icd': 0},
             'fathom': {'state': 'ready', 'cd': 0, 'dmg': ((50 * (1-hunter['crit']/100)) + (100 * (hunter['crit']/100))) , 'rate': 8.4, 'icd': 0},
             'bloodpike': {'state': 'ready', 'cd': 0, 'dmg': 100, 'rate': 3, 'icd': 0},
             'duskbringer': {'state': 'ready', 'cd': 0, 'dmg': 95, 'rate': 6.5, 'icd': 0},
             'grimclaw': {'state': 'ready', 'cd': 0, 'dmg': 25, 'rate': 2, 'icd': 0},
             'bootknife': {'state': 'ready', 'cd': 0, 'dmg': 11, 'rate': 12.5, 'icd': 0},
             "serra'kis": {'state': 'ready', 'cd': 0, 'dmg': 40, 'rate': 6, 'icd': 0}
    }[proc]

    wep_procs = []

    for i,event in valid_hits.iterrows():

        if procs['cd'] <= event.time: procs['state'] = 'ready'

        roll = np.random.randint(0,1001)

        if (roll <= (procs['rate'] * 10)) & (procs['state'] == 'ready') & (event.dmg > 0):

            if proc == 'bloodpike':
              dmg = np.clip((duration - event.time) / 30, 0, 1) * procs['dmg']
            elif proc == 'hydra':
              dmg = np.clip((duration - event.time) / 15, 0, 1) * procs['dmg']
            elif proc == "serra'kis":
              dmg = np.clip((duration - event.time) / 20, 0, 1) * procs['dmg']
            else:
              dmg = procs['dmg']

            wep_procs += [(event.time, event.attack + f' {proc}', dmg)]
            procs['state'] = 'down'
            procs['cd'] = event.time + procs['icd']
        else:
            if procs['cd'] <= event.time:
                procs['state'] = 'ready'
                procs['cd'] = 0

    wep_procs = pd.DataFrame(wep_procs, index = np.arange(0,len(wep_procs)), columns = ['time','attack','dmg'])


    return wep_procs

#@title Sim Red Whelp Gloves
def sim_whelp_gloves(combat_log):

    valid_hits = combat_log[(~combat_log.attack.str.contains('pet')) & (combat_log.dmg != 0)]
    rwg_procs = []

    for i,event in valid_hits.iterrows():

        roll = np.random.randint(0,1001)

        if roll <= 50:

            rwg_procs += [(event.time, event.attack + f' rwg', 20)]

    rwg_procs = pd.DataFrame(rwg_procs, index = np.arange(0,len(rwg_procs)), columns = ['time','attack','dmg'])

    return rwg_procs

#@title Sim Mana Usage
def sim_mana(combat_log):

    fs_cost = combat_log[(combat_log.attack.str.contains('fs')) & (~combat_log.attack.str.contains('pet'))].attack.drop_duplicates().to_list()
    fs_cost = [{'attack': x, 'cost': 9} for x in fs_cost]

    wc_cost = combat_log[combat_log.attack.str.contains('wc')].attack.drop_duplicates().to_list()
    wc_cost = [{'attack': x, 'cost': 40} for x in wc_cost]

    rs_cost = combat_log[combat_log.attack.str.contains('rs')].attack.drop_duplicates().to_list()
    rs_cost = [{'attack': x, 'cost': 45} for x in rs_cost]

    cv_cost = combat_log[combat_log.attack.str.contains('carve')].attack.drop_duplicates().to_list()
    cv_cost = [{'attack': x, 'cost': 24} for x in cv_cost]

    mana_cost = fs_cost + wc_cost + rs_cost + cv_cost

    mana_cost = pd.DataFrame(mana_cost, index = np.arange(len(mana_cost)))

    combat_log = pd.concat([prepull(), combat_log.merge(mana_cost, how = 'left')]).drop_duplicates().fillna(0.0)
    combat_log_mana_cost = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    return combat_log_mana_cost

#@title Sim Frenzy
def sim_frenzy(pet_log):

    crits = pet_log[pet_log.attack.str.contains('crit')]

    frenzy_crits = []

    for i,row in crits.iterrows():

      roll = np.random.randint(0,1000)

      if roll <= hunter['spec']['bm'][14] * 200:
        frenzy_crits += [row]

    frenzy_uptime = pd.DataFrame(frenzy_crits).time.diff().fillna(0).clip(0,8).sum()

    n_extra_swings = int(np.ceil(frenzy_uptime / pet['spd'] * 0.3))

    extra_swings = pet_log[~(pet_log.attack.str.contains('claw') | pet_log.attack.str.contains('bite') | pet_log.attack.str.contains('cast'))]
    extra_swings = extra_swings[(extra_swings.time <= 120) & (extra_swings.time >= 18)].sample(n_extra_swings)

    assert len(extra_swings) == n_extra_swings

    extra_swings.attack = ['pet frenzy ' + x.split(' ')[1] for x in extra_swings.attack]

    extra_swings.time = duration + 0.1

    extra_swings = extra_swings[extra_swings.dmg > 0]

    return extra_swings

#@title Sim Pet Damage
def sim_pet(duration):

    pet_info = {'ws': {'dmg': (51,59), 'cost': 50, 'mod': 1.07},
                'cat': {'dmg': {'claw':(26,36),'bite':(49,59)}, 'cost': {'claw':25,'bite':35}, 'mod': 1.1},
                'monke': {'dmg': {'stomp':(87,99),'bite':(49,59)}, 'cost': {'stomp':60,'bite':35}, 'mod': 1.02}
               }[pet['type']]

    spec_mod = 1.0

    if hand_runes == 'beast master':
      bm_rune_mod = 1.2
    else:
      bm_rune_mod = 1.0

    try:
      if hunter['spec']['bm'][8] != 0:
        spec_mod += int(hunter['spec']['bm'][8]) * 0.04
    except:
      pass

    # using old blizzard formulas result in pet autos that are ~2x too big from looking thru logs
    # check sources for pet auto formulas to check for yourself
    blizard_petauto_mod = 0.45

    n_hits = int(np.floor(duration / pet['spd']))
    pet_hits = []
    pet_time = 0
    for attack in np.arange(0,n_hits):
        dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
        mod_dmg = dmg[1] * pet_info['mod'] * spec_mod * bm_rune_mod * blizard_petauto_mod
        pet_hits += [(pet_time, dmg[0], mod_dmg)]
        pet_time += pet['spd']

    pet_hits = pd.DataFrame(pet_hits, index = np.arange(0,len(pet_hits)), columns = ['time','attack','dmg'])

    focus_rate = 5 # per second

    if hand_runes == 'beast master':
      bm_rune_focus_mod = 0.5
    else:
      bm_rune_focus_mod = 0

    try:
      if hunter['spec']['bm'][13] != 0:
        bm_talent_focus_mod += int(hunter['spec']['bm'][13]) * 0.1
      else:
        bm_talent_focus_mod = 0
    except:
      bm_talent_focus_mod = 0

    focus_rate *= (1 + bm_rune_focus_mod + bm_talent_focus_mod)

    if pet['type'] == 'ws':
        opening_gcd = np.floor(100 / pet_info['cost'])
        total_focus = 100 + (duration - (opening_gcd * 1.5)) * focus_rate
        max_casts = np.floor(total_focus / pet_info['cost'])

        ws_sp_scaling = pet['ap'] * 0.425

        def ws_dmg():

          cast_dmg = (np.random.randint(pet_info['dmg'][0],pet_info['dmg'][1] + 1) + ws_sp_scaling) * pet_info['mod'] * spec_mod * bm_rune_mod

          crit_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
          if 'crit' in crit_roll[0]:
            cast_dmg *= 2
            msg = 'pet cast crit'
            return (cast_dmg, msg)

          elif (('miss' not in crit_roll[0]) & ('dodge' not in crit_roll[0])):
            msg = 'pet cast hit'
            return (cast_dmg, msg)
          else:
            msg = 'pet cast miss'
            return (0, msg)

        ix = np.arange(0, max_casts)

        all_casts = [ws_dmg() for x in ix]
        all_msg = [x[1] for x in all_casts]
        all_casts = [x[0] for x in all_casts]

        pet_casts = pd.DataFrame(zip(ix, all_msg, all_casts), index = ix, columns = ['time','attack','dmg'])
        pet_casts['time'] = [(1.5 * x) if x < opening_gcd else ((x - 1) * 1.5) + 10 for x in ix]

        for i,row in pet_casts.iterrows():
            if i < opening_gcd:
                continue
            else:
                pet_casts['time'][i] = pet_casts['time'][i - 1] + (pet_info['cost']/9)
        pet_casts.time = pet_casts.time.round(1)

    elif pet['type'] == 'cat':
        bite_cd = 10
        total_focus = pet_info['cost']['bite'] + duration * focus_rate
        max_bites = np.floor(duration / 10)
        total_focus = total_focus - (max_bites * pet_info['cost']['bite'])
        max_claws = np.floor(total_focus / pet_info['cost']['claw'])

        cat_ap_scaling = {}
        cat_ap_scaling['bite'] = pet['ap'] * 0.3
        cat_ap_scaling['claw'] = pet['ap'] * 0.2

        def cat_dmg(spell):

          cast_dmg = (np.random.randint(pet_info['dmg'][spell][0],pet_info['dmg'][spell][1] + 1) + cat_ap_scaling[spell]) * pet_info['mod'] * spec_mod * bm_rune_mod

          crit_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
          if 'crit' in crit_roll[0]:
            cast_dmg *= 2
            msg = f'pet {spell} crit'
            return (cast_dmg, msg)

          elif (('miss' not in crit_roll[0]) & ('dodge' not in crit_roll[0])):
            msg = f'pet {spell} hit'
            return (cast_dmg, msg)
          else:
            msg = f'pet {spell} miss'
            return (0, msg)

        bite_ix = np.arange(0, max_bites)
        all_bites = [cat_dmg('bite') for x in bite_ix]
        all_bite_msg = [x[1] for x in all_bites]
        all_bites = [x[0] for x in all_bites]

        pet_bites = pd.DataFrame(zip(bite_ix,all_bite_msg,all_bites), index = bite_ix, columns = ['time','attack','dmg'])
        pet_bites['time'] = [x*10 for x in bite_ix]

        claw_ix = np.arange(0, max_claws)
        all_claws = [cat_dmg('claw') for x in claw_ix]
        all_claw_msg = [x[1] for x in all_claws]
        all_claws = [x[0] for x in all_claws]

        pet_claws = pd.DataFrame(zip(claw_ix,all_claw_msg,all_claws), index = claw_ix, columns = ['time','attack','dmg'])
        pet_claws['time'] = np.linspace(1.5, int(duration) - 1.5, int(max_claws)).round(1)

        pet_casts = pd.concat([pet_bites, pet_claws])

    elif pet['type'] == 'monke':

        bite_cd = 10
        stomp_cd = 60

        total_focus = pet_info['cost']['bite'] + duration * focus_rate
        max_bites = np.floor(duration / bite_cd)

        total_focus = total_focus - (max_bites * pet_info['cost']['bite'])

        max_stomps = np.floor(total_focus / pet_info['cost']['stomp'])
        max_stomps_cd = 1 + np.floor(duration / stomp_cd)
        max_stomps = np.min([max_stomps, max_stomps_cd])

        monke_ap_scaling = {}
        monke_ap_scaling['bite'] = pet['ap'] * 0.3
        monke_ap_scaling['stomp'] = pet['ap'] * 0.5

        def monke_dmg(spell):

          cast_dmg = (np.random.randint(pet_info['dmg'][spell][0],pet_info['dmg'][spell][1] + 1) + monke_ap_scaling[spell]) * pet_info['mod'] * spec_mod * bm_rune_mod

          crit_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
          if 'crit' in crit_roll[0]:
            cast_dmg *= 2
            msg = f'pet {spell} crit'
            return (cast_dmg, msg)

          elif (('miss' not in crit_roll[0]) & ('dodge' not in crit_roll[0])):
            msg = f'pet {spell} hit'
            return (cast_dmg, msg)
          else:
            msg = f'pet {spell} miss'
            return (0, msg)

        bite_ix = np.arange(0, max_bites)
        all_bites = [monke_dmg('bite') for x in bite_ix]
        all_bite_msg = [x[1] for x in all_bites]
        all_bites = [x[0] for x in all_bites]

        pet_bites = pd.DataFrame(zip(bite_ix,all_bite_msg,all_bites), index = bite_ix, columns = ['time','attack','dmg'])
        pet_bites['time'] = [x*10 for x in bite_ix]

        stomp_ix = np.arange(0, max_stomps)
        all_stomps = [monke_dmg('stomp') for x in stomp_ix]
        all_stomp_msg = [x[1] for x in all_stomps]
        all_stomps = [x[0] for x in all_stomps]

        pet_stomps = pd.DataFrame(zip(stomp_ix,all_stomp_msg,all_stomps), index = stomp_ix, columns = ['time','attack','dmg'])
        pet_stomps['time'] = np.linspace(1.5, int(duration) - 1.5, int(max_stomps)).round(1)

        pet_casts = pd.concat([pet_bites, pet_stomps])

    if race_wid == 'orc':
      pet_casts.dmg = pet_casts.dmg * 1.05
      pet_hits.dmg = pet_hits.dmg * 1.05

    try:
      if hunter['spec']['bm'][15] != 0:

        n_bestial_wrath = 1 + np.floor(duration / 120)
        bestial_wrath_activations = [x * 120 for x in np.arange(n_bestial_wrath)]

        for t in bestial_wrath_activations:
          pet_casts.dmg = [y * 1.5 if t <= x <= t + 18 else y for x,y in zip(pet_casts.time, pet_casts.dmg)]
          pet_hits.dmg = [y * 1.5 if t <= x <= t + 18 else y for x,y in zip(pet_hits.time, pet_hits.dmg)]
          hunter['mana'] = hunter['mana'] - (hunter['base_mana'] * 0.12)

    except:
      pass

    pet_log = pd.concat([pet_hits, pet_casts]).sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    try:
      if hunter['spec']['bm'][14] != 0:
        extra_swings = sim_frenzy(pet_log)
        pet_log = pd.concat([pet_log, extra_swings]).sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    except:
      pass

    return pet_log

#@title Sim Prepull
def prepull():

  immo_dmg = 340
  try:
    if hunter['spec']['sv'][6] != 0:
      immo_dmg = immo_dmg * (1 + (hunter['spec']['sv'][6] * 0.15))
  except:
    pass

  if engi_wid != None:

    n_engi = 1 + np.floor(duration / 60)
    engi_casts = [x * 60 for x in np.arange(n_engi)]

    casts = []

    for t in engi_casts:

      if t == 0:
        t = -4.0

      engi_explo = np.random.randint(275,375)
      msg = 'high-yield radiation bomb'

      explo_crit_roll = np.random.randint(0,1001)
      if explo_crit_roll <= 50:
        engi_explo = ((engi_explo - 125) * 2) + 125
        msg = 'high-yield radiation bomb crit'

      casts += [{'time':t,'attack':msg,'dmg':engi_explo,'cost':0}]

    casts += [{'time':-1.0,'attack':'immo trap','dmg':immo_dmg,'cost':135}]
    casts += [{'time':-2.0,'attack':'serpent sting','dmg':105,'cost':50}]
    casts += [{'time':-3.5,'attack':'multi-shot','dmg':160,'cost':100}]

    log = pd.DataFrame(casts, index = np.arange(len(casts)))

  else:
    log = pd.DataFrame([{'time':-1.0,'attack':'immo trap','dmg':immo_dmg,'cost':135},
                        {'time':-2.0,'attack':'serpent sting','dmg':105,'cost':50},
                        {'time':-3.5,'attack':'multi-shot','dmg':160,'cost':100}], index = [0,1,2])

  return log

#@title Sim Encounter
def sim_fight(duration, coh):

    white = sim_autos(duration)

    if belt_runes != 'melee spec':
      raptors = sim_raptor_strikes(white, duration)
      flankings = sim_flankings(raptors)
      yellow = sim_rotation(flankings)
      combat_log = sim_flanking_buff(yellow)

    else:
      combat_log = pd.concat([white, sim_priority_rotation(duration)])

    combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)
    combat_log = sim_mana(combat_log)

    if raid_buffs3['feralwf'] == True:
        wf_procs = sim_windfury(combat_log)

        if len(wf_procs) > 0:
            combat_log = pd.concat([wf_procs, combat_log]).fillna(0.0)
            combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    if coh != None: # coh is chance on hit

        if twoh_wid == True:
            wep_procs = sim_weapon_procs(combat_log, proc = wep_proc_wid1, mh = True)

        if twoh_wid == False:

            if coh[0] != 'None':
                mh_wep_procs = sim_weapon_procs(combat_log, proc = coh[0], mh = True)
            else:
                mh_wep_procs = []

            if coh[1] != 'None':
                oh_wep_procs = sim_weapon_procs(combat_log, proc = coh[1], mh = False)
            else:
                oh_wep_procs = []

            if (len(mh_wep_procs) > 0) & (len(oh_wep_procs) > 0):
                wep_procs = pd.concat([mh_wep_procs, oh_wep_procs])
            elif (len(mh_wep_procs) > 0) & (len(oh_wep_procs) == 0):
                wep_procs = mh_wep_procs
            elif (len(mh_wep_procs) == 0) & (len(oh_wep_procs) > 0):
                wep_procs = oh_wep_procs
            else:
                wep_procs = []

        if len(wep_procs) > 0:
            combat_log = pd.concat([wep_procs, combat_log]).fillna(0.0)
            combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    if lw_wid == 'red whelp gloves':
      rwg_procs = sim_whelp_gloves(combat_log)
      if len(rwg_procs) > 0:
        combat_log = pd.concat([rwg_procs, combat_log]).fillna(0.0)
        combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    dmg_mods = 1.0

    if world_buffs['dmf'] == True:
        dmg_mods += 0.1

    if chest_runes != 'lone wolf':
      combat_log.dmg = combat_log.dmg*dmg_mods

    pet_log = sim_pet(duration)

    if (len(pet_log) > 0) and (chest_runes != 'lone wolf'):

        combat_log = pd.concat([pet_log, combat_log]).fillna(0.0)
        combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    elif chest_runes == 'lone wolf':
      combat_log.dmg = combat_log.dmg*(dmg_mods+0.3)
      combat_log = combat_log[~combat_log.attack.str.contains('pet')]
    else:
      pass

    combat_log['total_dmg'] = combat_log.dmg.cumsum()
    combat_log['total_mana'] = hunter['mana'] -  combat_log.cost.cumsum()

    p1 = combat_log[combat_log.total_mana >= 0]
    p2 = combat_log[ (combat_log.total_mana < 0) & ((combat_log.attack.str.contains('mh ') | (combat_log.attack.str.contains('oh ')) | (combat_log.attack.str.contains('pet '))))]
    p2.total_mana = 0

    combat_log = pd.concat([p1, p2])

    dmg_done = combat_log[combat_log.dmg > 0][['attack', 'dmg']].groupby('attack').sum().astype(int).sort_values('dmg',ascending = False).reset_index()
    casts = combat_log[['attack']].value_counts().reset_index()
    avg_hit = combat_log[['attack', 'dmg']].groupby('attack').mean().astype(int).reset_index().rename(columns = {'dmg':'avg_hit'})
    min_hit = combat_log[['attack', 'dmg']].groupby('attack').min().astype(int).reset_index().rename(columns = {'dmg':'min_hit'})
    max_hit = combat_log[['attack', 'dmg']].groupby('attack').max().astype(int).reset_index().rename(columns = {'dmg':'max_hit'})

    dmg_done = dmg_done.merge(casts).merge(avg_hit).merge(min_hit).merge(max_hit)

    dmg_done.columns = ['attack','dmg','count','avg_hit','min_hit','max_hit']

    return combat_log, dmg_done

#@title Report Results

def report(trials):

  results = pd.concat([x[1] for x in trials]).drop(['avg_hit'],axis = 1)
  results_sum = results[['attack','dmg','count']].groupby('attack').sum()
  results_min = results[['attack','min_hit']].groupby('attack').min()
  results_max = results[['attack','max_hit']].groupby('attack').max()

  results = results_sum.join(results_min).join(results_max)
  results['avg_hit'] = (results['dmg'] / results['count']).astype(int)
  results['expected_casts'] = (results['count'] / iter).round(2)
  results['expected_dmg'] = (results['dmg'] / iter).astype(int)

  results = results.reset_index()

  dps = [(x[1].dmg.sum()/duration).round(1) for x in trials]

  pet_dmg = int((results[results.attack.str.contains('pet')].dmg.sum() / results.dmg.sum()).round(2) * 100)

  results = results.drop(['count','dmg'],axis = 1).sort_values('expected_dmg',ascending=False)

  print('\n')
  print(('avg', np.mean(dps).round(1),'max', np.max(dps), 'std', np.std(dps).round(1)))
  print(f'\nhunter: {100 - pet_dmg}%\npet: {pet_dmg}%')
  print('\n')

  import matplotlib.pyplot as plt
  fig = plt.figure(figsize=(4,2))
  ax = fig.add_subplot(111)
  ax.hist(dps)
  plt.ylabel('trials')
  plt.xlabel('dps')
  plt.show()

  print('\n\n\nsummary over all iterations:')
  display(results.reset_index(drop=True))

  print('\n\n\nrandom iteration:')
  random_trial = trials[0][1]
  random_trial['dps'] = (random_trial['dmg'] / duration).round(1)
  random_trial = random_trial[['attack','min_hit','avg_hit','max_hit','count','dmg']]
  display(random_trial)

  print('\n\n\nrandom combat log:')
  random_log = trials[0][0]
  random_log.dmg = random_log.dmg.round(1)
  random_log.total_dmg = random_log.total_dmg.round(1)
  display(random_log)

  return None

#@title Sim Orchestration

def run_sim():

  global duration
  duration = duration_wid
  iterations = iter

  if twoh_wid == False:
    weapons = {'dmg': ((mh_range[0],oh_range[0]),(mh_range[1],oh_range[1])),
               'spd': (wep_spd1,wep_spd2)}

  else:
    weapons = {'dmg': ((mh_range[0],0),(mh_range[1],0)),
               'spd': (wep_spd1,0)}

  attributes = {'str': strength,
                'agi': agi,
                'int': intel,
                'spirit': spirit,
                'hit': ex_hit,
                'spec':spec}

  hunter = make_hunter(weapons, attributes)
  globals()['hunter'] = hunter

  pet = make_pet()
  globals()['pet'] = pet

  if (wep_proc_wid1 == 'None') and (wep_proc_wid2 == 'None'):
    coh = None
  elif (twoh_wid == False):
    coh = [wep_proc_wid1, wep_proc_wid2]
  elif (twoh_wid == True):
    coh = [wep_proc_wid1, None]

  return sim_fight(duration, coh = coh)


########################################################
      #### Above code from flori's notebook ####
########################################################


def app_report(trials):

  results = pd.concat([x[1] for x in trials]).drop(['avg_hit'],axis = 1)
  results_sum = results[['attack','dmg','count']].groupby('attack').sum()
  results_min = results[['attack','min_hit']].groupby('attack').min()
  results_max = results[['attack','max_hit']].groupby('attack').max()

  results = results_sum.join(results_min).join(results_max)
  results['avg_hit'] = (results['dmg'] / results['count']).astype(int)
  results['expected_casts'] = (results['count'] / iter).round(2)
  results['expected_dmg'] = (results['dmg'] / iter).astype(int)

  results = results.reset_index()

  dps = [(x[1].dmg.sum()/duration).round(1) for x in trials]

  pet_dmg = int((results[results.attack.str.contains('pet')].dmg.sum() / results.dmg.sum()).round(2) * 100)

  results = results.drop(['count','dmg'],axis = 1).sort_values('expected_dmg',ascending=False)

  st.sidebar.header('Simulation results:')
  st.sidebar.write('Average dps', np.mean(dps).round(1))
  st.sidebar.write('Max dps', np.max(dps))
  st.sidebar.write('dps std', np.std(dps).round(1))

  # Append mean DPS to prev_sims
  if dps:  # Check if dps is not empty
      st.session_state.prev_sims.append(np.mean(dps).round(1))


  st.sidebar.write(f'\nPercent hunter damage: {100 - pet_dmg}%')
  st.sidebar.write(f'\nPercent pet damage: {pet_dmg}%')

  fig = plt.figure(figsize=(5,2))
  ax = fig.add_subplot(111)
  ax.hist(dps)
  plt.title('Simulations')
  plt.ylabel('trials')
  plt.xlabel('dps')

  st.sidebar.pyplot(fig)
  
  st.sidebar.write(results)

  return None


# Initial page config

st.set_page_config(
     page_title='WoW SOD Melee Hunter Simulator',
     layout="wide",
     initial_sidebar_state="expanded",
)


### App UI ###
# Header
st.title("WoW SOD Melee Hunter Simulator")

st.write('app builder: discord: zzenn777 | sim builder: discord: bloodflori')
st.write('Please report any bugs to discord: @zzenn777')

# Add Text Section for User Instructions
st.header("Instructions:", divider=True)
st.markdown("""
# Latest Version: Feb 1 2024
- sim updated to P2
- added monke

## How to Use This Sim:
- Go to the top left File menu and make a copy of this notebook in drive
- If you copy multiple notebooks you can have multiple sims for comparisons
- Go to the top right and attach a runtime
- Go to the top left Runtime menu and select 'Run all' to load the notebook
- Enter your stats:
  - Weapon stats come from the item tooltip NOT the character panel
  - To sim 2h, set all the offhand options to 0 and/or select 'Twohand' (both work)
  - Character and pet stats come from the character panel
  - TURN OFF HAWK AND LION WHEN ENTERING STATS
  - Extra stats come from item tooltips (i.e. hit/ap on crafting items, weps, trinkets, tier bonuses)
- Set encounter info:
  - Select runes
  - Enter talents using wowhead sod calc url. Default is deep sv
  - Duration is encounter length in seconds
  - Iterations is number of simulations to run (use 3k+ for settings similar to wowsims)
- Set additional options:
  - Weapon enchants (wep dmg)
  - Consumes (mana potion, minor recombobulator, offhand stone, elixirs, pet scrolls)
  - Catfury
  - Raid buffs (shout, might,  mark, int)
  - World buffs (dmf, bfd, ashen)
- You do not need to reload the options this will actually reset them
- You do want to reload the sim by hitting the play button in the last cell to clear any old results and load new options
- Run sim by hitting 'Melee Dream'

### Things This Sim Is Good At:
- Comparing gear options
- Comparing talent options
- Comparing rune options
- Comparing dps without optimal setups (wep enchants, buffs, wf)

### Things This Sim Is Not Good At:
- Getting 100 percent accurate raid dps numbers (sims are for comps and i am not implementing boss armor/resist)
- Very long fight lengths (>120s, on longer fights fishing and mana regen are more important -- all fights in bfd are under 2 min)

### Things I Won't Implement:
- Save Features

### Things I'm Working On (In No Order):
- Adjusting damage formulas
- Sixtyupgrades character sheet urls
- Wowhead weapon urls

### Known Bugs:
- None
""")

st.header('Hunter specs', divider=True)

col1, col2 = st.columns(2)
with col1:
    level = st.number_input('level:', min_value=0, max_value=60, value=40, step=1)
    strength = st.number_input('strength:', min_value=0, value=53, step=1)
    intel = st.number_input('intelligence:', min_value=0, value=40, step=1)

with col2:
    race_wid = st.selectbox('race:', ['night elf','dwarf','tauren','orc','troll'], index=0)
    agi = st.number_input('agility:', min_value=0, value=175, step=1)
    spirit = st.number_input('spirit:', min_value=0, value=40, step=1)

spec = st.text_input('Input talents url from wowhead:', 'https://www.wowhead.com/classic/talent-calc/hunter/--330220221232315')
st.markdown("[Wowhead hunter talents url](https://www.wowhead.com/classic/talent-calc/hunter)")

# Display mh and oh next to each other
col1, col2, col3 = st.columns(3)

with col1:
    chest_runes = st.selectbox('Chest rune:', ['lion', 'lone wolf', 'master marksman', None], index=0)
    belt_runes = st.selectbox('Belt rune:', ['melee spec', None], index=0)

with col2:
    leg_runes = st.selectbox('Leg rune:', ['flanking'], index=0)
    boot_runes = st.selectbox('Boot rune:', ['dual wield spec', 'trap launcher', None], index=0)

with col3:
    hand_runes = st.selectbox('Hand rune:', ['beast master', 'carve', None], index=1)

st.subheader('Extra stats')
col1, col2, col3 = st.columns(3)
with col1:
    ex_hit = st.number_input('extra hit percent:', min_value=0, value=1, step=1)
    ex_crit = st.number_input('extra crit:', min_value=0, value=0, step=1)
with col2:
    ex_ap = st.number_input('extra ap:', min_value=0, value=54, step=1)
    ex_rap = st.number_input('extra rap:', min_value=0, value=0, step=1)
with col3:
  lw_wid = st.selectbox('leather:', ['haste gloves','haste helm', None], index=1)
  engi_wid = st.selectbox('engineering:', ['high-yield radiation bomb', None], index=0)

st.header('Weapon specs', divider=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Main Hand (MH)')
    wep_proc_wid1 = st.selectbox('mh proc:', ['shadowfang', 'talwar', 'meteor', 'hydra', 'fathom', 'bloodpike', 'duskbringer', 'grimclaw', "serra'kis", 'None'], index=9)
    wep_spd1 = st.number_input('mh speed:', min_value=0.0, value=2.7, step=0.1)
    mh_range = st.slider('mh dmg', 0, 200, (55, 104))

with col2:
    st.subheader('Off Hand (OH)')
    wep_proc_wid2 = st.selectbox('oh proc:', ['gust', 'meteor', 'grimclaw', 'bootknife', "serra'kis", 'None'], index=5)
    wep_spd2 = st.number_input('oh speed:', min_value=0.0, value=2.2, step=0.1)
    oh_range = st.slider('oh dmg', 0, 200, (46, 86))

col1, col2 = st.columns(2)
with col1:
  mh_race_wep_wid = st.checkbox('mh +5 wep skill', value=False)
  oh_race_wep_wid = st.checkbox('oh +5 wep skill', value=False)
  twoh_wid = st.checkbox('twohand', value=False)

with col2:
  same_type_wid = st.checkbox('same wep type', value=True)
  enchant_wid = st.checkbox('+wep dmg enchants', value=True)

st.header('Pet specs', divider=True)

col1, col2 = st.columns(2)
with col1:
  pett = st.selectbox('pet:', ['monke', 'ws', 'cat'], index=2)
with col2:
  pett_spd = st.number_input('pet speed:', min_value=0.1, value=2.0, step=0.1)

st.header('Fight simulation specs', divider=True)
duration_wid = st.number_input('Fight duration:', min_value=5, value=45, step=5)

st.subheader('Consumes:')
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
  agi_elixir = st.checkbox('Agi Elixir', value=True)
with col2:
  str_elixir = st.checkbox('Str Elixir', value=True)
with col3:
  mana_pot = st.checkbox('Mana Pot', value=True)
with col4:
  str_scroll = st.checkbox('Pet Str Scroll', value=True)
with col5:
  oh_stone = st.checkbox('Offhand Stone', value=True)

st.subheader('Buffs:')
col1, col2, col3 = st.columns(3)
with col1:
    raid_buffs1 = {}
    raid_buffs1['mage'] = st.checkbox('Arcane Int', value=True)
    raid_buffs1['warr'] = st.checkbox('Battle Shout', value=True)
    raid_buffs1['palamight'] = st.checkbox('Blessing of Might', value=True)
    raid_buffs1['palahorn'] = st.checkbox('Horn of Lordaeron', value=False)
with col2:
    raid_buffs2 = {}
    raid_buffs2['druid'] = st.checkbox('Mark of the Wild', value=True)
    raid_buffs2['shamstr'] = st.checkbox('Strength Totem', value=False)
    raid_buffs2['hunterlion'] = st.checkbox('Blessing of Kings/Lion', value=False)
    raid_buffs2['hunterap'] = st.checkbox('Trueshot Aura', value=False)

with col3:
    raid_buffs3 = {}
    # raid_buffs3['shamagi'] = st.checkbox('Agi Totem')
    raid_buffs3['feralcrit'] = st.checkbox('Leader of the Pack', value=True)
    raid_buffs3['feralwf'] = st.checkbox('Windfury', value=True)
    world_buffs = {}
    world_buffs['dmf'] = st.checkbox('Darkmoon Faire', value=True)
    # world_buffs['gnomer'] = st.checkbox('Spark of Inspiration', disabled=True)


iter = st.number_input('Number of iterations:', min_value=100, value=300, step=1)


if st.sidebar.button('Calculate DPS'):
    global trials
    trials = []

    progress_bar = st.sidebar.progress(0)

    for i in range(iter):
        trials.append(run_sim())

        # Update the progress bar
        progress_bar.progress((i + 1) / iter)

    app_report(trials)
  
st.sidebar.subheader('Previous Simulations:')
if st.session_state.prev_sims:
  st.sidebar.write(pd.DataFrame({'Avg. DPS': st.session_state.prev_sims}))

  if st.sidebar.button('Reset previous sims'):
     st.session_state.prev_sims = []
