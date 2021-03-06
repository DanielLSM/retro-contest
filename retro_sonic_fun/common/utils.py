import json
import gym
import numpy as np

# from baselines.common.atari_wrappers import WarpFrame, FrameStack
# import gym_remote.client as grc


#normalize pixel values
def normalize_obs(obs):
    return obs.astype('float32') / 255.


def create_json_params(params: dict, model_name: str):
    file_name = '{}.json'.format(model_name)
    with open(file_name, 'w') as handle:
        json.dump(params, handle)
    print("{} generated".format(file_name))


def load_json_params(file_name: str):
    with open(file_name, 'r') as handle:
        params = json.load(handle)
    print("{} loaded".format(file_name))
    return params


class NN(type):
    pass


# from https://github.com/openai/retro-baselines/blob/master/agents/sonic_util.py
#################################################################################
# def make_env(stack=True, scale_rew=True):
#     """
#     Create an environment with some standard wrappers.
#     """
#     env = grc.RemoteEnv('tmp/sock')
#     env = SonicDiscretizer(env)
#     if scale_rew:
#         env = RewardScaler(env)
#     env = WarpFrame(env)
#     if stack:
#         env = FrameStack(env, 4)
#     return env


#CHANGED
class SonicDiscretizer(gym.ActionWrapper):
    """
    Wrap a gym-retro environment and make it use discrete
    actions for the Sonic game.
    """

    def __init__(self, env):
        super(SonicDiscretizer, self).__init__(env)
        buttons = [
            "B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y",
            "X", "Z"
        ]
        actions = [['LEFT'], ['RIGHT'], ['LEFT', 'DOWN'], ['RIGHT', 'DOWN'],
                   ['DOWN'], ['DOWN', 'B'], ['B'], ['RIGHT', 'B'],\
                   ['LEFT', 'B'], ['NULL']]
        self._actions = []
        for action in actions[:-1]:
            arr = np.array([False] * 12)
            for button in action:
                arr[buttons.index(button)] = True
            self._actions.append(arr)
        self._actions.append(np.array([False] * 12))
        self.action_space = gym.spaces.Discrete(len(self._actions))

    def action(self, a):  # pylint: disable=W0221
        return self._actions[a].copy()


# class RewardScaler(gym.RewardWrapper):
#     """
#     Bring rewards to a reasonable scale for PPO.
#     This is incredibly important and effects performance
#     drastically.
#     """

#     def reward(self, reward):
#         return reward * 0.01

# class AllowBacktracking(gym.Wrapper):
#     """
#     Use deltas in max(X) as the reward, rather than deltas
#     in X. This way, agents are not discouraged too heavily
#     from exploring backwards if there is no way to advance
#     head-on in the level.
#     """

#     def __init__(self, env):
#         super(AllowBacktracking, self).__init__(env)
#         self._cur_x = 0
#         self._max_x = 0

#     def reset(self, **kwargs):  # pylint: disable=E0202
#         self._cur_x = 0
#         self._max_x = 0
#         return self.env.reset(**kwargs)

#     def step(self, action):  # pylint: disable=E0202
#         obs, rew, done, info = self.env.step(action)
#         self._cur_x += rew
#         rew = max(0, self._cur_x - self._max_x)
#         self._max_x = max(self._max_x, self._cur_x)
#         return obs, rew, done, info

#################################################################################
#################################################################################
