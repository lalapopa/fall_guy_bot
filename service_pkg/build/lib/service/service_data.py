class ServiceData:
	path_service = 'D:/Documents/Python/fallguy_bot/DATA/NEED_IMG/SERVICE'
	path_levels = 'D:/Documents/Python/fallguy_bot/DATA/NEED_IMG/LEVELS'
	path_data_levels = 'D:/Documents/Python/fallguy_bot/DATA/LEVELS' 

	# levels = ('BigFans','DizzyHeights','DoorDash','GateCrush','HitParade',
	# 'KnightFever','RollOn','SeeSaw','SkylineStumble','TheWhirlygig',
	# 'TundraRun','FreezyPeak','FruitChute','ShortCircuit','SkiFall',
	# 'TipToe','WallGuys','JumpClub','RollOut','SlimeClimb',
	# 'PerfectMatch','zamikanie','SnowballSurvival','test')

	# While CNN testing use that levels variable \/ 
	
	levels = ['KnightFever','RollOn' ,'TundraRun', 'HitParade',
	'DizzyHeights', 'TheWhirlygig', 'DoorDash', 'GateCrush']

	# While test functions 
	# levels = ['SnowballSurvival']
	
	# 'FreezyPeak','FruitChute','ShortCircuit','SkiFall',
	# 'TipToe','WallGuys','JumpClub','RollOut','SlimeClimb',
	# 'PerfectMatch','zamikanie','SnowballSurvival','test']


	keys = ['w','a','s','d','space','e','shift']

	service_buttons = (
		'finding_game', 
		'finding_game2', 
		'Youlost', 
		'nextlevel',
		)

	go_text = ('go',)

	keys_categories = {
	'W':        [1,0,0,0,0,0,0],
	'A':        [0,1,0,0,0,0,0],
	'S':        [0,0,1,0,0,0,0],
	'D':        [0,0,0,1,0,0,0],
	'SPACE':    [0,0,0,0,1,0,0],
	'E':        [0,0,0,0,0,1,0],
	'SHIFT':    [0,0,0,0,0,0,1],
	'NOTHING':  [0,0,0,0,0,0,0],
	}

	img_size_x = 200
	img_size_y = 120

