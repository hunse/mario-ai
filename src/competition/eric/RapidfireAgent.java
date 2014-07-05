package competition.eric;

import ch.idsia.agents.Agent;
import ch.idsia.agents.controllers.BasicMarioAIAgent;
import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.Environment;

public class RapidfireAgent extends BasicMarioAIAgent implements Agent
{
public RapidfireAgent()
{
    super("RapidfireAgent");
    reset();
}

boolean lastKeySpeed = false;

public boolean[] getAction()
{
//    action[Mario.KEY_SPEED] = action[Mario.KEY_JUMP] = isMarioAbleToJump || !isMarioOnGround;
	action[Mario.KEY_JUMP] = isMarioAbleToJump;
	action[Mario.KEY_SPEED] = isMarioOnGround || isMarioAbleToShoot;
	lastKeySpeed = action[Mario.KEY_SPEED];
    return action;
}

public void reset()
{
    action = new boolean[Environment.numberOfKeys];
    action[Mario.KEY_RIGHT] = true;
//    action[Mario.KEY_SPEED] = false;
    lastKeySpeed = false;
}
}