import streamlit as st
import time
#import socket
from datetime import timedelta, timezone, datetime
import pandas as pd 
import numpy as np
import qrcode
from PIL import Image
from math import floor

from  .session import fetch_post, fetch_put, fetch_get, fetch_delete
from .singletons import settings, logger


@st.cache
def getqrcode(content):
    logger.info("create qr code")
    logger.info(content)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="#212529")
    logger.info(str(img))
    img.save('./qrcode_test.png')
    return Image.open('./qrcode_test.png')


def getGameInfo(lobby_id, game_id, stage_id):
    return fetch_get(f"{settings.driftapi_path}/driftapi/manage_game/get/{lobby_id}/{game_id}/{stage_id}/")

def getScoreBoard(lobby_id, game_id, stage_id):
    return fetch_get(f"{settings.driftapi_path}/driftapi/game/{lobby_id}/{game_id}/{stage_id}/playerstatus")

def showTime(s):
    if ((s is None) or s==''):
        return ''
    s = float(s)
    ms = floor((s % 1)*1000)
    s = floor(s)
    m = floor(s / 60)
    s = s -60*m
    return f"{m:02d}:{s:02d}.{ms:03d}"
    #return round(float(s),2) if not((s is None) or s== '') else None

def showDistance(s):
    if ((s is None) or s==''):
        return ''
    s = float(s)
    cm = floor((s % 1)*100)
    m = floor(s)
    km = floor(s / 1000)
    m = m - 1000*km
    return f"{km:01d}km {m:03d}m" #{cm:02d}"

# added function for track condition tracking (quite quick and dirty)
def handleCurrentTrackCondition(r:dict):
    if ( ( "enter_data" in r ) and not ( r["enter_data"] is None ) ):
        if ( ("last_recognized_target" in r ) and not ( r["last_recognized_target"] is None ) ):
# handle rally-cross here
            if( r["enter_data"]["track_bundle"] == "rally_cross" ):
                if( r["last_recognized_target"] == 4 ):
                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                elif( r["last_recognized_target"] == 5 ):
                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                elif( r["last_recognized_target"] == 6 ):
                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                elif( r["last_recognized_target"] == 7 ):
                    delay = datetime.now() - datetime.strptime(r["last_target_timestamp"],'%Y-%m-%dT%H:%M:%S.%f')
                    if(delay.total_seconds() <= 3):
                        current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                    else:
                        if( r["second_last_recognized_target"] == 4 ):
                            current_track_condition = f"{st.session_state.track_dry_emoji}"
                        elif( r["second_last_recognized_target"] == 5 ):
                            current_track_condition = f"{st.session_state.track_wet_emoji}"
                        elif( r["second_last_recognized_target"] == 6 ):
                            current_track_condition = f"{st.session_state.track_gravel_emoji}"
                        else:
                            if( r["third_last_recognized_target"] == 4 ):
                                current_track_condition = f"{st.session_state.track_dry_emoji}"
                            elif( r["third_last_recognized_target"] == 5 ):
                                current_track_condition = f"{st.session_state.track_wet_emoji}"
                            elif( r["third_last_recognized_target"] == 6 ):
                                current_track_condition = f"{st.session_state.track_gravel_emoji}"
                            else:
                                if( r["forth_last_recognized_target"] == 4 ):
                                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                                elif( r["forth_last_recognized_target"] == 5 ):
                                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                                elif( r["forth_last_recognized_target"] == 6 ):
                                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                else:
                                    if( r["fith_last_recognized_target"] == 4 ):
                                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                                    elif( r["fith_last_recognized_target"] == 5 ):
                                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                                    elif( r["fith_last_recognized_target"] == 6 ):
                                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                    else: # be aware this might be wrong
                                        if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                            current_track_condition = f"{st.session_state.track_dry_emoji}"
                                        elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                            current_track_condition = f"{st.session_state.track_wet_emoji}"
                                        elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                            current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                        elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                            current_track_condition = f"{st.session_state.track_snow_emoji}"
                                        else:
                                            current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
# handle rally-cross here when last target has been start/finish
                else:
                    if( r["second_last_recognized_target"] == None):
                        if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                            current_track_condition = f"{st.session_state.track_dry_emoji}"
                        elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                            current_track_condition = f"{st.session_state.track_wet_emoji}"
                        elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                            current_track_condition = f"{st.session_state.track_gravel_emoji}"
                        elif(r["enter_data"]["track_condition"] == "drift_ice"):
                            current_track_condition = f"{st.session_state.track_snow_emoji}"
                        else:
                            current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                    elif( r["second_last_recognized_target"] == 4 ):
                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                    elif( r["second_last_recognized_target"] == 5 ):
                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                    elif( r["second_last_recognized_target"] == 6 ):
                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                    else:
# handle rally-cross here when last two target have been start/finish
                        if( r["third_last_recognized_target"] == None):
                            if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                current_track_condition = f"{st.session_state.track_dry_emoji}"
                            elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                current_track_condition = f"{st.session_state.track_wet_emoji}"
                            elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                current_track_condition = f"{st.session_state.track_gravel_emoji}"
                            elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                current_track_condition = f"{st.session_state.track_snow_emoji}"
                            else:
                                current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                        elif( r["third_last_recognized_target"] == 4 ):
                            current_track_condition = f"{st.session_state.track_dry_emoji}"
                        elif( r["third_last_recognized_target"] == 5 ):
                            current_track_condition = f"{st.session_state.track_wet_emoji}"
                        elif( r["third_last_recognized_target"] == 6 ):
                            current_track_condition = f"{st.session_state.track_gravel_emoji}"
                        else:
# handle rally-cross here when last three target have been start/finish
                            if( r["forth_last_recognized_target"] == None):
                                if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                                elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                                elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                    current_track_condition = f"{st.session_state.track_snow_emoji}"
                                else:
                                    current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                            elif( r["forth_last_recognized_target"] == 4 ):
                                current_track_condition = f"{st.session_state.track_dry_emoji}"
                            elif( r["forth_last_recognized_target"] == 5 ):
                                current_track_condition = f"{st.session_state.track_wet_emoji}"
                            elif( r["forth_last_recognized_target"] == 6 ):
                                current_track_condition = f"{st.session_state.track_gravel_emoji}"
                            else:
# handle rally-cross here when last four target have been start/finish
                                if( r["fith_last_recognized_target"] == None):
                                    if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                        current_track_condition = f"{st.session_state.track_snow_emoji}"
                                    else:
                                        current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                                elif( r["fith_last_recognized_target"] == 4 ):
                                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                                elif( r["fith_last_recognized_target"] == 5 ):
                                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                                elif( r["fith_last_recognized_target"] == 6 ):
                                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                else:
# finaly give up... nobody should come to this point...
                                    if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                        current_track_condition = f"{st.session_state.track_snow_emoji}"
                                    else:
                                        current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
# handle rally here
            elif( r["enter_data"]["track_bundle"] == "rally" ):
                if( r["last_recognized_target"] == 4 ):
                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                elif( r["last_recognized_target"] == 5 ):
                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                elif( r["last_recognized_target"] == 6 ):
                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                elif( r["last_recognized_target"] == 7 ):
                    current_track_condition = f"{st.session_state.track_snow_emoji}"
# handle rally here when last target has been start/finish
                else:
                    if( r["second_last_recognized_target"] == None):
                        if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                            current_track_condition = f"{st.session_state.track_dry_emoji}"
                        elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                            current_track_condition = f"{st.session_state.track_wet_emoji}"
                        elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                            current_track_condition = f"{st.session_state.track_gravel_emoji}"
                        elif(r["enter_data"]["track_condition"] == "drift_ice"):
                            current_track_condition = f"{st.session_state.track_snow_emoji}"
                        else:
                            current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                    elif( r["second_last_recognized_target"] == 4 ):
                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                    elif( r["second_last_recognized_target"] == 5 ):
                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                    elif( r["second_last_recognized_target"] == 6 ):
                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                    elif( r["second_last_recognized_target"] == 7 ):
                        current_track_condition = f"{st.session_state.track_snow_emoji}"
                    else:
# handle rally here when last two target have been start/finish
                        if( r["third_last_recognized_target"] == None):
                            if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                current_track_condition = f"{st.session_state.track_dry_emoji}"
                            elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                current_track_condition = f"{st.session_state.track_wet_emoji}"
                            elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                current_track_condition = f"{st.session_state.track_gravel_emoji}"
                            elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                current_track_condition = f"{st.session_state.track_snow_emoji}"
                            else:
                                current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                        elif( r["third_last_recognized_target"] == 4 ):
                            current_track_condition = f"{st.session_state.track_dry_emoji}"
                        elif( r["third_last_recognized_target"] == 5 ):
                            current_track_condition = f"{st.session_state.track_wet_emoji}"
                        elif( r["third_last_recognized_target"] == 6 ):
                            current_track_condition = f"{st.session_state.track_gravel_emoji}"
                        elif( r["third_last_recognized_target"] == 7 ):
                            current_track_condition = f"{st.session_state.track_snow_emoji}"
                        else:
# handle rally here when last three target have been start/finish
                            if( r["forth_last_recognized_target"] == None):
                                if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                                elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                                elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                    current_track_condition = f"{st.session_state.track_snow_emoji}"
                                else:
                                    current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                            elif( r["forth_last_recognized_target"] == 4 ):
                                current_track_condition = f"{st.session_state.track_dry_emoji}"
                            elif( r["forth_last_recognized_target"] == 5 ):
                                current_track_condition = f"{st.session_state.track_wet_emoji}"
                            elif( r["forth_last_recognized_target"] == 6 ):
                                current_track_condition = f"{st.session_state.track_gravel_emoji}"
                            elif( r["forth_last_recognized_target"] == 7 ):
                                current_track_condition = f"{st.session_state.track_snow_emoji}"
                            else:
# handle rally here when last four target have been start/finish
                                if( r["fith_last_recognized_target"] == None):
                                    if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                        current_track_condition = f"{st.session_state.track_snow_emoji}"
                                    else:
                                        current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
                                elif( r["fith_last_recognized_target"] == 4 ):
                                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                                elif( r["fith_last_recognized_target"] == 5 ):
                                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                                elif( r["fith_last_recognized_target"] == 6 ):
                                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                elif( r["fith_last_recognized_target"] == 7 ):
                                    current_track_condition = f"{st.session_state.track_snow_emoji}"
                                else:
