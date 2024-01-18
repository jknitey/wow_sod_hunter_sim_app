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

    if rbuff_wid == True:
        hunter['str'] = hunter['str'] + 4
        hunter['agi'] = hunter['agi'] + 4

    hunter['mana'] = ((attributes['int'] - 34) * 15) + 841
    hunter['spirit'] = attributes['spirit']

    try:
      talent_points = attributes['spec'].split('hunter/')[1]
    except ValueError:
      print('Use a wowhead classic hunter url.')

    talents = {}
    try:
      talents['bm'] = [x for x in talent_points.split('-')[0]]
    except:
      talents['bm'] = ['0']
    try:
      talents['mm'] = [x for x in talent_points.split('-')[1]]
    except:
      talents['mm'] = ['0']
    try:
      talents['sv'] = [x for x in talent_points.split('-')[2]]
    except:
      talents['sv'] = ['0']

    hunter['spec'] = talents
    hunter['hit'] = attributes['hit']

    try:
      if hunter['spec']['sv'][10] != 0:
          hunter['hit'] += int(hunter['spec']['sv'][10])
    except:
      pass

    # weapon
    hunter['spd'] = weapons['spd']

    if (enchant_wid == True) and (weapons['spd'][1] == 0):
        hunter['wep'] = ((weapons['dmg'][0][0] + 3, 0), (weapons['dmg'][1][0] + 3, 0))

    if (enchant_wid == True) and (weapons['spd'][1] != 0):
        hunter['wep'] = ((weapons['dmg'][0][0] + 2, weapons['dmg'][0][1] + 2), (weapons['dmg'][1][0] + 2, weapons['dmg'][1][1] + 2))

    else:
        hunter['wep'] = weapons['dmg']

    if consume_wid == True:
        hunter['mana'] = hunter['mana'] + 700
        hunter['agi'] = hunter['agi'] + 8
        hunter['str'] = hunter['str'] + 8

        if hunter['spd'][1] != 0:
            hunter['hit'] = hunter['hit'] + 2

    # melee stats
    hunter['crit'] = 3.09 + (0.052 * (hunter['agi'] - 60))
    hunter['ap'] = 118 + (hunter['str'] - 28) + (hunter['agi'] - 60)

    if bfd_wid == True:
        hunter['crit'] = hunter['crit'] = 2
        hunter['ap'] = hunter['ap'] + 20

    if rbuff_wid == True:
        hunter['ap'] = hunter['ap'] + 60 + 55
        hunter['mana'] = hunter['mana'] + (7 * 15)

    hunter['ap'] = hunter['ap'] + ex_ap

    if race_wid == 'orc':
      base_ap =  hunter['str'] +  hunter['agi'] + (25 * 2) - 20
      orc_bonus = (base_ap * 0.25) * 15 / duration_wid # ap is in units of dps so we can transform it to get orc bonus ap over the whole fight -- cleans up later calcs
      hunter['ap'] = hunter['ap'] + orc_bonus

    return hunter

#@title Auto Attack
def melee(mh):

    if mh == True:

        min_dmg = hunter['ap']/14 * hunter['spd'][0] + hunter['wep'][0][0]
        max_dmg = hunter['ap']/14 * hunter['spd'][0] + hunter['wep'][1][0]

    else:

        min_dmg = ((hunter['ap']/14 * hunter['spd'][1]) + hunter['wep'][0][1]) * 0.5
        max_dmg = ((hunter['ap']/14 * hunter['spd'][1]) + hunter['wep'][1][1]) * 0.5

    return (min_dmg, max_dmg)

#@title Windfury Attack
def windfury_proc(wf_mod = 1.2):

    min_dmg = (hunter['ap'] * wf_mod)/14 * hunter['spd'][0] + hunter['wep'][0][0]
    max_dmg = (hunter['ap'] * wf_mod)/14 * hunter['spd'][0] + hunter['wep'][1][0]

    return (min_dmg, max_dmg)

