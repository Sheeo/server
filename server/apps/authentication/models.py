# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.contrib.auth.models import UserManager
from django.db import models


class Login(models.Model):
    """
    Represents user accounts on FAF
    """
    login = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=64)
    email = models.CharField(unique=True, max_length=64)
    ip = models.CharField(max_length=15, blank=True)

    # Field name made lowercase.
    unique_id = models.CharField(db_column='uniqueId', unique=True, max_length=45, blank=True)
    session = models.IntegerField()
    validated = models.IntegerField()
    steam_id = models.BigIntegerField(db_column='steamid', unique=True, blank=True, null=True)
    steam_checked = models.IntegerField(db_column="steamchecked")

    # Field name made lowercase.
    ladder_cancelled = models.IntegerField(db_column='ladderCancelled')

    # Added for compatibility with the django usermanager
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateField()
    date_joined = models.DateField()

    objects = UserManager()

    def get_full_name(self):
        return self.login

    def get_short_name(self):
        return self.login

    REQUIRED_FIELDS = ('password', 'email')
    USERNAME_FIELD = 'login'

    class Meta:
        db_table = 'login'


class NameHistory(models.Model):
    """
    History of name changes
    """
    change_time = models.DateTimeField()
    user = models.ForeignKey(Login)
    previous_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'name_history'




