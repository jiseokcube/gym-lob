from gym.envs.registration import register

register(
    id='lob',
    entry_point='gym_lob.envs:LOBEnv',
)
