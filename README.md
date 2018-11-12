## This is a project working on LuST Scenario to get car flow from a specific intersection and then generate corresponding route:
First configure the files in deploymentMap the way you want
then run carFlow.py, parseResult.py, makeRoute.py (you have to change the parameter to obey the intersection) sequentially to generate route. works for SUMO 0.26

## Luxembourg SUMO Traffic (LuST) Scenario
The orginal LuST can be found here:
https://github.com/lcodeca/LuSTScenario

LuST Scenario can be lunched directly with four configuration files.
* Mobility: shortest path with rerouting.
  * `sumo -c dua.static.sumocfg` with static traffic lights.
  * `sumo -c dua.actuated.sumocfg` with actuated traffic lights.
* Mobility: Dynamic user equilibrium.
  * `sumo -c due.static.sumocfg` with static traffic lights.
  * `sumo -c due.actuated.sumocfg` with actuated traffic lights.

*A special thanks to Matěj Kubička [matej@matejk.cz] for his contribution to the network topology.*