# finaly give up... nobody should come to this point...
                                    if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                                        current_track_condition = f"{st.session_state.track_dry_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                                        current_track_condition = f"{st.session_state.track_wet_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                                        current_track_condition = f"{st.session_state.track_gravel_emoji}"
                                    elif(r["enter_data"]["track_condition"] == "drift_ice"):
                                        current_track_condition = f"{st.session_state.track_snow_emoji}"
                                    else:
                                        current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
# handle none here
            else:
                if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                    current_track_condition = f"{st.session_state.track_dry_emoji}"
                elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                    current_track_condition = f"{st.session_state.track_wet_emoji}"
                elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                    current_track_condition = f"{st.session_state.track_gravel_emoji}"
                elif(r["enter_data"]["track_condition"] == "drift_ice"):
                    current_track_condition = f"{st.session_state.track_snow_emoji}"
                else:
                    current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
# handle car in starting position here                                
        else:
            if(r["enter_data"]["track_condition"] == "drift_asphalt"):
                current_track_condition = f"{st.session_state.track_dry_emoji}"
            elif(r["enter_data"]["track_condition"] == "drift_asphalt_wet"):
                current_track_condition = f"{st.session_state.track_wet_emoji}"
            elif(r["enter_data"]["track_condition"] == "drift_dirt"):
                current_track_condition = f"{st.session_state.track_gravel_emoji}"
            elif(r["enter_data"]["track_condition"] == "drift_ice"):
                current_track_condition = f"{st.session_state.track_snow_emoji}"
            else:
                current_track_condition = f"{st.session_state.track_gravel_trap_emoji}"
    else: 
        current_track_condition = "-"
    return current_track_condition


# added function to handle awards after the race (Race: 1st, 2nd, 3rd and bonus award for fastest lap)
def get_minvalue(inputlist):
    #get the minimum value in the list
    min_value = min(inputlist)
    #return the index of minimum value 
    res = [i for i,val in enumerate(inputlist) if val==min_value]
    return res

# added function to handle awards after the gymkhana (Race: 1st, 2nd, 3rd and bonus award for highest bonus target)
def get_maxvalue(inputlist):
    #get the maximum value in the list
    max_value = max(inputlist)
    if max_value == 0:
        res = []
        return res
    #return the index of maximum value 
    res = [i for i,val in enumerate(inputlist) if val==max_value]
    return res

def app():   

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        color: white;
        height: 2em;
        width: 13em;
        border-radius:10px;
        font-size:15px;
        font-weight: bold;
        margin: auto;
    }

    div.stButton > button:active {
        position:relative;
        top:3px;
    }

    </style>""", unsafe_allow_html=True)

    lobby_id = st.session_state.lobby_id        
    game_id = st.session_state.game_id
    stage_id = st.session_state.stage_id
    num_stages = st.session_state.num_stages
        
    game_track_images_set = st.session_state.game_track_images_set
    game_track_images = st.session_state.game_track_images

#    hostname = socket.gethostname()
#    ip_address = socket.gethostbyname(hostname)
    
    st.header("Game Statistics of Event " + str(game_id) + " from Lobby " + str(lobby_id))

    games = []
    joker_lap_code = [None] * 20
    scoreboard = []
    track_image_upload = []
    track_image = []
    
    next_race = st.empty()
    placeholder1 = st.empty()
    placeholder2 = st.empty()

    with placeholder1.container():
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

        with col1:
            if st.button(f"Back {st.session_state.back_emoji}"):
                st.session_state.nextpage = "main_page"
                st.session_state.game_track_images_set = [False] * 20
                st.session_state.game_track_images = [None] * 20
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col2:
            if st.button(f"Start in 1 Min. {st.session_state.driving_emoji}"):
                result = fetch_get(f"{settings.driftapi_path}/driftapi/manage_game/start_stage/{lobby_id}/{game_id}/{stage_id}")
                st.session_state.new_stage_event = False
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col3:
            if st.button(f"Rem. Player (Stage) {st.session_state.remove_emoji}"):
                st.session_state.nextpage = "remove_player_from_stage_part1"
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col4:
            if st.button(f"Reset Stage {st.session_state.reset_emoji}"):
                st.session_state.nextpage = "reset_stage"
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col5:
            if st.button(f"Rem. Player (Event) {st.session_state.remove_emoji}"):
                st.session_state.nextpage = "remove_player_from_race"
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col6:
            if st.button(f"Reset Event {st.session_state.reset_emoji}"):
                result = fetch_get(f"{settings.driftapi_path}/driftapi/manage_game/reset/{lobby_id}/{game_id}/{stage_id}")
                st.session_state.new_stage_event = False
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col7:
            if st.button(f"Download Data {st.session_state.download_emoji}"):
                st.session_state.nextpage = "download_stagerace"
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col8:
            if st.button(f"Detailed Statistics {st.session_state.statistics_emoji}"):
                st.session_state.nextpage = "statistics_stage"
                st.session_state.game_track_images_set = game_track_images_set
                st.session_state.game_track_images = game_track_images
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

        with col9:
            if st.button(f"Delete Event {st.session_state.delete_emoji}"):
                result = fetch_delete(f"{settings.driftapi_path}/driftapi/manage_game/delete/{lobby_id}/{game_id}")
                st.session_state.game_id = None
                st.session_state.stage_id = 1
                st.session_state.num_stages = 1
                st.session_state.nextpage = "main_page"
                st.session_state.game_track_images_set = [False] * 20
                st.session_state.game_track_images = [None] * 20
                next_race.empty()
                placeholder1.empty()
                placeholder2.empty()
                time.sleep(0.1)
                st.experimental_rerun()

    with placeholder2.container():
        for x in range(num_stages):
            game = getGameInfo(lobby_id, game_id, x+1)
            if not game:
                st.error("No Game with that id exists, going back to main menu...")
                time.sleep(1)
                st.session_state.nextpage = "main_page"
                st.experimental_rerun()
            if game:
                with st.expander(f"Game Statistics of Sage " + str(x+1) + " - " + str(game["game_mode"]) + " - Join the game via URL: http://"+str(st.session_state.ip_address)+":8001/driftapi/game/"+str(lobby_id)+"/"+str(x+1)+" and GAME ID: "+str(game_id) + "   " + str(game["track_id"]) +  f"{st.session_state.show_game_emoji}", expanded = False):

                    track_image.append(st.empty())

                    track_image_upload.append(st.file_uploader("Here you can upload the track layout", type=['png', 'jpg'], accept_multiple_files=False, key="The track layout upload of " + str(x+1), help=None, on_change=None, args=None, kwargs=None, disabled=False))

                    if(game_track_images_set[x] == False): # no track image upload so far
                        if(track_image_upload[x] != None): # user has supplied a track image
                            game_track_images_set[x] = True
                            track_image[x] = st.image(track_image_upload[x], caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto") # Show Uploaded Track Image
                            game_track_images[x] = track_image_upload[x] # store in session state
                    elif(game_track_images_set[x] == True): # track image existing
                        if(track_image_upload[x] != None): # user has supplied a new track image
                            game_track_images_set[x] = True
                            track_image[x] = st.image(track_image_upload[x], caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto") # Show Uploaded Track Image
                            game_track_images[x] = track_image_upload[x] # store in session state
                        else:
                            track_image[x] = st.image(game_track_images[x], caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto") # Show Prev. Uploaded Track Image
                    if st.button(f"Remove Image {st.session_state.remove_emoji}", key="Remove Image "+str(x+1)):
                        track_image[x].empty()
                        game_track_images_set[x] = False

                    submitUri:str = "http://"+str(st.session_state.ip_address)+":8001/driftapi/game/"+str(lobby_id)+"/"+str(stage_id)+"/"
                    st.image(getqrcode(submitUri), clamp=True)
                    st.write("URL: "+submitUri)
                    st.write("GAME ID: "+game_id)

                    st.write(game)

                scoreboard.append(st.empty())
                if "joker_lap_code" in game:
                    joker_lap_code[x] = game["joker_lap_code"]   
            games.append(game)
 
    while True:

        # getting the info from one stage only is ok, since all stages have the same start_time
        game = getGameInfo(lobby_id, game_id, stage_id)
        current_time = datetime.now().astimezone(timezone.utc)
        if (st.session_state.new_stage_event == True):
            start_time = datetime.strptime(game["start_time"],'%Y-%m-%dT%H:%M:%S%z')
        else:
            try:
                start_time = datetime.strptime(game["start_time"],'%Y-%m-%d %H:%M:%S.%f%z')
            except:
                start_time = datetime.strptime(game["start_time"],'%Y-%m-%dT%H:%M:%S%z')
        time_delay = start_time - current_time
        if(current_time <= start_time):
            next_race.text("Stage starts in approx. " + str(time_delay))
        else:
            next_race.text("Time elapsed! Please press Button 'Start in 1 Min.' or 'Reset Event' and Sync. in Sturmkind App before entering a Stage")

        scoreboard_data = []
        scoreboard_len = []
        
        for x in range(num_stages):

            with scoreboard[x].container():
        
                scoreboard_data.append(getScoreBoard(lobby_id, game_id, x+1))
                
                # CSS to inject contained in a string
                hide_dataframe_row_index = """
                            <style>
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            </style>
                """
                # Inject CSS with Markdown
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
                        
                def constructEntry(r:dict):
                    d = {
                        "Spieler":r["user_name"] if "user_name" in r else "",
                    }
                            
# differentiate between RACE and GYMKHANA game mode:
                    if ( games[x]["game_mode"] == "RACE" ):
                    
# handle track_bundle:
                        if "enter_data" in r:
                            if( (r["enter_data"]["track_bundle"] == "rally_cross" ) ):
                                d["Kursmodus"] = "RALLY CROSS"
                            elif( (r["enter_data"]["track_bundle"] == "rally" ) ):
                                d["Kursmodus"] = "RALLY"
                            else:
                                d["Kursmodus"] = "KEINER"
                        else:
                            d["Kursmodus"] = "-"

# handle lap_count:
                        if "enter_data" in r:
                            d["Ges. Runden"] = r["enter_data"]["lap_count"]
                        else:
                            d["Ges. Runden"] = "-"

# handle laps_completed:
                        if "enter_data" in r:
                            d["Abg. Runden"] = r["laps_completed"]
                        else:
                            d["Abg. Runden"] = "-"

                        if joker_lap_code[x] != None:
                            d["Joker"] = int(r["joker_laps_counter"]) if "joker_laps_counter" in r else 0

# handle best_lap:
                        if "best_lap" in r:
                            d["Beste"] = showTime(r["best_lap"])
                        else:
                            d["Beste"] = showTime(None)

# handle last_lap:
                        if "last_lap" in r:
                            d["Letzte"] = showTime(r["last_lap"])
                        else:
                            d["Letzte"] = showTime(None)
                            
# handle total_time:
                        if "total_time" in r:
                            d["Gesamtzeit"] = showTime(r["total_time"])
                        else:
                            d["Gesamtzeit"] = showTime(None)

# handle total_driven_distance
                        if ( ( "end_data" in r ) and not ( r["end_data"] is None ) ):
                           d["Gesamtdistanz"] = showDistance(r["end_data"]["total_driven_distance"])
                        else:
                            d["Gesamtdistanz"] = ""               
                        
                        if ( ( "end_data" in r ) and not ( r["end_data"] is None ) ):
                            if(r["end_data"]["false_start"]):
                                d["Status"] = f"{st.session_state.false_start_emoji}" #"False Start!"
                                total_time_list.append(showTime(86400)) # fake 24h time
                                best_lap_list.append(showTime(86400)) # fake 24h time
                                shortest_distance_list.append(showDistance(9999999)) # fake 9999999 m
                            else:
                                d["Status"] = f"{st.session_state.finish_emoji}" #"Finished"
                                if(d["Ges. Runden"] == d["Abg. Runden"]):
                                    total_time_list.append(showTime(r["total_time"])) # real driven time
                                    best_lap_list.append(showTime(r["best_lap"])) # real best lap/target time
                                    shortest_distance_list.append(showDistance(r["end_data"]["total_driven_distance"])) # real total driven distance
                                else:
                                    total_time_list.append(showTime(86400)) # fake 24h time
                                    best_lap_list.append(showTime(86400)) # fake 24h time
                                    shortest_distance_list.append(showDistance(9999999)) # fake 9999999 m
                        elif ( ( "start_data" in r ) and not ( r["start_data"] is None ) ):
                            d["Status"] = f"{st.session_state.driving_emoji}" #"Driving"
                        elif "enter_data" in r:
                            d["Status"] = f"{st.session_state.ready_emoji}" #"Ready"
                        else:
                            d["Status"] = ""

                    elif ( games[x]["game_mode"] == "GYMKHANA" ):
                        display_text_speed = f"Bester Speed"
                        display_text_angle = f"Bester Angle"
                        display_text_360 = f"Bester 360"
                        display_text_180 = f"Bester 180"
# handle bonus target set:
                        if ( "bonus_target" in games[x] ) and (not games[x]["bonus_target"] is None):
                            if ( games[x]["bonus_target"] == "SPEED" ):
                                display_text_speed = display_text_speed + f" ({st.session_state.award_trophy_emoji})"
                            elif ( games[x]["bonus_target"] == "ANGLE" ):
                                display_text_angle = display_text_angle + f" ({st.session_state.award_trophy_emoji})"
                            elif ( games[x]["bonus_target"] == "360" ):
                                display_text_360 = display_text_360 + f" ({st.session_state.award_trophy_emoji})"
                            elif ( games[x]["bonus_target"] == "180" ):
                                display_text_180 = display_text_180 + f" ({st.session_state.award_trophy_emoji})"
                        else:
                            display_text_360 = display_text_360 + f" ({st.session_state.award_trophy_emoji})"

                        if ("best_speed_drift" in r) and (not (r["best_speed_drift"] is None)):
                            d[display_text_speed] = int(r["best_speed_drift"])
                        else:
                            d[display_text_speed] = 0

                        if ("best_angle_drift" in r) and (not (r["best_angle_drift"] is None)):
                            d[display_text_angle] = int(r["best_angle_drift"])
                        else:
                            d[display_text_angle] = 0

                        if ("best_360_angle" in r) and (not (r["best_360_angle"] is None)):
                            d[display_text_360] = int(r["best_360_angle"])
                        else:
                            d[display_text_360] = 0                   
                        
                        if ("best_180_speed" in r) and (not (r["best_180_speed"] is None)):
                            d[display_text_180] = int(r["best_180_speed"])
                        else:
                            d[display_text_180] = 0  
# handle total_score:
                        if ("total_score" in r) and (not (r["total_score"] is None)):
                            d["Gesamtpunkte"] = int(r["total_score"])
                        else:
                            d["Gesamtpunkte"] = 0
                        if ( ( "end_data" in r ) and not ( r["end_data"] is None ) ):
                        
                            if ( "bonus_target" in games[x] ) and (not games[x]["bonus_target"] is None):
                                if ( games[x]["bonus_target"] == "SPEED" ):
                                    if (not r["best_speed_drift"] is None):
                                        best_target_set = int(r["best_speed_drift"])
                                    else:
                                        best_target_set = 0
                                elif ( games[x]["bonus_target"] == "ANGLE" ):
                                    if (not r["best_angle_drift"] is None):
                                        best_target_set = int(r["best_angle_drift"])
                                    else:
                                        best_target_set = 0
                                elif ( games[x]["bonus_target"] == "360" ):
                                    if (not r["best_360_angle"] is None):
                                        best_target_set = int(r["best_360_angle"])
                                    else:
                                        best_target_set = 0
                                elif ( games[x]["bonus_target"] == "180" ):
                                    if (not r["best_180_speed"] is None):
                                        best_target_set = int(r["best_180_speed"])
                                    else:
                                        best_target_set = 0
                            else:
                                if (not r["best_360_angle"] is None):
                                    best_target_set = int(r["best_360_angle"]) # default
                                else:
                                    best_target_set = 0
                            
                            if(r["end_data"]["false_start"]):
                                d["Status"] = f"{st.session_state.false_start_emoji}" #"False Start!"
                                total_score_list.append(int(r["total_score"]))
                                best_target_list.append(best_target_set) # best_target_set, default is 360
                                shortest_distance_list.append(showDistance(r["end_data"]["total_driven_distance"])) # real total driven distance
                            else:
                                d["Status"] = f"{st.session_state.finish_emoji}" #"Finished"
                                total_score_list.append(int(r["total_score"]))
                                best_target_list.append(best_target_set) # best_target_set, default is 360
                                shortest_distance_list.append(showDistance(r["end_data"]["total_driven_distance"])) # real total driven distance
                        elif ( ( "start_data" in r ) and not ( r["start_data"] is None ) ):
                            d["Status"] = f"{st.session_state.driving_emoji}" #"Driving"
                        elif "enter_data" in r:
                            d["Status"] = f"{st.session_state.ready_emoji}" #"Ready"
                        else:
                            d["Status"] = ""

    # handle engine
                    if "enter_data" in r:
                        d["Motor"] = r["enter_data"]["engine_type"]
                    else:
                        d["Motor"] = "-"

    # handle tuning
                    if "enter_data" in r:
                        d["Tuning"] = r["enter_data"]["tuning_type"]
                    else:
                        d["Tuning"] = "-"
               
    # handle game_mode:
                    if "enter_data" in r:
                        d["Modus"] = r["enter_data"]["game_mode"]
                    else:
                        d["Modus"] = "-"

    # handle setup_mode:
                    if "enter_data" in r:
                        d["Setup"] = r["enter_data"]["setup_mode"]
                    else:
                        d["Setup"] = "-"

    # handle wheels
                    if "enter_data" in r:
                        if( (r["enter_data"]["wheels"] == "spikes" ) ):
                            d["Reifen"] = "SPIKES"
                        elif( (r["enter_data"]["wheels"] == "gravel_tires" ) ):
                            d["Reifen"] = "RALLY"
                        else:
                            d["Reifen"] = "STRAßE"
                    else:
                        d["Reifen"] = "-"

                    return (d)

# handle awards after the race (Race: 1st, 2nd, 3rd and bonus award for fastest lap)

                total_time_list = []
                best_lap_list = []
                total_score_list = []
                best_target_list = []
                shortest_distance_list = []
                (scoreboard_data[x]) = [constructEntry(r) for r in scoreboard_data[x] if (type(r) is dict)] # we have to handle up to 10 scoreboards

                #if there is no entry, just add an empty one by calling the construct Entry with an empty dict
                while len(scoreboard_data[x])<1:
                    scoreboard_data[x].append(constructEntry({}))

                scoreboard_len.append(len(scoreboard_data[x]))
                
                if(len(total_time_list) == scoreboard_len[x]): # all players finished race    
                    min_total_time_indices_list = get_minvalue(total_time_list)
                    min_total_time_indices_list_len = len(min_total_time_indices_list)
# handle normal case: one player on 1st place
                    for y in min_total_time_indices_list:
                        if( (total_time_list[y] != "1440:00.000") ):
                            scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_1st_emoji}"
                            total_time_list[y] = showTime(172800)  # fake 48h time - meaning player has been handled
                        else:
                            scoreboard_data[x][y]["Platz"] = "-"
# cont. handle normal case: one player on 2nd place as well as special case more players on 2nd place
                    if min_total_time_indices_list_len == 1:
                        min_total_time_indices_list = get_minvalue(total_time_list)
                        min_total_time_indices_list_len = len(min_total_time_indices_list)
                        for y in min_total_time_indices_list:
                            if( (total_time_list[y] != "2880:00.000") ):
                                if( (total_time_list[y] == "1440:00.000") ):
                                    scoreboard_data[x][y]["Platz"] = "-"
                                else:
                                    scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_2nd_emoji}"
                                    total_time_list[y] = showTime(172800)  # fake 48h time - meaning player has been handled
# cont. handle normal case: one player on 3rd place as well as special case more players on 3rd place
                        if min_total_time_indices_list_len == 1:
                            min_total_time_indices_list = get_minvalue(total_time_list)
                            min_total_time_indices_list_len = len(min_total_time_indices_list)
                            for y in min_total_time_indices_list:
                                if( (total_time_list[y] != "2880:00.000") ):
                                    if( (total_time_list[y] == "1440:00.000") ):
                                        scoreboard_data[x][y]["Platz"] = "-"
                                    else:
                                        scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_3rd_emoji}"
                                        total_time_list[y] = showTime(172800)  # fake 48h time
# handle special case: two players on 1st place as well as special case more players on 3rd place                                   
                    elif min_total_time_indices_list_len == 2:
                        min_total_time_indices_list = get_minvalue(total_time_list)
                        min_total_time_indices_list_len = len(min_total_time_indices_list)
                        for y in min_total_time_indices_list:
                            if( (total_time_list[y] != "2880:00.000") ):
                                if( (total_time_list[y] == "1440:00.000") ):
                                    scoreboard_data[x][y]["Platz"] = "-"
                                else:
                                    scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_3rd_emoji}"
                                    total_time_list[y] = showTime(172800)  # fake 48h time

# award for best lap / best bonus target score                        
                if(len(best_lap_list) == scoreboard_len[x]): # all players finished race
                    min_best_lap_indices_list = get_minvalue(best_lap_list)
                    for y in range(len(best_lap_list)):
                        if y in min_best_lap_indices_list:
                            if( (best_lap_list[y] != "1440:00.000") ):
                                scoreboard_data[x][y]["Beste Runde"] = f"{st.session_state.award_bonus_emoji}"
                            else:
                                scoreboard_data[x][y]["Beste Runde"] = "-"
                        else:
                            scoreboard_data[x][y]["Beste Runde"] = "-"

                if(len(total_score_list) == scoreboard_len[x]): # all players finished race    
                    max_total_score_indices_list = get_maxvalue(total_score_list)
                    max_total_score_indices_list_len = len(max_total_score_indices_list)
# handle normal case: one player on 1st place
                    for y in max_total_score_indices_list:
                        scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_1st_emoji}"
                        total_score_list[y] = 0  # fake 0 score - meaning player has been handled
# cont. handle normal case: one player on 2nd place as well as special case more players on 2nd place
                    if max_total_score_indices_list_len == 1:
                        max_total_score_indices_list = get_maxvalue(total_score_list)
                        max_total_score_indices_list_len = len(max_total_score_indices_list)
                        for y in max_total_score_indices_list:
                            scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_2nd_emoji}"
                            total_score_list[y] = 0  # fake 0 score - meaning player has been handled
# cont. handle normal case: one player on 3rd place as well as special case more players on 3rd place
                    if max_total_score_indices_list_len == 1:
                        max_total_score_indices_list = get_maxvalue(total_score_list)
                        max_total_score_indices_list_len = len(max_total_score_indices_list)
                        for y in max_total_score_indices_list:
                            scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_3rd_emoji}"
                            total_score_list[y] = 0  # fake 0 score - meaning player has been handled
# handle special case: two players on 1st place as well as special case more players on 3rd place                                   
                    elif max_total_score_indices_list_len == 2:
                        max_total_score_indices_list = get_maxvalue(total_score_list)
                        max_total_score_indices_list_len = len(max_total_score_indices_list)
                        for y in max_total_score_indices_list:
                            scoreboard_data[x][y]["Platz"] = f"{st.session_state.award_3rd_emoji}"
                            total_score_list[y] = 0  # fake 0 score - meaning player has been handled

                if(len(best_target_list) == scoreboard_len[x]): # all players finished race
                    max_best_target_indices_list = get_maxvalue(best_target_list)
                    for y in range(len(best_target_list)):
                        if y in max_best_target_indices_list:
                            scoreboard_data[x][y]["Bonus Target"] = f"{st.session_state.award_bonus_emoji}"
                        else:
                            scoreboard_data[x][y]["Bonus Target"] = "-"

# award for shortest distance                        
                if(len(shortest_distance_list) == scoreboard_len[x]): # all players finished race
                    min_shortest_distance_list_indices_list = get_minvalue(shortest_distance_list)
                    for y in range(len(shortest_distance_list)):
                        if y in min_shortest_distance_list_indices_list:
                            if( (shortest_distance_list[y] != "9999km 999m") ):
                                scoreboard_data[x][y]["Kürzeste Strecke"] = f"{st.session_state.award_bonus_emoji}"
                            else:
                                scoreboard_data[x][y]["Kürzeste Strecke"] = "-"
                        else:
                            scoreboard_data[x][y]["Kürzeste Strecke"] = "-"

                df = pd.DataFrame( scoreboard_data[x] )
                
#                st.dataframe(df)
                st.table(df)
                #st.dataframe(df, width=1600, height = 20*len(scoreboard_data))

        time.sleep(0.5)
