BOT_TOKEN: str = ""
SPOTIFY_ID: str = ""
SPOTIFY_SECRET: str = ""

BOT_PREFIX = "$"

EMBED_COLOR = 0x4dd4d0  #replace after'0x' with desired hex code ex. '#ff0188' >> '0xff0188'

SUPPORTED_EXTENSIONS = ('.webm', '.mp4', '.mp3', '.avi', '.wav', '.m4v', '.ogg', '.mov')

MAX_SONG_PRELOAD = 5  #maximum of 25

COOKIE_PATH = "/config/cookies/cookies.txt"

GLOBAL_DISABLE_AUTOJOIN_VC = False

VC_TIMEOUT = 600 #seconds
VC_TIMOUT_DEFAULT = True  #default template setting for VC timeout true= yes, timeout false= no timeout
ALLOW_VC_TIMEOUT_EDIT = True  #allow or disallow editing the vc_timeout guild setting


STARTUP_MESSAGE = "Starting Bot..."
STARTUP_COMPLETE_MESSAGE = "Startup Complete"

NO_GUILD_MESSAGE = 'Error: Please join a voice channel or enter the command in guild chat'
USER_NOT_IN_VC_MESSAGE = "Error: Please join the active voice channel to use commands"
WRONG_CHANNEL_MESSAGE = "Error: Please use configured command channel"
NOT_CONNECTED_MESSAGE = "Error: Bot not connected to any voice channel"
ALREADY_CONNECTED_MESSAGE = "Error: Already connected to a voice channel"
CHANNEL_NOT_FOUND_MESSAGE = "Error: Could not find channel"
DEFAULT_CHANNEL_JOIN_FAILED = "Error: Could not join the default voice channel"
INVALID_INVITE_MESSAGE = "Error: Invalid invitation link"

ADD_MESSAGE= "To add this bot to your own Server, click [here]" #brackets will be the link text

INFO_HISTORY_TITLE = "Songs Played:"
MAX_HISTORY_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Likes: "
SONGINFO_DISLIKES = "Dislikes: "
SONGINFO_NOW_PLAYING = "Now Playing"
SONGINFO_QUEUE_ADDED = "Added to queue"
SONGINFO_SONGINFO = "Song info"
SONGINFO_ERROR = "Error: Unsupported site or age restricted content. To enable age restricted content check the documentation/wiki."
SONGINFO_PLAYLIST_QUEUED = "Queued playlist :page_with_curl:"
SONGINFO_UNKNOWN_DURATION = "Unknown"

DESCRIPTION_ADDBOT_SHORT = "Add Bot to another server"
DESCRIPTION_ADDBOT = "Gives you the link for adding this bot to another server of yours."
DESCRIPTION_CONNECT_SHORT = "Connect bot to voicechannel"
DESCRIPTION_CONNECT = "Connects the bot to the voice channel you are currently in"
DESCRIPTION_DISCONNECT_SHORT = "Disonnect bot from voicechannel"
DESCRIPTION_DISCONNECT = "Disconnect the bot from the voice channel and stop audio."

DESCRIPTION_SETTINGS_SHORT = "View and set bot settings"
DESCRIPTION_SETTINGS = "View and set bot settings in the server. Usage: {}settings setting_name value".format(BOT_PREFIX)

DESCRIPTION_HISTORY_SHORT = "Show history of songs"
DESCRIPTION_HISTORY = "Shows the " + str(MAX_TRACKNAME_HISTORY_LENGTH) + " last played songs."
DESCRIPTION_PAUSE_SHORT = "Pause Music"
DESCRIPTION_PAUSE = "Pauses the AudioPlayer. Playback can be continued with the resume command."
DESCRIPTION_VOL_SHORT = "Change volume %"
DESCRIPTION_VOL = "Changes the volume of the AudioPlayer. Argument specifies the % to which the volume should be set."
DESCRIPTION_PREV_SHORT = "Go back one Song"
DESCRIPTION_PREV = "Plays the previous song again."
DESCRIPTION_RESUME_SHORT = "Resume Music"
DESCRIPTION_RESUME = "Resumes the AudioPlayer."
DESCRIPTION_SKIP_SHORT = "Skip a song"
DESCRIPTION_SKIP = "Skips the currently playing song and goes to the next item in the queue."
DESCRIPTION_SONGINFO_SHORT = "Info about current Song"
DESCRIPTION_SONGINFO = "Shows details about the song currently being played and posts a link to the song."
DESCRIPTION_STOP_SHORT = "Stop Music"
DESCRIPTION_STOP = "Stops the AudioPlayer and clears the songqueue"
DESCRIPTION_MOVE = f"{BOT_PREFIX}move [position] [new position]"
DESCRIPTION_MOVE_SHORT = 'Moves a track in the queue'
DESCRIPTION_YT_SHORT = "Play a supported link or search on youtube"
DESCRIPTION_YT = ("/[video title / playlist/soundcloud/spotify/bandcamp/twitter link]")
DESCRIPTION_PING_SHORT = "Pong"
DESCRIPTION_PING = "Test bot response status"
DESCRIPTION_CLEAR_SHORT = "Clear the queue."
DESCRIPTION_CLEAR = "Clears the queue and skips the current song."
DESCRIPTION_LOOP_SHORT = "Loops the currently playing song, toggle on/off."
DESCRIPTION_LOOP = "Loops the currently playing song and locks the queue. Use the command again to disable loop."
DESCRIPTION_QUEUE_SHORT = "Shows the songs in queue."
DESCRIPTION_QUEUE = "Shows the number of songs in queue, up to 10."
DESCRIPTION_SHUFFLE_SHORT = "Shuffle the queue"
DESCRIPTION_SHUFFLE = "Randomly sort the songs in the current queue"
DESCRIPTION_CHANGECHANNEL_SHORT = "Change the bot channel"
DESCRIPTION_CHANGECHANNEL = "Change the bot channel to the VC you are in"

ABSOLUTE_PATH = '' #do not modify