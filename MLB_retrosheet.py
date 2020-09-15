# -*- coding: utf-8 -*-
"""

Author: Daniel R. Ciarrocki, Copyright (c) 2020
License: MIT License


Description:
    Scripts to download and parse retrosheet.org event files.

    The main parsing function, parse_retro_event_file, returns dictionaries
    containing data for all games and plate appearances in the file.   


Function List:
    download_unpack_retro_event_files
    parse_retro_event_file

"""



### TESTING/DEV

TestFile1 = '/home/dan/MLBstat/data/retrosheet/EventFiles2010/2010ANA.EVA'




### Imports/Dependencies

import os
import re
import requests
import zipfile




### Globals and Constants

# The files specified in these URLs contain all data for seasons 1910-2019.
EVENT_FILE_URLS = ['https://www.retrosheet.org/events/1910seve.zip',
                   'https://www.retrosheet.org/events/1920seve.zip',
                   'https://www.retrosheet.org/events/1930seve.zip',
                   'https://www.retrosheet.org/events/1940seve.zip',
                   'https://www.retrosheet.org/events/1950seve.zip',
                   'https://www.retrosheet.org/events/1960seve.zip',
                   'https://www.retrosheet.org/events/1970seve.zip',
                   'https://www.retrosheet.org/events/1980seve.zip',
                   'https://www.retrosheet.org/events/1990seve.zip',
                   'https://www.retrosheet.org/events/2000seve.zip',
                   'https://www.retrosheet.org/events/2010seve.zip',]

NOT_PITCHES = '+*.123>'




### Main Functions

def download_unpack_retro_event_files(save_path='/data/retrosheet/'):

    # Process the save path and create directory if necessary
    pro_save_path = save_path if save_path[0] == '/' else '/' + save_path
    final_save_path = os.getcwd() + pro_save_path
    if not os.path.exists(final_save_path): os.makedirs(final_save_path)

    # Download and write the files
    file_set = set()
    for url in EVENT_FILE_URLS:
        res = requests.get(url)
        file_name = url.split('/')[-1]
        with open(final_save_path + file_name, 'wb') as write_file:
            write_file.write(res.content)
            file_set.add(final_save_path + file_name)

    # Upnack and then delete each zip file we downloaded
    for zip_file_path in [file for file in file_set if file.endswith('.zip')]:
        year_directory = zip_file_path.split('/')[-1][:4]
        if not year_directory.isnumeric(): continue
        year_directory = final_save_path + '/' + 'EventFiles' + year_directory + '/'
        if not os.path.exists(year_directory): os.makedirs(year_directory)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            print(year_directory)
            zip_ref.extractall(year_directory)
        os.remove(zip_file_path)




def parse_retro_event_file(file_path=TestFile1):
 
    # Quick file check
    if re.search('TEAM\d\d\d\d', file_path): return {}, {}
    if file_path.lower().endswith('ros'): return {}, {}

    all_games = {}
    all_PAs = {}

    for game in event_file_game_generator(file_path):

        this_game = {}
        pa_counter = {}
        current_players = {0: {}, 1: {}}
        this_game['home_runs'] = 0
        this_game['away_runs'] = 0

        #CHANGE TEAM FIELDS TO AN ENUM DATA TYPE?

        for row in game:

            if row.startswith('info'): parse_info_line(this_game, row)

            elif row.startswith('play'): 

                newPA = parse_play_line(row, this_game['home_team'] + 
                                        game[0].split(',')[1][3:].strip(), 
                                        pa_counter, current_players,
                                        this_game['date'], 
                                        this_game['home_team'],
                                        this_game['away_team'],)
                all_PAs[newPA['PAID']] = newPA

                if newPA['home']: this_game['home_runs'] += newPA['runs']
                else: this_game['away_runs'] += newPA['runs']

            elif row.startswith('start') or row.startswith('sub'): 
                parse_player_line(row, current_players)

        set_win_loss(this_game, this_game['home_runs'], this_game['away_runs'])
        gameID = this_game['home_team'] + game[0].split(',')[1][3:].strip()
        this_game['gameID'] = gameID       
        
        all_games[gameID] = this_game

    return all_games, all_PAs




### Helper Functions 

def event_file_game_generator(file_path):
    
    current_game_rows = []
    first_flag = True

    for row in open(file_path, 'r'):

        # If it is an 'id' row, yield results and reset (unless first time)
        if row.startswith('id'):
            if first_flag:
                first_flag = False
                current_game_rows.append(row)
            else:
                yield(current_game_rows)
                current_game_rows = []
                current_game_rows.append(row)
            continue

        current_game_rows.append(row)

    # Yield results for the final game
    yield(current_game_rows)




