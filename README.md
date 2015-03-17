
## About RunFree, RunMe

### Project Overview

RunFree, RunMe is a beginner friendly running log that can help anyone enjoy the physical, mental, and emotional benefits that regular running provides. Users answer a series of questions about the quality of each logged run. Additionally they can associate a single run with a route from MapMyRun and a picture from Instagram. Users can visualize their progress with graphs that illustrate their running habits and how running impacts their daily lives. RunFree, RunMe provides users insight into their optimal running conditions. A goal setting feature incorporating the active.com API will have the users crossing the finish line smiling.

### Technologies

Python, Flask, Javascript, JQuery, AJAX, JSON, HTML/CSS, Jinja, SQLAlchemy, D3, Active.com API, Machine Learning

### Disclaimer

Running is excellent excercise and is beneficial in many ways for the majority of people, but it is always important to check with your physician before adopting a new excercise regime. A simple visit could save your health or your life. 

### To Get RunFree, RunMe On Your Computer

<ol>
	<li>Clone this repository.</li>
	<li>Set up and activate your virtual environment to match requirements.txt.</li>
	<li>Set up your database by running the following commands.</li>
		<ul>
			<li>python -i model.py</li>
			<li>create_db()</li>
			<li>python -i seedqs.py</li>
			<li>seed(questions)</li>
		</ul>
	<li>Get an API key from active.com. Put this in a secrets.sh file in this format: "export ACTIVEDOTCOM_KEY=YOUR_KEY_HERE" and enter "source secrets.sh" in your terminal.</li>
	<li>Start the server with the command: python runfree.py</li>
	<li>You can now create your first user and explore the app.</li>
</ol>


### Features

RunFree, RunMe is a comprehensive running app which focuses on tapping into not only the physical benefits of running, but also the emotional benefits. The following features were all developed with that focus.

#### Landing Page

<img src="/static/images/user_landing.jpg">

Upon logging in, RunFree, RunMe users can see a calendar heatmap of their recent running. The user is also informed if one of his or her recent runs met a milestone for one of his or her goals. Users also get a chance to see pictures from their most recent runs.

#### Running Log

<img src="/static/images/run_report.jpg">

RunFree, RunMe is first and foremost a place to log and track your runs. It is much more than that as well. When you review your run, you can see a map of your route, an instagram picture from the run, a detailed summary of how the run impacted your mood, and an overview of the running conditions (terrain type, route type, etc).

#### Route Library

<img src="/static/images/routes.jpg">

Users can store their routes from MapMyRun and add notes and a description. These routes can be selected for a given run.

#### Goal Setting and Tracking

<img src="/static/images/goal.jpg">

One of the most innovative features of RunFree RunMe is the goal setting and tracking feature. Many beginners aren't sure how to set a goal. Questions such as "What is a good first goal?", "What is a reasonable time frame for my goal?" and "Where do I find a race?" can be overwhelming for beginners. RunFree, RunMe allows the user to select a goal and using the user inputted fitness level and running history determines a reasonable time frame for the goal. The user can then select a race from options that RunFree, RunMe currates using the Active.com API or can choose to set a goal date without an associated race.

Once a goal is set, when the user reviews the goal, he or she can see a countdown, the website associated with their race, and a series of milestones that should be met before the goal is attempted. RunFree, RunMe determines when a run you logged met a milestone. Once the run is confirmed by the user, the milestone will display as complete.

#### Run Visualization

Data Visualization is a common feature of running web applications. RunFree, RunMe focuses on the emotional and mental benefits of running, so its data visualization is a little bit different. Currently there are three type of graphs that can be viewed on RunFree, RunMe.

<div><img src="/static/images/mileage_graph.jpg"></div><br>

The first chart that users see upon clicking on the "Run Graphs" tab is a simple bar chart showing the most recent runs. The length of the bar corresponds to the distance and the color of the bar changes based on how highly the user rated the run.

<div><img src="/static/images/conditions.jpg"></div><br>

The next charts that the users can peruse is a series of pie charts that help the user see the variation of their runs. Users can easily see what percentage of their runs take place at a park or around a neighborhood. With a glance the user can determine that most of their runs are a looped course, but that he or she hasn't been to the track lately. We all love running on flat stretches, but maybe it would be better if a higher percentage of runs occured on a hilly course.

<div><img src="/static/images/moodmap.jpg"></div><br>

The final type of chart currently available is what is called a "mood map". Each bubble corresponds to a question that the user answered for a single run. The diameter of the bubble is relative to the distance for the run it represents. The color indicates how well the user indicated he or she was feeling. Darker bubbles correspond to positive feelings, lighter bubbles correspond to more negative feelings. Users can easily see how their feelings change from before the run, during the run, to after the run.


#### Ideal Run Conditions
<img src="/static/images/ideal_runs.jpg">

It is the goal of RunFree, RunMe to help people enjoy running and see the physical, emotional, and mental benefits that regular activity provides. With that goal in mind, RunFree, RunMe helps user pinpoint the conditions under which they are likely to have a highly rated run. RunFree, RunMe determines what a highly rated run is for the given user, and it reports the conditions most strongly associated with these runs: distance, setting, terrain, weekday, etc. The user can user this information to zero in on the sorts of runs that they are likely to enjoy, or the user can choose to challenge him or herself with a more taxing run.


#### Acknowledgements
<ul>
	<li>RunFree, RunMe badges were drawn by Noelle Cook. Lots of love and thanks.</li>
	<li>The <a href="http://glyphicons.com/">Glyphicons</a> used in RunFree, RunMe buttons and Navbar are part of the free set included in Bootstrap.</li>
	<li>The calendar heatmap uses a creative commons licensed javascript module by Wan Qi Chen and available at <a href="http://kamisama.github.io/cal-heatmap/">http://kamisama.github.io/cal-heatmap/</a></li>
	<li>Data Visualizations were created using D3 and based off examples found at <a href="https://github.com/mbostock/d3/wiki/Gallery">https://github.com/mbostock/d3/wiki/Gallery</a></li>
	<li>Thanks to Hackbright Mentors: Cole Goeppinger, Tess Bakke, Vishal Srivastava, and Danielle Robinson.</li>
	<li>Thanks to the excellent teaching staff at Hackbright Academy and to the wonderful ladies of the Winter 2015 cohort.</li>
</ul>
