# 数字人实时表情模拟系统

## 项目简介

**数字人实时表情模拟系统** 是一个结合 **Blender**、**AI面部捕捉** 和 **PyQt5 GUI** 开发的实时表情模拟系统。该系统通过摄像头实时捕捉用户面部的关键点数据，使用AI模型将这些数据映射为Blender中的形状键动画，从而驱动虚拟角色的面部表情。最终的动画通过Blender渲染并使用FFmpeg生成MP4格式的视频。

## 项目功能

- **实时面部捕捉**：通过摄像头和OpenCV结合FaceMesh模型，实时捕捉用户的面部关键点数据。
- **AI模型推理**：将捕捉到的面部关键点转换为Blender中虚拟角色的形状键参数，驱动面部表情动画。
- **Blender动画生成**：通过Blender的Python API渲染虚拟角色的面部表情动画。
- **视频合成**：使用FFmpeg将渲染的图像序列合成为MP4视频。
- **用户界面**：使用PyQt5提供简洁易用的GUI界面，用户可以控制录制、渲染和视频播放。

## 系统架构

1. **面部捕捉模块**：使用OpenCV和FaceMesh获取面部关键点。
2. **关键点到形状键转换**：AI模型将关键点映射为Blender的blendshapes参数。
3. **Blender渲染模块**：通过Python API控制Blender动画生成并输出图像序列。
4. **视频合成模块**：FFmpeg将渲染出的图像序列合成为MP4视频。
5. **GUI模块**：PyQt5提供用户操作界面，实现录制、渲染、保存等功能。

## 安装步骤

### 依赖环境

- Python 3.8+
- Blender 3.6（需安装Python API）
- OpenCV

**注意！！Python版本请务必和Blender内置Python版本一致！！**

### 安装方法

1. 克隆项目代码：
   ```bash
   git clone https://github.com/IggyMeraki/digital-human-emotion-system.git
   cd digital-human-emotion-system
   ```

2. 安装所需Python依赖：

   ```
   pip install -r requirements.txt
   ```
   
2. 安装并配置Blender的Python API：

   - 在Blender首选项中启用Python脚本控制。
   - 确保Blender的Python版本与项目一致。

3. 配置FFmpeg：

   - 下载并安装FFmpeg。
   - 确保FFmpeg的可执行文件路径已添加到系统环境变量中。

## 使用说明

1. 程序地址更改

   1. 在<u>animator.py</u>的**Line2**改为项目环境绝对路径，**Line8**改为项目文件夹绝对路径

   2. 在<u>run_blender.py</u>的**Line10**改为Blender程序的绝对路径

2. 启动程序：

   ```bash
   python qt_main.py
   ```

3. 在GUI界面中，用户可以选择以下功能：

   - **开始录制**：点击按钮启动面部捕捉。
   - **停止录制**：点击按钮停止录制。
   - **开始渲染**：点击按钮生成Blender动画并渲染视频。
   - **播放视频**：预览生成的视频文件。

4. 输出的MP4视频文件将保存在 `output/` 文件夹中。

## 贡献指南

欢迎大家贡献代码和提交问题！如有改进建议或问题，请提交Issue或Pull Request。

## 许可证

该项目基于 MIT License 开源。