def parse_info_line(game_dict, row):

        row_parts = row.strip().split(',')
        
        if row_parts[1] == 'visteam': game_dict['visiting_team'] = row_parts[2]
        if row_parts[1] == 'hometeam': game_dict['home_team'] = row_parts[2]
        if row_parts[1] == 'visteam': game_dict['away_team'] = row_parts[2]
        if row_parts[1] == 'date': game_dict['date'] = row_parts[2]
        if row_parts[1] == 'site': game_dict['site'] = row_parts[2]
        if row_parts[1] == 'starttime': game_dict['start_time'] = row_parts[2]
        if row_parts[1] == 'day': 
            game_dict['day'] = True if row_parts[2] == 'day' else False
        if row_parts[1] == 'usedh': 
            game_dict['dh'] = True if row_parts[2] == 'true' else False
        if row_parts[1] == 'umphome': game_dict['ump_home'] = row_parts[2]
        if row_parts[1] == 'ump1b': game_dict['ump_first'] = row_parts[2]
        if row_parts[1] == 'ump2b': game_dict['ump_second'] = row_parts[2]
        if row_parts[1] == 'ump3b': game_dict['ump_third'] = row_parts[2]
        if row_parts[1] == 'pitches': game_dict['pitches'] = row_parts[2]
        if row_parts[1] == 'temp': game_dict['temperature'] = row_parts[2]
        if row_parts[1] == 'winddir': game_dict['wind_direction'] = row_parts[2]
        if row_parts[1] == 'windspeed': game_dict['wind_speed'] = row_parts[2]
        if row_parts[1] == 'fieldcond': game_dict['field_condition'] = row_parts[2]
        if row_parts[1] == 'precip': game_dict['precipitation'] = row_parts[2]
        if row_parts[1] == 'sky': game_dict['sky'] = row_parts[2]
        if row_parts[1] == 'timeofgame': game_dict['game_length'] = row_parts[2]
        if row_parts[1] == 'attendance': game_dict['attendance'] = row_parts[2]
        if row_parts[1] == 'wp': game_dict['winning_pitcher'] = row_parts[2]
        if row_parts[1] == 'lp': game_dict['losing_pitcher'] = row_parts[2]
        if row_parts[1] == 'save': game_dict['save_pitcher'] = row_parts[2]




def parse_player_line(row, current_players):

    row_parts = row.strip().split(',')
    if len(row_parts) < 6: return

    playerID = row_parts[1]
    player_name = row_parts[2]
    home = int(row_parts[3])
    batting_position = int(row_parts[4])
    fielding_position = int(row_parts[5])   

    current_players[home][fielding_position] = {
        'playerID':playerID, 'player_name':player_name, 'home':home, 
        'batting_position': batting_position, 
        'fielding_position':fielding_position}




def parse_play_line(row, gameID, pa_counter, current_players, date, home_team,
                    away_team):

    PA = {}
    PA['home_team'] = home_team
    PA['away_team'] = away_team
    PA['date'] = date
    
    row_parts = row.strip().split(',')

    PA['inning'] = row_parts[1]
    PA['home'] = True if row_parts[2] == '1' else False
    PA['batterID'] = row_parts[3]
    PA['final_count'] = row_parts[4]
    PA['pitch_sequence'] = row_parts[5]
    PA['num_pitches'] = count_num_pitches(PA['pitch_sequence'], 
                                          PA['final_count'])

    home_away = 0 if PA['home'] else 1
    if 1 in current_players[home_away].keys():
        pitcherID = current_players[home_away][1]['playerID']
    else: pitcherID = None
    PA['pitcherID'] = pitcherID

    PA['PAID'] = gameID + '_' + PA['batterID'] + '_' + str(pa_counter.get(PA['batterID'], 1))
    pa_counter[PA['batterID']] = pa_counter.get(PA['batterID'], 1) + 1
    PA['gameID'] = gameID

    event = ''
    for piece in row_parts[6:]: event += piece

    basic_play, modifiers, advances = process_event(event)
    parse_event(PA, basic_play, modifiers, advances)

    return PA




