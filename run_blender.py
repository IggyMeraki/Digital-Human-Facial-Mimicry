import subprocess
import os
import shutil


def run_blender(Communicator,playButton,recordButton):
    playButton.setEnabled(False)
    recordButton.setEnabled(False)
    # 定义Blender的路径以及要执行的Python脚本路径
    blender_path = r"C:\Program Files\Blender Foundation\Blender 3.6\blender-launcher.exe"  # 需要替换为你本地的Blender安装路径
    script_path = "animator.py"                         # 需要替换为你想要运行的Blender Python脚本路径
    blend_file_path = "render.blend"                    # 需要替换为你想要渲染的Blender文件路径

    # 运行Blender并执行脚本
    subprocess.run([blender_path, blend_file_path, "--background", "--python", script_path])
    Communicator.update_text.emit("AI模型推理完成\n")
    print("Blender渲染完成")

    # 图片文件夹路径
    image_folder = "tmp"  # 替换为你的图片文件夹路径
    output_video_path = 'outputs/blender.mp4'  # 输出视频文件路径

    # 检查输出目录是否存在，不存在则创建
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 获取文件夹中的所有图片文件名，并按顺序排序
    image_files = sorted([file for file in os.listdir(image_folder) if file.endswith('.png')])

    # 检查是否有图片
    if not image_files:
        raise Exception("没有找到任何png图片")

    # 确保文件名按数字顺序命名，比如 img_001.png, img_002.png
    # 运行 ffmpeg 命令，将图片合成为视频
    ffmpeg_command = [
        'ffmpeg', '-y',  # 覆盖输出文件
        '-framerate', '15',  # 设置帧率
        '-i', os.path.join(image_folder, '%05d.png'),  # 输入图片格式，假设文件名格式为四位数字
        '-c:v', 'libx264',  # 使用libx264编码
        '-pix_fmt', 'yuv420p',  # 视频像素格式
        output_video_path  # 输出视频文件
    ]

    # 执行 ffmpeg 命令
    subprocess.run(ffmpeg_command, check=True)

    # print("视频生成完成:", output_video_path)
    Communicator.update_text.emit("推理结果渲染完成\n")
    playButton.setEnabled(True)
    recordButton.setEnabled(True)
    shutil.rmtree(image_folder)  # 删除图片文件夹
    return True

if __name__ == '__main__':
    run_blender()