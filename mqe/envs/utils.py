# environments
from mqe.envs.field.legged_robot_field import LeggedRobotField
from mqe.envs.go1.go1 import Go1
from mqe.envs.npc.go1_sheep import Go1Sheep
from mqe.envs.npc.go1_object import Go1Object
from mqe.envs.npc.go1_football_defender import Go1FootballDefender
# from mqe.envs.npc.go2_football_defender import Go2FootballDefender


# configs
from mqe.envs.field.legged_robot_field_config import LeggedRobotFieldCfg
from mqe.envs.configs.go1_plane_config import Go1PlaneCfg
from mqe.envs.configs.go1_gate_config import Go1GateCfg
from mqe.envs.configs.go1_sheep_config import SingleSheepCfg, NineSheepCfg
from mqe.envs.configs.go1_football_config import Go1FootballDefenderCfg, Go1Football1vs1Cfg, Go1Football2vs2Cfg, Go1FootballShootCfg
from mqe.envs.configs.go1_seesaw_config import Go1SeesawCfg
from mqe.envs.configs.go1_door_config import Go1DoorCfg
from mqe.envs.configs.go1_pushbox_config import Go1PushboxCfg
from mqe.envs.configs.go1_tug_config import Go1TugCfg
from mqe.envs.configs.go1_wrestling_config import Go1WrestlingCfg
from mqe.envs.configs.go1_rotation_config import Go1RotationCfg
from mqe.envs.configs.go1_bridge_config import Go1BridgeCfg


# wrappers
from mqe.envs.wrappers.empty_wrapper import EmptyWrapper
from mqe.envs.wrappers.go1_gate_wrapper import Go1GateWrapper
from mqe.envs.wrappers.go1_pushbox_wrapper import Go1PushboxWrapper
from mqe.envs.wrappers.go1_sheep_wrapper import Go1SheepWrapper
from mqe.envs.wrappers.go1_seesaw_wrapper import Go1SeesawWrapper
from mqe.envs.wrappers.go1_football_wrapper import Go1FootballDefenderWrapper, Go1FootballGameWrapper, Go1FootballShootWrapper
from mqe.envs.wrappers.go1_tug_wrapper import Go1TugWrapper
from mqe.envs.wrappers.go1_wrestling_wrapper import Go1WrestlingWrapper
from mqe.envs.wrappers.go1_rotation_wrapper import Go1RotationWrapper
from mqe.envs.wrappers.go1_bridge_wrapper import Go1BridgeWrapper


from mqe.utils import get_args, make_env

from typing import Tuple

ENV_DICT = {
    "go1plane": {
        "class": Go1,
        "config": Go1PlaneCfg,
        "wrapper": EmptyWrapper
    },
    "go1gate": {
        "class": Go1,
        "config": Go1GateCfg,
        "wrapper": Go1GateWrapper  # no return
    },
    "go1sheep-easy": {
        "class": Go1Sheep,
        "config": SingleSheepCfg,
        "wrapper": Go1SheepWrapper
    },
    "go1sheep-hard": {
        "class": Go1Sheep,
        "config": NineSheepCfg,
        "wrapper": Go1SheepWrapper
    },
    "go1football-defender": {
        "class": Go1FootballDefender,
        "config": Go1FootballDefenderCfg,
        "wrapper": Go1FootballDefenderWrapper
    },
    "go1football-1vs1": {
        "class": Go1Object,
        "config": Go1Football1vs1Cfg,
        "wrapper": Go1FootballGameWrapper  # no return
    },
    "go1football-2vs2": {
        "class": Go1Object,
        "config": Go1Football2vs2Cfg,
        "wrapper": Go1FootballGameWrapper  # no return
    },
    "go1seesaw": {
        "class": Go1Object,
        "config": Go1SeesawCfg,
        "wrapper": Go1SeesawWrapper
    },
    "go1pushbox": {
        "class": Go1Object,
        "config": Go1PushboxCfg,
        "wrapper": Go1PushboxWrapper
    },
    "go1tug": {
        "class": Go1Object,
        "config": Go1TugCfg,
        "wrapper": Go1TugWrapper
    },
    "go1wrestling": {
        "class": Go1Object,
        "config": Go1WrestlingCfg,
        "wrapper": Go1WrestlingWrapper
    },
    "go1revolvingdoor": {
        "class": Go1Object,
        "config": Go1RotationCfg,
        "wrapper": Go1RotationWrapper
    },
    "go1bridge": {
        "class": Go1Object,
        "config": Go1BridgeCfg,
        "wrapper": Go1BridgeWrapper
    },
    # "go1door": {
    #     "class": Go1Object,
    #     "config": Go1DoorCfg,
    #     "wrapper": Go1SeesawWrapper
    # },
    "go1football-shoot":{
        "class": Go1Object,
        "config": Go1FootballShootCfg,
        "wrapper": Go1FootballShootWrapper
    },
    # TODO: ------------------ go2 -------------------- 
    # "go2football-defender":{
    #     "class": ,
    #     "config": ,
    #     "wrapper": 
    # },
    # "go2football-shoot":{
    #     "class": ,
    #     "config": ,
    #     "wrapper": 
    # }
}

def make_mqe_env(env_name: str, args=None, custom_cfg=None) -> Tuple[LeggedRobotField, LeggedRobotFieldCfg]:
    
    env_dict = ENV_DICT[env_name]

    if callable(custom_cfg):
        env_dict["config"] = custom_cfg(env_dict["config"])
        
    env, env_cfg = make_env(env_dict["class"], env_dict["config"], args)
    env = env_dict["wrapper"](env)

    return env, env_cfg

def custom_cfg(args):
    """
    对env_dict["config"]加工, 将env_dict["config"]中预定义的num_envs替换成train()中输入的args.num_envs, 另外包括是否record_video
    """
    def fn(cfg:LeggedRobotFieldCfg):
        
        if getattr(args, "num_envs", None) is not None:
            cfg.env.num_envs = args.num_envs
        
        cfg.env.record_video = args.record_video

        return cfg
    
    return fn