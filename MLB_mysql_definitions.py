# -*- coding: utf-8 -*-
"""

Author: Daniel R. Ciarrocki, Copyright (c) 2020
License: MIT License


Description:
    SQL definitions for the mysql database tables that store all project data.

"""



### Tables Definitions

TABLES = {}


TABLES['Games'] = (
    "CREATE TABLE `Games` ( "
    " `gameID` VARCHAR(13), "
    " `away_team` VARCHAR(3), "
    " `home_team` VARCHAR(3), "
    " `home_win` BOOLEAN, "
    " `away_win` BOOLEAN, "
    " `tie` BOOLEAN, "
    " `home_runs` TINYINT, "
    " `away_runs` TINYINT, "
    " `date` DATE, "
    " `site` VARCHAR(40), "
    " `start_time` VARCHAR(20), "
    " `day` BOOLEAN, "
    " `use_dh` BOOLEAN, "
    " `upmire_home` VARCHAR(10), "
    " `upmire_first` VARCHAR(10), "
    " `upmire_second` VARCHAR(10), "
    " `upmire_third` VARCHAR(10), "
    " `total_pitches` SMALLINT, "
    " `temperature` TINYINT, "
    " `wind_direction` VARCHAR(5), "
    " `wind_speed` TINYINT, "
    " `field_condition` VARCHAR(20), "
    " `precipitation` VARCHAR(20), "
    " `sky` VARCHAR(20), "
    " `game_length` VARCHAR(10), "
    " `attendance` MEDIUMINT, "
    " `winning_pitcher` VARCHAR(20), "
    " `losing_pitcher` VARCHAR(20), "
    " `save_pitcher` VARCHAR(20), "
    " PRIMARY KEY (`gameID`) "
    " )")


TABLES['PAs'] = (
    "CREATE TABLE `PAs` ( "
    " `PAID` VARCHAR(20), "
    " `gameID` VARCHAR(13), "
    " `batterID` VARCHAR(10), "
    " `pitcherID` VARCHAR(10), "
    " `away_team` VARCHAR(3), "
    " `home_team` VARCHAR(3), "
    " `date` DATE, "
    " `inning` TINYINT, "
    " `home` BOOLEAN, "
    " `at_bat` BOOLEAN, "
    " `pitch_sequence` VARCHAR(25), "
    " `num_pitches` TINYINT, "
    " `single` BOOLEAN, "
    " `double` BOOLEAN, "
    " `triple` BOOLEAN, "
    " `home_run` BOOLEAN, "
    " `ground_rule_double` BOOLEAN, "
    " `strike_out` BOOLEAN, "
    " `walk` BOOLEAN, "
    " `intentional_walk` BOOLEAN, "
    " `fielders_choice` BOOLEAN, "
    " `reached_on_error` BOOLEAN, "
    " `hit_by_pitch` BOOLEAN, "
    " `double_play` BOOLEAN, "
    " `steals` TINYINT, "
    " `runs` TINYINT, "
    " `RBI` TINYINT, "
    " `hit` BOOLEAN, "
    " `on_base` BOOLEAN, "
    " `in_play` BOOLEAN, "
    " `total_outs` TINYINT, "
    " PRIMARY KEY (`PAID`), "
    " FOREIGN KEY (`gameID`) REFERENCES `Games`(`gameID`) "
    ")")


TABLES['Players'] = (
    "CREATE TABLE `Players` ( "
    " `playerID` VARCHAR(10), "
    " `name` VARCHAR(50), "   
    " PRIMARY KEY (`playerID`) "
    ")")


