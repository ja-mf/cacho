import redis
import json
import random

redisdb = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_members_info(room):
	members = []
	room_members = list(redisdb.smembers('room_' + room))

	for sessid in room_members:
		members.append(json.loads(redisdb.get('user_' + sessid)))

	return members

def get_members(room):
	return len(redisdb.smembers('room_' + str(room)))

def get_members_name(room):
	members = []
	if get_members(room) == 0:
		return members
		
	room_members = list(redisdb.smembers('room_' + str(room)))
	
	for sessid in room_members:
		members.append(json.loads(redisdb.get('user_' + sessid))['user_name'])
	
	return members