def parse_event(PA_dict, basic_play, modifiers, advances):

    modifiers_string = ''
    for m in modifiers: modifiers_string += m + '/'
    advances_string = ''
    for s in advances: advances_string += ';'
    full_string = basic_play + '/' + modifiers_string + advances_string

    # Elemental Fields

    if basic_play[0] == 'S': PA_dict['single'] = True
    else: PA_dict['single'] = False

    if basic_play[0] == 'D': PA_dict['double'] = True
    else: PA_dict['double'] = False

    if basic_play.startswith('DGR'): PA_dict['ground_rule_double'] = True
    else: PA_dict['ground_rule_double'] = False

    if basic_play[0] == 'T': PA_dict['triple'] = True
    else: PA_dict['triple'] = False

    if basic_play[0] == 'H' and (basic_play[1] != 'P' and basic_play[1] != 'B'): 
        PA_dict['home_run'] = True
    else: PA_dict['home_run'] = False

    if basic_play[0] == 'K': PA_dict['strike_out'] = True
    else: PA_dict['strike_out'] = False

    if basic_play[0] == 'I': 
        PA_dict['intentional_walk'] = True
        PA_dict['walk'] = True
    else: PA_dict['intentional_walk'] = False

    if basic_play[0] == 'W': PA_dict['walk'] = True
    else: PA_dict['walk'] = False

    if basic_play.startswith('FC'): PA_dict['fielders_choice'] = True
    else: PA_dict['fielders_choice'] = False

    if basic_play[0] == 'E': PA_dict['reached_on_error'] = True
    else: PA_dict['reached_on_error'] = False

    if basic_play[0] == 'H' and (basic_play[1] == 'P' or basic_play[1] == 'B'):
        PA_dict['hit_by_pitch'] = True
    else: PA_dict['hit_by_pitch'] = False

    PA_dict['steals'] = basic_play.count("SB")

    PA_dict['double_plays'] = basic_play.count("DP")

    runs = 1 if PA_dict['home_run'] else 0
    for advance in advances:
        runs += advance.count('-H') + advance.count('-B')
    PA_dict['runs'] = runs

    unearned_runs = 0
    unearned_runs += full_string.count('UR')
    PA_dict['unearned_runs'] = unearned_runs

    RBI = runs
    RBI -= full_string.count('NR')
    PA_dict['RBI'] = RBI


    # Derived fields
    
    PA_dict['hit'] = PA_dict['single'] or PA_dict['double'] or \
                     PA_dict['triple'] or PA_dict['home_run']
        
    PA_dict['on_base'] = PA_dict['hit'] or PA_dict['walk'] or PA_dict['hit_by_pitch']
    
    PA_dict['at_bat'] = not (PA_dict['hit_by_pitch'] or PA_dict['walk'] 
                             or PA_dict['intentional_walk'] 
                             or PA_dict['reached_on_error'])
    
    PA_dict['in_play'] = not (PA_dict['home_run'] or PA_dict['walk']
                              or PA_dict['intentional_walk']
                              or PA_dict['hit_by_pitch'] 
                              or PA_dict['strike_out'])
    
    PA_dict['total_outs'] = -1




def count_num_pitches(pitch_sequence, final_count):    
    num_pitches = len(pitch_sequence)
    if num_pitches == 0 and final_count == '00': num_pitches = 1
    elif len(pitch_sequence) > 0:
        for character in pitch_sequence:
            if character in NOT_PITCHES: num_pitches -= 1
    return num_pitches




def set_win_loss(this_game, home_runs, away_runs):
    if home_runs > away_runs: 
       this_game['home_win'] = True
       this_game['away_win'] = False
       this_game['tie'] = False
    elif away_runs > home_runs: 
       this_game['home_win'] = False
       this_game['away_win'] = True
       this_game['tie'] = False
    else:
       this_game['home_win'] = False
       this_game['away_win'] = False
       this_game['tie'] = True




def process_event(event_string):

    basic_play = ''
    modifiers = []
    advances = []

    if '/' in event_string:
        slash_index = event_string.index('/')
        if '.' in event_string: 
            period_index = event_string.index('.')
            modifiers = event_string[slash_index:period_index].split('/')
            advances = event_string[period_index+1:].split(';')
            advances = [a for a in advances if a != '']
        else:
            modifiers = event_string[slash_index:].split('/')
        modifiers = [m for m in modifiers if m != '']
        basic_play = event_string[:slash_index]

    elif '.' in event_string:
        period_index = event_string.index('.')
        advances = event_string[period_index+1:].split(';')
        advances = [a for a in advances if a != '']
        basic_play = event_string[:period_index]

    else:
        basic_play = event_string    

    return basic_play, modifiers, advances