#@title Pet Auto Attack
def pet_auto():

    if rbuff_wid == True:
        ap = pet['ap'] + 55 + 60
    else:
        ap = pet['ap']

    min_dmg = pet['dmg'][0] + (ap * pet['spd'] / 14)
    max_dmg = pet['dmg'][1] + (ap * pet['spd'] / 14)

    return (min_dmg, max_dmg)

#@title Melee Attack Table
def attack_table(roll, mh, hit = 0, pet = False, spell = ''):

    if pet == True:

      crit = 5

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

    if (spell != 'rs') & (spell != 'wc') & (spell != 'fs'):
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
        dmg = melee(mh)
        dmg = (dmg[0] + 35, dmg[1] + 35)

    else:
        dmg = melee(mh)

    if (spell != 'wc') and (spell != 'fs'):
        dmg = dmg[0] + (np.random.random() * (dmg[1] - dmg[0]))

    elif spell == 'fs':

        dmg = (hunter['ap']/14 * hunter['spd'][0] + hunter['wep'][1][0])

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
        res = ('rs' + res[0], res[1])

    elif spell == 'wc':
        res = ('wc' + res[0], res[1])

    elif spell == 'fs':
        res = ('fs' + res[0], res[1])

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

  if (race_wid == 'troll') and (glove_wid == 'haste gloves'):

    mh_speed = mh_speed / 1.2

  elif glove_wid == 'haste gloves':

    mh_speed = mh_speed / 1.1

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

      if (race_wid == 'troll') and (glove_wid == 'haste gloves'):

        oh_speed = mh_speed / 1.2

      elif glove_wid == 'haste gloves':

        oh_speed = mh_speed / 1.1

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

#@title Sim FS/WC Rotation
def sim_rotation(duration):

    globals = np.floor(duration / 1.5)

    flanking_cd = 30 / 1.5

    flanking = {'state': 'ready', 'cd': 0, 'mana':18}
    wingclip = {'state': 'ready', 'cd': 0, 'mana':40}

    events = []

    for gcd in np.arange(0, globals):

        if flanking['cd'] == gcd: flanking['state'] = 'ready'

        if flanking['state'] == 'ready':

            dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'fs')
            events += [(gcd * 1.5, dmg[0], dmg[1])]
            events += [(gcd * 1.5, 'pet ' + dmg[0], 0.375 * pet['spd'] * pet_auto()[1])]

            flanking['state'] = 'down'
            flanking['cd'] = gcd + flanking_cd
            continue

        if wingclip['state'] == 'ready':
            dmg = attack_table(roll = np.random.randint(0,1001), mh = True, hit = hunter['hit'], spell = 'wc')

            events += [(gcd * 1.5, dmg[0], dmg[1])]

    log = pd.DataFrame(events)
    log.columns = ['time','attack','dmg']

    return log

#@title Sim Raptor Strike Placements
def sim_raptor_strikes(white, yellow, duration):

    mh_hits = white[white.attack.str.contains('mh')]
    mh_hits.time = mh_hits.time.round(1)
    flankings = yellow[(yellow.attack.str.contains('fs hit')) | (yellow.attack.str.contains('fs crit'))].time.to_list()

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

    if len(flankings) > 0:

        for i in np.arange(0, len(flankings)):

            raptor_strikes['buff_end'] = flankings[i] + 10
            raptor_strikes['buff_remaining'] = raptor_strikes['buff_end'] - raptor_strikes['time']
            raptor_strikes['buff_active'] = [1 if 0 < x <= 10 else 0 for x in raptor_strikes['buff_remaining']]
            raptor_strikes['dmg'] = [x * 1.1 if y == 1 else x for x,y in zip(raptor_strikes['dmg'], raptor_strikes['buff_active'])]

        raptor_strikes = raptor_strikes.drop(['buff_end','buff_active','buff_remaining'], axis = 1)

    mh_hits = mh_hits[~mh_hits.index.isin(ix)]

    log = pd.concat([mh_hits, raptor_strikes, white[~white.attack.str.contains('mh')]]).drop_duplicates().sort_values(['time','attack'])

    return log

