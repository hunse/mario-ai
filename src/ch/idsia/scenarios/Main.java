/*
 * Copyright (c) 2009-2010, Sergey Karakovskiy and Julian Togelius
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the Mario AI nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

package ch.idsia.scenarios;

import competition.eric.RapidfireAgent;
import competition.gic2010.gameplay.sergeykarakovskiy.SergeyKarakovskiy_ForwardAgent;

import ch.idsia.benchmark.tasks.BasicTask;
import ch.idsia.benchmark.tasks.ProgressTask;
import ch.idsia.tools.MarioAIOptions;
import ch.idsia.agents.Agent;
import ch.idsia.agents.controllers.ForwardAgent;
import ch.idsia.agents.controllers.ForwardJumpingAgent;

/**
 * Created by IntelliJ IDEA. User: Sergey Karakovskiy, sergey at idsia dot ch Date: Mar 17, 2010 Time: 8:28:00 AM
 * Package: ch.idsia.scenarios
 */
public final class Main
{
public static void main(String[] args)
{
	System.out.println(System.getenv("LD_LIBRARY_PATH"));
	
//        final String argsString = "-vis on";
    final MarioAIOptions marioAIOptions = new MarioAIOptions(args);
    marioAIOptions.setLevelRandSeed(0);

    runUserPlayTask(marioAIOptions);
//    runProgressTask(marioAIOptions);

    System.exit(0);
}

public static void runUserPlayTask(MarioAIOptions marioAIOptions)
{
	marioAIOptions.setVisualization(true);
//	marioAIOptions.setFlatLevel(true);
	
    final BasicTask basicTask = new BasicTask(marioAIOptions);
    basicTask.setOptionsAndReset(marioAIOptions);
    basicTask.doEpisodes(1,true,1);
}

public static void runProgressTask(MarioAIOptions marioAIOptions)
{
	marioAIOptions.setVisualization(false);
	
	final Agent agent = new ForwardAgent();
//	final Agent agent = new ForwardJumpingAgent();
//	final Agent agent = new SergeyKarakovskiy_ForwardAgent();
//	final Agent agent = new RapidfireAgent();
	
    final ProgressTask task = new ProgressTask(marioAIOptions);
    task.setOptionsAndReset(marioAIOptions);
    int fitness = task.evaluate(agent);
    System.out.printf("Fitness = %d\n", fitness);
//    basicTask.doEpisodes(1,true,1);

    System.exit(0);
}

//public static void main(String[] args)
//{
////        final String argsString = "-vis on";
//    final MarioAIOptions marioAIOptions = new MarioAIOptions(args);
////        final Environment environment = new MarioEnvironment();
//    final Agent agent = new ForwardAgent();
////        final Agent agent = marioAIOptions.getAgent();
////        final Agent a = AgentsPool.loadAgent("ch.idsia.controllers.agents.controllers.ForwardJumpingAgent");
//    final BasicTask basicTask = new BasicTask(marioAIOptions);
////        for (int i = 0; i < 10; ++i)
////        {
////            int seed = 0;
////            do
////            {
////                marioAIOptions.setLevelDifficulty(i);
////                marioAIOptions.setLevelRandSeed(seed++);
//    basicTask.setOptionsAndReset(marioAIOptions);
////    basicTask.runSingleEpisode(1);
//    basicTask.doEpisodes(1,true,1);
////  System.out.println(basicTask.getEnvironment().getEvaluationInfoAsString());
////  } while (basicTask.getEnvironment().getEvaluationInfo().marioStatus != Environment.MARIO_STATUS_WIN);
////}
////
//System.exit(0);
//}
}
