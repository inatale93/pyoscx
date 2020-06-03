import pyoscx   


route = pyoscx.Route('myroute')

route.add_waypoint(pyoscx.WorldPosition(),'shortest')

route.add_waypoint(pyoscx.WorldPosition(1,1,1),'shortest')




# routepos = pyoscx.RoutePositionOfCurrentEntity(route,'Ego')
# routepos = pyoscx.RoutePositionInRoadCoordinates(route,1,3)
routepos = pyoscx.RoutePositionInLaneCoordinates(route,1,'a',2)
pyoscx.prettyprint(routepos.get_element())


### create catalogs
catalog = pyoscx.Catalog()
catalog.add_catalog('VehicleCatalog','../xosc/Catalogs/Vehicles')



### create road
road = pyoscx.RoadNetwork(roadfile='../xodr/e6mini.xodr',scenegraph='../models/e6mini.osgb')


### create parameters
paramdec = pyoscx.ParameterDeclarations()

paramdec.add_parameter(pyoscx.Parameter('$HostVehicle','string','car_white'))
paramdec.add_parameter(pyoscx.Parameter('$TargetVehicle','string','car_red'))


## create entities

egoname = 'Ego'
targetname = 'Target'

entities = pyoscx.Entities()
entities.add_scenario_object(egoname,pyoscx.CatalogReference('VehicleCatalog','car_white'))
entities.add_scenario_object(targetname,pyoscx.CatalogReference('VehicleCatalog','car_red'))


### create init

init = pyoscx.Init()
step_time = pyoscx.TransitionDynamics('step','time',1)

egospeed = pyoscx.AbsoluteSpeedAction(30,step_time)
egostart = pyoscx.TeleportAction(pyoscx.LanePosition(25,0,-3,0))

targetspeed = pyoscx.AbsoluteSpeedAction(40,step_time)
targetstart = pyoscx.TeleportAction(pyoscx.LanePosition(15,0,-2,0))

init.add_init_action(egoname,egospeed)
init.add_init_action(egoname,egostart)
init.add_init_action(targetname,targetspeed)
init.add_init_action(targetname,targetstart)


### create an event

trigcond = pyoscx.TimeHeadwayCondition(targetname,0.1,'greaterThan')

trigger = pyoscx.EntityTrigger('mytesttrigger',0.2,'rising',trigcond,egoname)

event = pyoscx.Event('myfirstevent','overwrite')
event.add_trigger(trigger)

sin_time = pyoscx.TransitionDynamics('linear','time',3)
action = pyoscx.LongitudinalDistanceAction(-4,egoname,max_deceleration=3,max_speed=50)
event.add_action('newspeed',action)


## create the act, 
man = pyoscx.Maneuver('my_maneuver')
man.add_event(event)

mangr = pyoscx.ManeuverGroup('mangroup')
mangr.add_actor('$owner')
mangr.add_maneuver(man)
starttrigger = pyoscx.ValueTrigger('starttrigger',0,'rising',pyoscx.SimulationTimeCondition(0,'greaterThan'))
act = pyoscx.Act('my_act',starttrigger)
act.add_maneuver_group(mangr)

## create the story
storyparam = pyoscx.ParameterDeclarations()
storyparam.add_parameter(pyoscx.Parameter('$owner','string',targetname))
story = pyoscx.Story('mystory',storyparam)
story.add_act(act)

## create the storyboard
sb = pyoscx.StoryBoard(init)
sb.add_story(story)

## create the scenario
sce = pyoscx.Scenario('adaptspeed_example','Mandolin',paramdec,entities=entities,storyboard = sb,roadnetwork=road,catalog=catalog)
# display the scenario
# pyoscx.prettyprint(sce.get_element())

# if you want to save it
# sce.write_xml('myfirstscenario.xml',True)

# if you have esmini downloaded and want to see the scenario
# pyoscx.esminiRunner(sce)