#@title Sim Windfury Procs
def sim_windfury(combat_log):

    valid_hits = combat_log[(combat_log.attack.str.contains('fs')) | (combat_log.attack.str.contains('wc')) | (combat_log.attack.str.contains('mh'))]
    windfury = {'state': 'ready', 'cd': 0}
    windfury_cd = 3
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
        valid_hits = combat_log[(combat_log.attack.str.contains('fs')) | (combat_log.attack.str.contains('wc')) | (combat_log.attack.str.contains('mh'))]
    else:
        valid_hits = combat_log[combat_log.attack.str.contains('oh')]

    procs = {'shadowfang': {'state': 'ready', 'cd': 0, 'dmg': 30, 'rate': 5.5, 'icd':0},
             'gust': {'state': 'ready', 'cd': 0, 'dmg': 15, 'rate': 7.5, 'icd': 0},
             'talwar': {'state': 'ready', 'cd': 0, 'dmg': 30, 'rate': 15, 'icd': 0},
             'meteor': {'state': 'ready', 'cd': 0, 'dmg': 37.5, 'rate': 3, 'icd': 0},
             'hydra': {'state': 'ready', 'cd': 0, 'dmg': 120, 'rate': 3.5, 'icd': 0},
             'fathom': {'state': 'ready', 'cd': 0, 'dmg': 50, 'rate': 4, 'icd': 0},
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

    mana = float(hunter['mana'])
    total_mana = [mana]

    for i,event in combat_log.iterrows():

        if event.time < 0:
            pass

        else:
            if event.cost > 0:
                total_mana += [mana - event.cost]
                mana -= event.cost
            else:
                total_mana += [mana]

    return total_mana

#@title Sim Pet Damage
def sim_pet(duration):

    pet_info = {'ws': {'dmg': (36,40), 'cost': 50, 'mod': 1.07},
                'cat': {'dmg': {'claw':(16,22),'bite':(31,37)}, 'cost': {'claw':25,'bite':35}, 'mod': 1.1}

               }[pet['type']]

    spec_mod = 1.0

    bm_rune_mod = 1.2

    try:
      if hunter['spec']['bm'][8] != 0:
        spec_mod += int(hunter['spec']['bm'][8]) * 0.04
    except:
      pass

    # using old blizzard formulas result in pet autos that are ~2x too big from looking thru logs
    # check sources for pet auto formulas to check for yourself
    if pet['type'] == 'ws':
      blizard_petauto_mod = 0.45
    else:
      blizard_petauto_mod = 0.35

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
    bm_rune_focus_mod = 1.5

    focus_rate *= bm_rune_focus_mod

    if pet['type'] == 'ws':
        opening_gcd = np.floor(100 / pet_info['cost'])
        total_focus = 100 + (duration - (opening_gcd * 1.5)) * focus_rate
        max_casts = np.floor(total_focus / pet_info['cost'])

        ws_sp_scaling = pet['ap'] * 0.35

        def ws_dmg():

          cast_dmg = (np.random.randint(pet_info['dmg'][0],pet_info['dmg'][1] + 1) + ws_sp_scaling) * pet_info['mod'] * spec_mod * bm_rune_mod
          crit_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
          if 'crit' in crit_roll[0]:
            cast_dmg *= 1.5
            msg = 'pet cast crit'
          else:
            msg = 'pet cast'
          return (cast_dmg, msg)

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
        cat_ap_scaling['bite'] = pet['ap'] * 0.35
        cat_ap_scaling['claw'] = pet['ap'] * 0.24

        def cat_dmg(spell):

          cast_dmg = (np.random.randint(pet_info['dmg'][spell][0],pet_info['dmg'][spell][1] + 1) + cat_ap_scaling[spell]) * pet_info['mod'] * spec_mod * bm_rune_mod
          crit_roll = attack_table(roll = np.random.randint(0,1001), mh = True, hit = np.floor(hunter['hit']), pet = True)
          if 'crit' in crit_roll[0]:
            cast_dmg *= 2
            msg = 'pet cast crit'
          else:
            msg = 'pet cast'
          return (cast_dmg, msg)

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

    if race_wid == 'orc':
      pet_casts.dmg = pet_casts.dmg * 1.05
      pet_hits.dmg = pet_hits.dmg * 1.05

    return pet_hits, pet_casts

#@title Sim Encounter
def sim_fight(duration, coh):

    white = sim_autos(duration)
    yellow = sim_rotation(duration)
    raptors = sim_raptor_strikes(white, yellow, duration)

    combat_log = pd.concat([yellow, raptors]).sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    log = pd.DataFrame({'time':-1.0,'attack':'start','dmg':0.0,'cost':0}, index = [0])
    mana_cost = pd.DataFrame([
        {'attack':'fs','cost':18},
        {'attack':'wc hit','cost':40},
        {'attack':'wc crit','cost':40},
        {'attack':'rs hit','cost':45},
        {'attack':'rs crit','cost':45}], index = [0,1,2,3,4])
    combat_log = pd.concat([log, combat_log.merge(mana_cost, how = 'left')]).drop_duplicates().fillna(0.0)
    combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    if wf_wid == True:
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

    if glove_wid == 'red whelp gloves':
      rwg_procs = sim_whelp_gloves(combat_log)
      if len(rwg_procs) > 0:
        combat_log = pd.concat([rwg_procs, combat_log]).fillna(0.0)
        combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)

    if dmf_wid == True:
        combat_log.dmg = combat_log.dmg*1.1

    if pvp_wid == True:
        combat_log.dmg = combat_log.dmg*1.05

    pet_hits, pet_casts = sim_pet(duration)
    if (len(pet_hits) > 0) and (chest_runes != 'lone wolf'):
        combat_log = pd.concat([pet_hits, pet_casts, combat_log]).fillna(0.0)
        combat_log = combat_log.sort_values(['time', 'attack'],ascending = [True, True]).reset_index(drop=True)
    elif chest_runes == 'lone wolf':
      combat_log.dmg = combat_log.dmg*1.15
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
  display(results)

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

  pet = {'dmg': pett_range,
         'spd': pett_spd,
         'ap': pett_ap,
         'type': pett}

  if consume_wid == True:
    pet['ap'] = pet['ap'] + 16 # pets get 2 ap for 1 str

  if rbuff_wid == True:
    pet['ap'] = pet['ap'] + 55 + 60 # might and shout

  globals()['pet'] = pet

  global duration
  duration = duration_wid
  iterations = iter

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
Enter your stats:

- Weapon stats come from the item tooltip NOT the character panel
- To sim 2h, set all the offhand options to 0 and select 'Twohand'
- Character and pet stats come from the character panel
- You should have on lion and hawk when transferring your stats to the sim (so we can bypass stat scaling from hunter to pet)
- Extra stats come from item tooltips (i.e. hit/ap on crafting items or weps)

Set encounter info:

- Rune setup is assumed to be melee bis (lion, bm, flanking)
- Enter talents using wowhead sod calc url. Default is bm: [BM Talent Calculator](https://www.wowhead.com/classic/talent-calc/hunter/05003200501)
- Duration is encounter length in seconds
- Iterations is the number of simulations to run (use 3k+ for settings similar to wowsims)

Set additional options:

- Enchants (wep dmg)
- Consumes (mana potion, minor recombobulator, offhand stone, elixirs, pet scrolls)
- Catfury
- Raid buffs (shout, might, mark, int)
- World buffs (dmf, bfd, ashen)


Things This Sim Is Good At:

- Comparing gear options
- Comparing dps without optimal setups (enchants, buffs, wf)
- Comparing SV vs BM on SHORT fights (<45s, where flanking reset is less likely)

Things This Sim Is Not Good At:

- Getting 100%/ accurate raid dps numbers (sims are for comps and i am not implementing boss armor/resist)
- Very long fight lengths (>120s, on longer fights fishing and mana regen are more important -- all fights in bfd are under 2 min)

""")

st.header('Hunter specs', divider=True)

race_wid = st.selectbox('race:', ['other', 'orc', 'troll'], index=0)

col1, col2 = st.columns(2)
with col1:
    strength = st.number_input('strength:', min_value=0, value=65, step=1)
    intel = st.number_input('intelligence:', min_value=0, value=50, step=1)

with col2:
    agi = st.number_input('agility:', min_value=0, value=165, step=1)
    spirit = st.number_input('spirit:', min_value=0, value=50, step=1)

spec = st.text_input('Input talents url from wowhead:', 'https://www.wowhead.com/classic/talent-calc/hunter/05003200501')
st.markdown("[Wowhead hunter talents url](https://www.wowhead.com/classic/talent-calc/hunter)")

# Display mh and oh next to each other
col1, col2, col3 = st.columns(3)

with col1:
    chest_runes = st.selectbox('Chest rune:', ['lion', 'lone wolf'], index=0)

with col2:
    leg_runes = st.selectbox('Leg rune:', ['flanking'], index=0)

with col3:
    hand_runes = st.selectbox('Hand rune:', ['beast master'], index=0)

st.subheader('Extra stats')
col1, col2, col3 = st.columns(3)
with col1:
    ex_hit = st.number_input('extra hit percent:', min_value=0, value=0, step=1)
with col2:
    ex_ap = st.number_input('extra ap:', min_value=0, value=0, step=1)
with col3:
  glove_wid = st.selectbox('gloves:', ['haste gloves', 'red whelp gloves', None], index=2)

st.header('Weapon specs', divider=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Main Hand (MH)')
    wep_proc_wid1 = st.selectbox('mh proc:', ['shadowfang', 'talwar', 'meteor', 'hydra', 'fathom', 'bloodpike', 'duskbringer', 'grimclaw', "serra'kis", 'None'], index=1)
    wep_spd1 = st.number_input('mh speed:', min_value=0.1, value=2.7, step=0.1)
    mh_range = st.slider('mh dmg', 0, 200, (43, 82))
    mh_race_wep_wid = st.checkbox('mh race wep spec')

with col2:
    st.subheader('Off Hand (OH)')
    wep_proc_wid2 = st.selectbox('oh proc:', ['gust', 'meteor', 'grimclaw', 'bootknife', "serra'kis", 'None'], index=2)
    wep_spd2 = st.number_input('oh speed:', min_value=0.1, value=1.4, step=0.1)
    oh_range = st.slider('oh dmg', 0, 200, (21, 38))
    oh_race_wep_wid = st.checkbox('oh race wep spec')

twoh_wid = st.checkbox('twohand')
if twoh_wid == True:
    wep_proc_wid2 = 'None'
    wep_spd2 = 0.0
    oh_range = (0,0)

st.header('Pet specs', divider=True)

col1, col2 = st.columns(2)
with col1:
    pett = st.selectbox('pet:', ['ws', 'cat'], index=0)
with col2:
  pett_spd = st.number_input('pet speed:', min_value=0.1, value=2.0, step=0.1)

pett_range = st.slider('pet dmg', 0, 150, (82, 96), 1)
pett_ap = st.number_input('pet ap:', min_value=0, value=190, step=1)

st.header('Fight simulation specs', divider=True)
duration_wid = st.number_input('Fight duration:', min_value=5, value=45, step=5)

st.subheader('Buffs:')
col1, col2, col3 = st.columns(3)
with col1:
    consume_wid = st.checkbox('consumes')
    enchant_wid = st.checkbox('enchants')
with col2:
    rbuff_wid = st.checkbox('raid buffs')
    bfd_wid = st.checkbox('bfd buff')
with col3:
    dmf_wid = st.checkbox('dmf buff')
    wf_wid = st.checkbox('catfury')
pvp_wid = st.checkbox('ashen buff')

iter = st.number_input('Number of iterations:', min_value=100, value=100, step=100)


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
