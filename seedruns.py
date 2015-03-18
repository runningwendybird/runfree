# This file should be run in order to seed the
# database with run/rating information. Runs can also be
# added to the database by filling out a form, but
# this will be a faster way of seeding the database with
# dozens of runs at once. 

import model
import random
import datetime

def seedruns(user_id, number_of_runs_to_add, starting_date, run_id_start):

	count = 0

	zipcode_choices = ['92126', '93711', '94577', '93720']
	distance_choices = [1.5, 2, 5, 7, 9, 10, 4, 3.1, 6.2, 13.1, 2.25, 8]
	time_choices = [20, 25, 50, 75, 100, 110, 45, 45, 120, 200, 35, 90]
	
	map_choices = [1, 2, 3, 4, 5]

	run_id = run_id_start

	for run in range(number_of_runs_to_add - 1):
		
		# Will add a run object to the sqlalchemy session. 
		user_id = user_id
		date_run = starting_date + datetime.timedelta(count) 
		zipcode = random.choice(zipcode_choices)
		approx_dist = random.choice(distance_choices)
		approx_time = time_choices[distance_choices.index(approx_dist)]
		route_map = random.choice(map_choices)
		commit_date = datetime.datetime.now()

		current_run = model.Run(user_id = user_id, id = run_id, date_run = date_run, zipcode = zipcode, approx_dist = approx_dist, approx_time = approx_time, commit_date = commit_date, route = route_map )
		model.sqla_session.add(current_run)

		# will add ratings for the recently added run object. 

		for question_id in range (1, 11):
			# For number ratings

			if question_id == 1:
				random_rating_number = random.choice([2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			if question_id == 2:
				random_rating_number = random.choice([ 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			if question_id == 3:
				random_rating_number = random.choice([ 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			if question_id == 4:
				random_rating_number = random.choice([ 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			# For selection ratings. 

			if question_id == 5:
				feeling_choices = ['positive', 'optimistic', 'refreshed', 'excited', 'peaceful', 'nervous', 'upset', 'ill', 'injured', 'tired']
				random_feeling = random.choice(feeling_choices)
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_feeling)
			
			if question_id == 6:
				location_choices = ['park', 'city', 'neighborhood', 'trail', 'beach', 'track', 'treadmill']
				random_location = random.choice(location_choices)
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_location)
				# Creating a location rating in order to make sure if treadmill is selected
				# that the treadmill will be consistent throughout ratings.
				location_rating = current_rating
			
			if question_id == 7:
				terrain_choices = ['flat', 'downhill', 'uphill', 'hills']
				
				# checking track for consistency. 
				
				if location_rating.select_ans == "track":
					random_terrain = "flat"
				else:
					random_terrain = random.choice(terrain_choices)

				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_terrain)
			
			if question_id == 8:
				route_choices = ['out_and_back', 'point_to_point', 'random', 'track']

				# Checking treadmill for consistency. 

				if location_rating.select_ans == "treadmill":
					random_route = "treadmill"
				else:
					random_route = random.choice(route_choices) 


				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_route)

			if question_id == 9:

				dummy_text = ["What a good run! I am a beast!", 
				"Tired in the beginning, but improved about a mile in.", 
				"Just what I needed today.", 
				"Today was a hard run.", 
				"I can't wait for my upcoming race!", 
				"Feeling tired this week.", 
				"Burned off stress. Huzzah!", 
				"Legs are tired, heart and lungs felt strong!", 
				"Best part of my day", 
				"I can't wait to run again."]

				random_text = random.choice(dummy_text)

				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, text_ans = random_text)

			if question_id == 10:

				instagram_embeds = ['<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/zxs5BXi09R/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">UCSD run!</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Hayley Denbraver (@runwendybird) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-03-03T19:03:10+00:00">Mar 3, 2015 at 11:03am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', 
				'<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/zxs96LC09b/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">I love trails!</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Hayley Denbraver (@runwendybird) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-03-03T19:03:50+00:00">Mar 3, 2015 at 11:03am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', 
				'<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/zxp90Ki045/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">Lake Chabot run!</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Hayley Denbraver (@runwendybird) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-03-03T18:37:37+00:00">Mar 3, 2015 at 10:37am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', 
				'<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/zua0GzICQc/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">MONDAY MOTIVATION: &#34;Life is complicated. Running is simple. Is it any wonder that people like to run?&#34; - Kevin Nelson #RUNspiration</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Runner&#39;s World (@runnersworldmag) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-03-02T12:27:29+00:00">Mar 2, 2015 at 4:27am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', 
				'<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/zkLclKoCdy/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">On your next run, stop to look around and appreciate your surroundings. #RUNspiration (Photo credit: @hannahmcgold)</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Runner&#39;s World (@runnersworldmag) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-02-26T13:00:48+00:00">Feb 26, 2015 at 5:00am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', 
				'<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/zcmMMpoCT6/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">What do you hope to achieve this week? #RUNspiration</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Runner&#39;s World (@runnersworldmag) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2015-02-23T14:20:34+00:00">Feb 23, 2015 at 6:20am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', 
				'<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-version="4" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:658px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:8px;"> <div style=" background:#F8F8F8; line-height:0; margin-top:40px; padding:50% 0; text-align:center; width:100%;"> <div style=" background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAAAGFBMVEUiIiI9PT0eHh4gIB4hIBkcHBwcHBwcHBydr+JQAAAACHRSTlMABA4YHyQsM5jtaMwAAADfSURBVDjL7ZVBEgMhCAQBAf//42xcNbpAqakcM0ftUmFAAIBE81IqBJdS3lS6zs3bIpB9WED3YYXFPmHRfT8sgyrCP1x8uEUxLMzNWElFOYCV6mHWWwMzdPEKHlhLw7NWJqkHc4uIZphavDzA2JPzUDsBZziNae2S6owH8xPmX8G7zzgKEOPUoYHvGz1TBCxMkd3kwNVbU0gKHkx+iZILf77IofhrY1nYFnB/lQPb79drWOyJVa/DAvg9B/rLB4cC+Nqgdz/TvBbBnr6GBReqn/nRmDgaQEej7WhonozjF+Y2I/fZou/qAAAAAElFTkSuQmCC); display:block; height:44px; margin:0 auto -44px; position:relative; top:-22px; width:44px;"></div></div> <p style=" margin:8px 0 0 0; padding:0 4px;"> <a href="https://instagram.com/p/wwKogCoCa8/" style=" color:#000; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none; word-wrap:break-word;" target="_top">Runs end; running doesn&#39;t. #runmotivation</a></p> <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;">A photo posted by Runner&#39;s World (@runnersworldmag) on <time style=" font-family:Arial,sans-serif; font-size:14px; line-height:17px;" datetime="2014-12-18T15:10:24+00:00">Dec 18, 2014 at 7:10am PST</time></p></div></blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>']
			
				random_instagram = random.choice(instagram_embeds)

				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, text_ans = random_instagram)

			model.sqla_session.add(current_rating)

		count = count + 1
		run_id = run_id + 1

	model.sqla_session.commit()
	print "Commited runs and ratings to the database."

def select_start_date():
	print "This will select a start date to generate from."
	
	day_of_month = int(input("Enter day of the month in DD format: "))
	month = int(input("Enter the month in MM format: "))
	year = int(input("Enter the year YYYY format: "))

	starting_date = datetime.datetime(year, month, day_of_month, 8, 45, 0, 0)

	return starting_date

def main():

	# Set up all the parameters we need to start the seeding. 

	starting_date = select_start_date()
	user_id = int(input("Enter user_id for whom you want to add runs: "))
	number_of_runs_to_add = int(input("Enter number of runs to add."))
	run_id_start = int(input("Enter desired starting run_id: "))

	# Seed the database. 

	seedruns(user_id, number_of_runs_to_add, starting_date, run_id_start)


if __name__ == "__main__":
	main()

		