# Below is the output from manage.py inspectdb
#class AiNames(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    login = models.CharField(unique=True, max_length=60)
#
#    class Meta:
#        managed = False
#        db_table = 'ai_names'
#
#
#class AiRating(models.Model):
#    id = models.ForeignKey(AiNames, db_column='id', primary_key=True)
#    mean = models.FloatField(blank=True, null=True)
#    deviation = models.FloatField(blank=True, null=True)
#    numgames = models.IntegerField(db_column='numGames')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'ai_rating'
#
#
#class AuthGroup(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(unique=True, max_length=80)
#
#    class Meta:
#        managed = False
#        db_table = 'auth_group'
#
#
#class AuthGroupPermissions(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    group_id = models.IntegerField()
#    permission_id = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'auth_group_permissions'
#
#
#class AuthPermission(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(max_length=50)
#    content_type_id = models.IntegerField()
#    codename = models.CharField(max_length=100)
#
#    class Meta:
#        managed = False
#        db_table = 'auth_permission'
#
#
#class AuthUser(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    username = models.CharField(unique=True, max_length=30)
#    first_name = models.CharField(max_length=30)
#    last_name = models.CharField(max_length=30)
#    email = models.CharField(max_length=75)
#    password = models.CharField(max_length=128)
#    is_staff = models.IntegerField()
#    is_active = models.IntegerField()
#    is_superuser = models.IntegerField()
#    last_login = models.DateTimeField()
#    date_joined = models.DateTimeField()
#
#    class Meta:
#        managed = False
#        db_table = 'auth_user'
#
#
#class AuthUserGroups(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    user_id = models.IntegerField()
#    group_id = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'auth_user_groups'
#
#
#class AuthUserUserPermissions(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    user_id = models.IntegerField()
#    permission_id = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'auth_user_user_permissions'
#
#
#class Avatars(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.ForeignKey('Login', db_column='idUser')  # Field name made lowercase.
#    idavatar = models.ForeignKey('AvatarsList', db_column='idAvatar')  # Field name made lowercase.
#    selected = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'avatars'
#
#
#class AvatarsList(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    url = models.CharField(max_length=255)
#    tooltip = models.CharField(max_length=50, blank=True)
#
#    class Meta:
#        managed = False
#        db_table = 'avatars_list'
#
#
#class Bet(models.Model):
#    userid = models.IntegerField(primary_key=True)
#    amount = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'bet'
#
#
#class CoopLeaderboard(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    mission = models.IntegerField()
#    gameuid = models.BigIntegerField(unique=True)
#    secondary = models.IntegerField()
#    time = models.TimeField()
#
#    class Meta:
#        managed = False
#        db_table = 'coop_leaderboard'
#
#
#class CoopMap(models.Model):
#    type = models.IntegerField()
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(max_length=40, blank=True)
#    description = models.TextField(blank=True)
#    version = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
#    filename = models.CharField(max_length=200, blank=True)
#
#    class Meta:
#        managed = False
#        db_table = 'coop_map'
#
#
#class FeaturedModsOwners(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    uid = models.ForeignKey('Login', db_column='uid')
#    moduid = models.ForeignKey('GameFeaturedmods', db_column='moduid')
#
#    class Meta:
#        managed = False
#        db_table = 'featured_mods_owners'
#
#
#class Foes(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.ForeignKey('Login', db_column='idUser')  # Field name made lowercase.
#    idfoe = models.ForeignKey('Login', db_column='idFoe')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'foes'
#
#
#class Friends(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.ForeignKey('Login', db_column='idUser')  # Field name made lowercase.
#    idfriend = models.ForeignKey('Login', db_column='idFriend')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'friends'
#
#
#class GameFeaturedmods(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    gamemod = models.CharField(max_length=50, blank=True)
#    description = models.TextField()
#    name = models.CharField(max_length=255)
#    publish = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'game_featuredmods'
#
#
#class GameMinRating(models.Model):
#    id = models.ForeignKey('GameStatsBak', db_column='id', primary_key=True)
#    minrating = models.FloatField(db_column='minRating', blank=True, null=True)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'game_min_rating'
#
#
#class GamePlayerStats(models.Model):
#    id = models.BigIntegerField(primary_key=True)
#    gameid = models.BigIntegerField(db_column='gameId')  # Field name made lowercase.
#    playerid = models.IntegerField(db_column='playerId')  # Field name made lowercase.
#    ai = models.IntegerField(db_column='AI')  # Field name made lowercase.
#    faction = models.IntegerField()
#    color = models.IntegerField()
#    team = models.IntegerField()
#    place = models.IntegerField()
#    mean = models.FloatField()
#    deviation = models.FloatField()
#    after_mean = models.FloatField(blank=True, null=True)
#    after_deviation = models.FloatField(blank=True, null=True)
#    score = models.IntegerField()
#    scoretime = models.DateTimeField(db_column='scoreTime', blank=True, null=True)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'game_player_stats'
#
#
#class GamePlayerStatsBak(models.Model):
#    id = models.BigIntegerField(primary_key=True)
#    gameid = models.ForeignKey('GameStatsBak', db_column='gameId')  # Field name made lowercase.
#    playerid = models.ForeignKey('Login', db_column='playerId')  # Field name made lowercase.
#    ai = models.IntegerField(db_column='AI')  # Field name made lowercase.
#    faction = models.IntegerField()
#    color = models.IntegerField()
#    team = models.IntegerField()
#    place = models.IntegerField()
#    mean = models.FloatField()
#    deviation = models.FloatField()
#    after_mean = models.FloatField(blank=True, null=True)
#    after_deviation = models.FloatField(blank=True, null=True)
#    score = models.IntegerField()
#    scoretime = models.DateTimeField(db_column='scoreTime', blank=True, null=True)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'game_player_stats_bak'
#
#
#class GameReplays(models.Model):
#    uid = models.BigIntegerField(db_column='UID', primary_key=True)  # Field name made lowercase.
#    file = models.TextField()
#
#    class Meta:
#        managed = False
#        db_table = 'game_replays'
#
#
#class GameReplaysOld(models.Model):
#    uid = models.ForeignKey('GameStatsBak', db_column='UID', primary_key=True)  # Field name made lowercase.
#    file = models.TextField()
#
#    class Meta:
#        managed = False
#        db_table = 'game_replays_old'
#
#
#class GameStats(models.Model):
#    id = models.BigIntegerField(primary_key=True)
#    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
#    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
#    gametype = models.CharField(db_column='gameType', max_length=1, blank=True)  # Field name made lowercase.
#    gamemod = models.IntegerField(db_column='gameMod', blank=True, null=True)  # Field name made lowercase.
#    host = models.IntegerField(blank=True, null=True)
#    mapid = models.IntegerField(db_column='mapId', blank=True, null=True)  # Field name made lowercase.
#    gamename = models.TextField(db_column='gameName', blank=True)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'game_stats'
#
#
#class GameStatsBak(models.Model):
#    id = models.BigIntegerField(primary_key=True)
#    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
#    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
#    gametype = models.CharField(db_column='gameType', max_length=1, blank=True)  # Field name made lowercase.
#    gamemod = models.ForeignKey(GameFeaturedmods, db_column='gameMod', blank=True, null=True)  # Field name made lowercase.
#    host = models.ForeignKey('Login', db_column='host', blank=True, null=True)
#    mapid = models.ForeignKey('TableMap', db_column='mapId', blank=True, null=True)  # Field name made lowercase.
#    gamename = models.TextField(db_column='gameName', blank=True)  # Field name made lowercase.
#    valid = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'game_stats_bak'
#
#
#class GlobalRating(models.Model):
#    id = models.ForeignKey('Login', db_column='id', primary_key=True)
#    mean = models.FloatField(blank=True, null=True)
#    deviation = models.FloatField(blank=True, null=True)
#    numgames = models.IntegerField(db_column='numGames')  # Field name made lowercase.
#    is_active = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'global_rating'
#
#
#class Ladder1V1Rating(models.Model):
#    id = models.ForeignKey('Login', db_column='id', primary_key=True)
#    mean = models.FloatField(blank=True, null=True)
#    deviation = models.FloatField(blank=True, null=True)
#    numgames = models.IntegerField(db_column='numGames')  # Field name made lowercase.
#    wingames = models.IntegerField(db_column='winGames')  # Field name made lowercase.
#    is_active = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder1v1_rating'
#
#
#class LadderDivision(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(unique=True, max_length=255)
#    league = models.IntegerField()
#    limit = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_division'
#
#
#class LadderDivisions(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(unique=True, max_length=255)
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_divisions'
#
#
#class LadderMap(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    idmap = models.ForeignKey('TableMap', db_column='idmap', unique=True)
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_map'
#
#
#class LadderMapSelection(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser')  # Field name made lowercase.
#    idmap = models.IntegerField(db_column='idMap')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_map_selection'
#
#
#class LadderSeason1(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser', unique=True)  # Field name made lowercase.
#    league = models.IntegerField()
#    division = models.IntegerField()
#    score = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_season_1'
#
#
#class LadderSeason2(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser', unique=True)  # Field name made lowercase.
#    league = models.IntegerField()
#    division = models.IntegerField()
#    score = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_season_2'
#
#
#class LadderSeason3(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser', unique=True)  # Field name made lowercase.
#    league = models.IntegerField()
#    division = models.IntegerField()
#    score = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_season_3'
#
#
#class LadderSeason3Safe(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser', unique=True)  # Field name made lowercase.
#    league = models.IntegerField()
#    division = models.IntegerField()
#    score = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_season_3_safe'
#
#
#class LadderSeason4(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser', unique=True)  # Field name made lowercase.
#    league = models.IntegerField()
#    division = models.IntegerField()
#    score = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_season_4'
#
#
#class LadderSeason5(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    iduser = models.IntegerField(db_column='idUser', unique=True)  # Field name made lowercase.
#    league = models.IntegerField()
#    score = models.FloatField()
#
#    class Meta:
#        managed = False
#        db_table = 'ladder_season_5'
#
#
#class LobbyAdmin(models.Model):
#    user_id = models.IntegerField(primary_key=True)
#    group = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'lobby_admin'
#
#
#class LobbyBan(models.Model):
#    iduser = models.ForeignKey('Login', db_column='idUser', unique=True, blank=True, null=True)  # Field name made lowercase.
#    reason = models.CharField(max_length=255)
#
#    class Meta:
#        managed = False
#        db_table = 'lobby_ban'
#
#
#
#
#class MatchmakerBan(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    userid = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'matchmaker_ban'
#
#
#
#
#class NomadsBeta(models.Model):
#    iduser = models.ForeignKey(Login, db_column='idUser', unique=True, blank=True, null=True)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'nomads_beta'
#
#
#class PatchsTable(models.Model):
#    idpatchs_table = models.IntegerField(primary_key=True)
#    frommd5 = models.CharField(db_column='fromMd5', max_length=45, blank=True)  # Field name made lowercase.
#    tomd5 = models.CharField(db_column='toMd5', max_length=45, blank=True)  # Field name made lowercase.
#    patchfile = models.CharField(db_column='patchFile', max_length=200, blank=True)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'patchs_table'
#
#
#class RecoveryemailsEnc(models.Model):
#    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#    userid = models.ForeignKey(Login, db_column='UserID')  # Field name made lowercase.
#    key = models.CharField(db_column='Key', max_length=32)  # Field name made lowercase.
#    expdate = models.DateTimeField(db_column='expDate')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'recoveryemails_enc'
#
#
#class ReplayComment(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    user = models.ForeignKey(Login)
#    replay = models.ForeignKey('SubmittedReplays')
#    text = models.TextField()
#    timestamp = models.DateTimeField()
#
#    class Meta:
#        managed = False
#        db_table = 'replay_comment'
#
#
#class ReplayReview(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    submitted_replay = models.ForeignKey('SubmittedReplays')
#    user = models.ForeignKey(Login)
#    type = models.CharField(max_length=255)
#    body = models.TextField()
#
#    class Meta:
#        managed = False
#        db_table = 'replay_review'
#
#
#class ReplayVault(models.Model):
#    id = models.BigIntegerField()
#    gamename = models.TextField(db_column='gameName', blank=True)  # Field name made lowercase.
#    filename = models.CharField(max_length=200, blank=True)
#    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
#    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
#    gamemod = models.CharField(max_length=50, blank=True)
#    playerid = models.IntegerField(db_column='playerId')  # Field name made lowercase.
#    mapid = models.IntegerField(db_column='mapId', blank=True, null=True)  # Field name made lowercase.
#    rating = models.FloatField()
#    gamemodid = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        managed = False
#        db_table = 'replay_vault'
#
#
#class SearchPlayer(models.Model):
#    id = models.BigIntegerField()
#    playerid = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'search_player'
#
#
#class SmurfTable(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    origid = models.ForeignKey(Login, db_column='origId')  # Field name made lowercase.
#    smurfid = models.ForeignKey(Login, db_column='smurfId')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'smurf_table'
#
#
#class SteamLinkRequest(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    uid = models.IntegerField()
#    key = models.CharField(db_column='Key', max_length=32)  # Field name made lowercase.
#    expdate = models.DateTimeField(db_column='expDate')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'steam_link_request'
#
#
#class SteamUniqueid(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    uniqueid = models.CharField(unique=True, max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'steam_uniqueid'
#
#
#class SubmittedReplays(models.Model):
#    game = models.ForeignKey(GameStatsBak, primary_key=True)
#    featured_by = models.ForeignKey(Login, db_column='featured_by', blank=True, null=True)
#    experted_by = models.ForeignKey(Login, db_column='experted_by', blank=True, null=True)
#    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
#    votes = models.IntegerField()
#    voters = models.TextField(blank=True)
#    reserved_by = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        managed = False
#        db_table = 'submitted_replays'
#
#
#class SwissTournaments(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(max_length=100)
#    host = models.ForeignKey(Login, db_column='host', blank=True, null=True)
#    description = models.CharField(max_length=500, blank=True)
#    minplayers = models.IntegerField(blank=True, null=True)
#    maxplayers = models.IntegerField(blank=True, null=True)
#    minrating = models.IntegerField(blank=True, null=True)
#    maxrating = models.IntegerField(blank=True, null=True)
#    tourney_date = models.DateTimeField(blank=True, null=True)
#    tourney_state = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        managed = False
#        db_table = 'swiss_tournaments'
#
#
#class SwissTournamentsPlayers(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    idtourney = models.ForeignKey(SwissTournaments, db_column='idtourney')
#    iduser = models.ForeignKey(Login, db_column='iduser')
#
#    class Meta:
#        managed = False
#        db_table = 'swiss_tournaments_players'
#
#
#class TableMap(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    name = models.CharField(max_length=40, blank=True)
#    description = models.TextField(blank=True)
#    max_players = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
#    map_type = models.CharField(max_length=15, blank=True)
#    battle_type = models.CharField(max_length=15, blank=True)
#    map_sizex = models.DecimalField(db_column='map_sizeX', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#    map_sizey = models.DecimalField(db_column='map_sizeY', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#    version = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
#    filename = models.CharField(max_length=200, blank=True)
#    hidden = models.IntegerField()
#    mapuid = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'table_map'
#
#
#class TableMapBroken(models.Model):
#    broken_id = models.IntegerField(primary_key=True)
#    map = models.ForeignKey(TableMap)
#    description = models.TextField()
#    user = models.ForeignKey(Login, blank=True, null=True)
#    approved = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'table_map_broken'
#
#
#class TableMapComments(models.Model):
#    comment_id = models.IntegerField(primary_key=True)
#    map = models.ForeignKey(TableMap)
#    user = models.ForeignKey(Login)
#    comment_text = models.TextField()
#    comment_date = models.DateTimeField()
#
#    class Meta:
#        managed = False
#        db_table = 'table_map_comments'
#
#
#class TableMapFeatures(models.Model):
#    map = models.ForeignKey(TableMap, primary_key=True)
#    rating = models.FloatField()
#    voters = models.TextField()
#    downloads = models.IntegerField()
#    times_played = models.IntegerField()
#    num_draws = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'table_map_features'
#
#
#class TableMapUnranked(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#
#    class Meta:
#        managed = False
#        db_table = 'table_map_unranked'
#
#
#class TableMapUploaders(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    mapid = models.ForeignKey(TableMap, db_column='mapid', unique=True)
#    userid = models.ForeignKey(Login, db_column='userid')
#
#    class Meta:
#        managed = False
#        db_table = 'table_map_uploaders'
#
#
#class TableMod(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    uid = models.CharField(unique=True, max_length=40)
#    name = models.CharField(max_length=255)
#    version = models.IntegerField()
#    author = models.CharField(max_length=100)
#    ui = models.IntegerField()
#    big = models.IntegerField()
#    small = models.IntegerField()
#    date = models.DateTimeField()
#    downloads = models.IntegerField()
#    likes = models.IntegerField()
#    played = models.IntegerField()
#    description = models.CharField(max_length=255)
#    filename = models.CharField(max_length=255)
#    icon = models.CharField(max_length=255)
#    likers = models.TextField()
#    ranked = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'table_mod'
#
#
#class Test(models.Model):
#    id = models.IntegerField()
#    file = models.TextField()
#
#    class Meta:
#        managed = False
#        db_table = 'test'
#
#
#class Test2(models.Model):
#    id = models.IntegerField()
#    test = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'test2'
#
#
#class TestGameReplays(models.Model):
#    uid = models.BigIntegerField(db_column='UID', primary_key=True)  # Field name made lowercase.
#    file = models.TextField()
#
#    class Meta:
#        managed = False
#        db_table = 'test_game_replays'
#
#
#class TutorialSections(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    section = models.CharField(max_length=45)
#    description = models.CharField(max_length=100)
#
#    class Meta:
#        managed = False
#        db_table = 'tutorial_sections'
#
#
#class Tutorials(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    section = models.ForeignKey(TutorialSections, db_column='section')
#    name = models.CharField(max_length=45)
#    description = models.CharField(max_length=255)
#    url = models.CharField(max_length=45)
#    map = models.CharField(max_length=100)
#
#    class Meta:
#        managed = False
#        db_table = 'tutorials'
#
#
#class Uniqueid(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    userid = models.ForeignKey(Login, db_column='userid')
#    uuid = models.CharField(max_length=255)
#    mem_serialnumber = models.CharField(db_column='mem_SerialNumber', max_length=255)  # Field name made lowercase.
#    deviceid = models.CharField(db_column='deviceID', max_length=255)  # Field name made lowercase.
#    manufacturer = models.CharField(max_length=255)
#    name = models.CharField(max_length=255)
#    processorid = models.CharField(db_column='processorId', max_length=255)  # Field name made lowercase.
#    smbiosbiosversion = models.CharField(db_column='SMBIOSBIOSVersion', max_length=255)  # Field name made lowercase.
#    serialnumber = models.CharField(db_column='serialNumber', max_length=255)  # Field name made lowercase.
#    volumeserialnumber = models.CharField(db_column='volumeSerialNumber', max_length=255)  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'uniqueid'
#
#
#class Updates(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    file = models.CharField(max_length=45, blank=True)
#    md5 = models.CharField(max_length=45, blank=True)
#
#    class Meta:
#        managed = False
#        db_table = 'updates'
#
#
#class UpdatesBalancetesting(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_balancetesting'
#
#
#class UpdatesBalancetestingFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_balancetesting_files'
#
#
#class UpdatesBlackops(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_blackops'
#
#
#class UpdatesBlackopsFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_blackops_files'
#
#
#class UpdatesCivilians(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_civilians'
#
#
#class UpdatesCiviliansFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_civilians_files'
#
#
#class UpdatesClaustrophobia(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_claustrophobia'
#
#
#class UpdatesClaustrophobiaFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_claustrophobia_files'
#
#
#class UpdatesCoop(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_coop'
#
#
#class UpdatesCoopFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_coop_files'
#
#
#class UpdatesDiamond(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_diamond'
#
#
#class UpdatesDiamondFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_diamond_files'
#
#
#class UpdatesEngyredesign(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_engyredesign'
#
#
#class UpdatesEngyredesignFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_engyredesign_files'
#
#
#class UpdatesFaf(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_faf'
#
#
#class UpdatesFafFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_faf_files'
#
#
#class UpdatesGw(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_gw'
#
#
#class UpdatesGwFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_gw_files'
#
#
#class UpdatesKoth(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_koth'
#
#
#class UpdatesKothFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_koth_files'
#
#
#class UpdatesLabwars(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_labwars'
#
#
#class UpdatesLabwarsFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_labwars_files'
#
#
#class UpdatesMatchmaker(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_matchmaker'
#
#
#class UpdatesMatchmakerFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_matchmaker_files'
#
#
#class UpdatesMurderparty(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_murderparty'
#
#
#class UpdatesMurderpartyFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_murderparty_files'
#
#
#class UpdatesNomads(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_nomads'
#
#
#class UpdatesNomadsFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_nomads_files'
#
#
#class UpdatesPhantomx(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_phantomx'
#
#
#class UpdatesPhantomxFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_phantomx_files'
#
#
#class UpdatesSupremedestruction(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_supremedestruction'
#
#
#class UpdatesSupremedestructionFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_supremedestruction_files'
#
#
#class UpdatesVanilla(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_vanilla'
#
#
#class UpdatesVanillaFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_vanilla_files'
#
#
#class UpdatesWyvern(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_wyvern'
#
#
#class UpdatesWyvernFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_wyvern_files'
#
#
#class UpdatesXtremewars(models.Model):
#    id = models.IntegerField(unique=True)
#    filename = models.CharField(max_length=45)
#    path = models.CharField(max_length=45)
#
#    class Meta:
#        managed = False
#        db_table = 'updates_xtremewars'
#
#
#class UpdatesXtremewarsFiles(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    fileid = models.IntegerField(db_column='fileId')  # Field name made lowercase.
#    version = models.IntegerField()
#    name = models.CharField(max_length=45)
#    md5 = models.CharField(max_length=45)
#    obselete = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'updates_xtremewars_files'
#
#
#class UserAddedReplays(models.Model):
#    user = models.ForeignKey(Login)
#    game = models.ForeignKey(GameStatsBak)
#
#    class Meta:
#        managed = False
#        db_table = 'user_added_replays'
#
#
#class UserGroups(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    user = models.ForeignKey(Login)
#    module = models.CharField(max_length=255)
#    group = models.CharField(max_length=255)
#
#    class Meta:
#        managed = False
#        db_table = 'user_groups'
#
#
#class ValidateAccount(models.Model):
#    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#    userid = models.ForeignKey(Login, db_column='UserID')  # Field name made lowercase.
#    key = models.CharField(db_column='Key', max_length=32)  # Field name made lowercase.
#    expdate = models.DateTimeField(db_column='expDate')  # Field name made lowercase.
#
#    class Meta:
#        managed = False
#        db_table = 'validate_account'
#
#
#class VaultAdmin(models.Model):
#    user_id = models.IntegerField(primary_key=True)
#    group = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'vault_admin'
#
#
#class VersionLobby(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    file = models.CharField(max_length=100, blank=True)
#    version = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        managed = False
#        db_table = 'version_lobby'
#
#
#class ViewGlobalRating(models.Model):
#    id = models.IntegerField(primary_key=True)  # AutoField?
#    mean = models.FloatField(blank=True, null=True)
#    deviation = models.FloatField(blank=True, null=True)
#    numgames = models.IntegerField(db_column='numGames')  # Field name made lowercase.
#    is_active = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'view_global_rating'
