import sys
sys.path.append(r'C:\Users\21114\.conda\envs\blender_Rena\Lib\site-packages') # 添加当前环境的路径
import bpy
import math
import os
import numpy as np

script_path = r'C:\Users\21114\Desktop\MyProject\blender_gui2'  # 脚本所在路径
npy_name = "pose.npy"
npy_path = os.path.join(script_path, "npy")
npy = os.path.join(npy_path, npy_name)

output_dir = os.path.join(script_path, 'tmp')  # 输出路径
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# ==========================================================================
# 设置动画
# ==========================================================================
class Animator:
    def __init__(self):
        # 驱动数字人所需的blendershape系数
        # self.blender_shapes = {'jawOpen': 25,
        #                        'eyeBlinkLeft': 9,
        #                        'eyeWideLeft': 21,
        #                        'mouthSmileLeft': 44,
        #                        'eyeLookUpLeft': 17,
        #                        'eyeLookDownLeft': 11,
        #                        'eyeLookInLeft': 13,
        #                        'eyeLookOutLeft': 15,
        #                        'browOuterUpLeft': 4,
        #                        'browDownLeft': 1,
        #                        'eyeBlinkRight': 10,
        #                        'eyeWideRight': 22,
        #                        'mouthSmileRight': 45,
        #                        'eyeLookUpRight': 18,
        #                        'eyeLookDownRight': 12,
        #                        'eyeLookOutRight': 16,
        #                        'eyeLookInRight': 14,
        #                        'browOuterUpRight': 5,
        #                        'browDownRight': 2}

        self.blender_shapes = {
        "browDownLeft":1,
        "browDownRight":2,
        "browInnerUp":3,
        "browOuterUpLeft":4,
        "browOuterUpRight":5,
        "cheekPuff":6,
        "cheekSquintLeft":7,
        "cheekSquintRight":8,
        "eyeBlinkLeft":9,
        "eyeBlinkRight":10,
        "eyeLookDownLeft":11,
        "eyeLookDownRight":12,
        "eyeLookInLeft":13,
        "eyeLookInRight":14,
        "eyeLookOutLeft":15,
        "eyeLookOutRight":16,
        "eyeLookUpLeft":17,
        "eyeLookUpRight":18,
        "eyeSquintLeft":19,
        "eyeSquintRight":20,
        "eyeWideLeft":21,
        "eyeWideRight":22,
        "jawForward":23,
        "jawLeft":24,
        "jawOpen":25,
        "jawRight":26,
        "mouthClose":27,
        "mouthDimpleLeft":28,
        "mouthDimpleRight":29,
        "mouthFrownLeft":30,
        "mouthFrownRight":31,
        "mouthFunnel":32,
        "mouthLeft":33,
        "mouthLowerDownLeft":34,
        "mouthLowerDownRight":35,
        "mouthPressLeft":36,
        "mouthPressRight":37,
        "mouthPucker":38,
        "mouthRight":39,
        "mouthRollLower":40,
        "mouthRollUpper":41,
        "mouthShrugLower":42,
        "mouthShrugUpper":43,
        "mouthSmileLeft":44,
        "mouthSmileRight":45,
        "mouthStretchLeft":46,
        "mouthStretchRight":47,
        "mouthUpperUpLeft":48,
        "mouthUpperUpRight":49,
        "noseSneerLeft":50,
        "noseSneerRight":51
        }

    # animation
    def face_animation(self, bs):
        face_ob = bpy.data.objects['face']
        shape_keys = face_ob.data.shape_keys.key_blocks
        for key, value in self.blender_shapes.items():
            bs[value] = bs[value] * 2.0
            if bs[value] > 1.0:
                bs[value] = 1.0
            else:
                pass
            shape_keys[key].value = bs[value]     # 面部姿态信息同步至虚拟表情机器人
            shape_keys[key].keyframe_insert(data_path='value')

    def head_animation(self, rpy_angles):
        head_ob = bpy.data.objects['Armature']
        head = head_ob.pose.bones['Neck']
        head.rotation_mode = "XYZ"
        head.rotation_euler.x = -math.radians(rpy_angles[0])  # x=45 --> 数字人点头
        head.rotation_euler.y = math.radians(rpy_angles[1])  # y=45 --> 数字人左摇头
        head.rotation_euler.z = math.radians(rpy_angles[2])   # z=45 --> 数字人右摆头
        head.keyframe_insert(data_path="rotation_euler", frame=bpy.context.scene.frame_current)  # 更新当前帧
        # head.keyframe_insert(data_path="rotation_euler")  # 更新当前帧

    def all_animation(self,npy):
        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
        bpy.context.scene.display.shading.light = 'MATCAP'
        bpy.context.scene.display.render_aa = 'FXAA'
        bpy.context.scene.render.resolution_x = int(512)
        bpy.context.scene.render.resolution_y = int(768)
        bpy.context.scene.render.fps = 30
        bpy.context.scene.render.image_settings.file_format = 'PNG'

        cam = bpy.data.objects['Camera']
        cam.scale = [2, 2, 2]
        bpy.context.scene.camera = cam

        result = []
        bs = np.load(npy)
        for i in range(bs.shape[0]):
            current_bs = bs[i]
            self.face_animation(current_bs)
            bpy.context.scene.render.filepath = os.path.join(output_dir, f'{i:05d}.png')
            bpy.ops.render.render(write_still=True)


animator = Animator()
animator.all_animation(npy)
