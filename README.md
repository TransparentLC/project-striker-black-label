# project-striker-black-label

[![build](https://github.com/TransparentLC/project-striker-black-label/actions/workflows/build.yml/badge.svg)](https://github.com/TransparentLC/project-striker-black-label/actions/workflows/build.yml)
![size](https://img.shields.io/github/repo-size/TransparentLC/project-striker-black-label)
![lines](https://img.shields.io/tokei/lines/github/TransparentLC/project-striker-black-label)

一个出于“尝试从零开始写一个很像东方 Project 系列的弹幕射击游戏”的目的而制作的弹幕射击游戏……的加强版？

前作：[project-striker](https://github.com/TransparentLC/project-striker)

![](https://user-images.githubusercontent.com/47057319/216067582-12c67b32-9948-4c94-a59c-8fa171b9c373.jpg)

## 基本介绍

这是一个使用 [pygame](https://www.pygame.org/) 简单制作的弹幕射击游戏，目的是回避弹幕并击破敌机，在每一关的最后有一个比较强的 BOSS，击破后就算是过关了。

一共有 4 种机体、3 种难度和 5 个关卡，通关流程大概为 25+10 分钟。

音乐和图片用了不少免费素材，具体请参见后面的[借物表](#借物表)。没有剧情之类的设定。另外这个游戏里有不少明目张胆地抄袭东方 Project 的地方（逃）

因为我之前几乎没有制作游戏的经验，所以代码可能十分混乱，美术方面也会有所欠缺（比如严重的瞎眼问题之类的），某些设计可能也不是最佳实践，肥肠抱歉 ( >﹏<。)

以及，虽然公开了源代码，但是我实在是懒得写文档之类的东西，所以这部分的工作就咕咕咕了。

（更详细的介绍请参见游戏内的说明）

## 如何运行

最简单的方式是直接下载[使用 GitHub Actions 自动打包](https://github.com/TransparentLC/project-striker-black-label/actions/workflows/build.yml)的，可以在 Windows/Linux 下运行的可执行文件。打包使用 PyInstaller 完成。

未登录 GitHub 的话，可以在这里下载：

* [Windows 版](https://nightly.link/TransparentLC/project-striker-black-label/workflows/build/master/striker-bl-Windows)
* [Linux 版](https://nightly.link/TransparentLC/project-striker-black-label/workflows/build/master/striker-bl-Linux)

和系统相关的说明：

* Windows 版可能会被 Windows Defender 或其它杀毒软件报毒，属于误报。
* Linux 版打包和测试是在 Ubuntu 22.04 上进行的，并没有测试在其他 Linux 发行版上是否可以运行。可能需要使用 `LD_PRELOAD=/usr/lib64/libstdc++.so.6` 等方式强制使用系统库。
* 打包后的可执行文件为 x64 架构。

也可以从源代码运行，不过稍微有些麻烦：

<details>

* 需要 Python 3.10 或以上版本，使用之前的版本或许也可以运行，但我没有测试过。
* 使用 `pip install -r requirements.txt` 安装依赖。
* 参见[这里](https://github.com/TransparentLC/project-striker/blob/master/font/README.md)下载字体。
* 安装好 `gcc` 和 `g++` ，然后执行 `build-native.sh` 编译 C/C++ 的函数库。
    * 对于 Windows 用户，已经准备了编译好的 DLL。
* 从 `main.py` 开始运行即可。

</details>

配置数据和 replay 存储在项目（或可执行文件）所在的 `savedata` 目录下，删除即可完全初始化。

点击[这里](https://github.com/TransparentLC/project-striker-black-label/files/10564567/savedata.zip)可以下载我自己打的混关展示 replay。

## 操作方法

* <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> 移动自机、在标题画面的菜单项中选择
* <kbd>LShift</kbd> 使用低速移动
* <kbd>Z</kbd> 射击（按住不放就可以连射）、确认
* <kbd>X</kbd> 开启火力强化模式（参见游戏内的说明）、取消
* <kbd>P</kbd> 暂停游戏，再按一下就会恢复
* <kbd>Esc</kbd> 在游戏过程中返回标题画面

（想要改键或使用手柄？试试 [PowerToys](https://github.com/microsoft/PowerToys)、[JoyToKey](https://joytokey.net/) 之类的有按键映射功能的工具吧）

## “太难了，根本不能通关” >_<

**可以的。**

所有的前半/后半道中，以及 BOSS 的每种弹幕攻击我都单独测试过了，在不丢失残机不使用火力强化的情况下都能通过，也就是说**没有无解的弹幕设计**。

实在不能通关的话，损失所有残机~~满身疮痍~~之后还可以续关（最终 BOSS 战中除外），并且没有次数限制。不过续关之后：

* 不再记录分数，以记录续关次数作为替代。
* 在最高难度下也不能见到隐藏 BOSS。
  * 不过，在隐藏 BOSS 战期间是可以续关的。

所以还是以不续关通关为目标努力吧！

## 借物表

* [魔王魂｜無料で使える森田交一の音楽](https://maou.audio/) 所有的背景音乐和大部分的音效
* [Pixabay Royalty Free Sound Effects](https://pixabay.com/sound-effects/) 另一部分使用的音效
* [霞鹜文楷（基于 Klee One 的开源中文字体）](https://github.com/lxgw/LxgwWenKai) 使用的字体
* [铁蒺藜体（基于 Reggae One 的开源中文字体）](https://github.com/Buernia/Tiejili) 使用的字体
* [Avería – The Average Font](http://iotic.com/averia/) 使用的字体
* [Source Han Serif（思源宋体）](https://source.typekit.com/source-han-serif/) 使用的字体
* [Arcade game "1943 - The Battle of Midway" sprite sheet ripped by "AFruitaday!"](https://www.spriters-resource.com/arcade/1943thebattleofmidway/) 部分精灵图
* [Arcade game "1943 Kai" sprite sheet ripped by "AFruitaday!"](https://www.spriters-resource.com/arcade/1943kai/) 部分精灵图
* [Unsplash](https://unsplash.com/) 部分背景图片素材
* [Pixabay](https://pixabay.com/) 部分背景图片素材
* [xBRZ: "Scale by rules" - high quality image upscaling filter by Zenju](https://sourceforge.net/projects/xbrz/files/xBRZ/) 像素画放大算法
* [Free texture packer](https://free-tex-packer.com/) 精灵图打包工具

## 一些技术性较强的高级内容

### Replay 文件结构

<details>

Replay 文件分为文件头、校验码和按键数据三个部分。

文件头具体结构的伪代码：

```c
struct ReplayHeader {
    uint8_t  magic[4];     // 固定为RPLY四个字符
    uint32_t version;      // 版本号，对于每个主程序版本有固定的默认值（游戏机制修改时会改变），与主程序对应版本号不同的replay可能无法正常播放
    uint64_t timestamp;    // 创建replay的时间戳
    uint8_t  name[8];      // 机签
    uint64_t seed;         // 随机种子（random.seed(version=2)）
    uint64_t score;        // 游戏结束时的分数
    uint8_t  type;         // 从低位开始：2位自机类型，2位难度，4位未使用
    uint8_t  missCount;    // MISS次数
    uint8_t  hyperCount;   // 火力强化使用次数
    uint8_t  bonusCount;   // 完美击破奖励次数
    uint32_t unused;       // 未使用
}
```

校验码计算规则：`hmac_sha256(msg=文件头 + 解压后的按键数据, key=???)`。文件头和校验码共计 80 字节，

按键数据保存时使用 `lzma.compress(format=lzma.FORMAT_ALONE)` 压缩。在原始数据中每一帧用一个 `uint8_t` 表示，每个位表示一个按键是否有按下：

* `1 << 0` <kbd>↑</kbd>
* `1 << 1` <kbd>↓</kbd>
* `1 << 2` <kbd>←</kbd>
* `1 << 3` <kbd>→</kbd>
* `1 << 4` <kbd>LShift</kbd>
* `1 << 5` <kbd>Z</kbd>
* `1 << 6` <kbd>X</kbd>
* `1 << 7` <kbd>C</kbd>（未使用）

通关流程大概为 35 分钟，即 35x60x60=126000f，但由于使用了压缩，文件大小一般会远远小于 120 KB。

</details>

### 关于判定和同屏弹幕量

<details>

自机、敌机及弹幕均使用圆形判定，对于 BOSS 之类的较大的敌机则会使用多个圆以尽可能地覆盖敌机图像。

没有硬性的弹幕上限，但为了保持 FPS 稳定为 60（不出现处理落），BOSS 战中的同屏弹幕量一般控制在不超过 600。

由于 pygame 仅使用软件渲染，并且我没有使用多进程，所以只要 CPU 主频足够这个数值的差别就不会很大，显卡性能也不会产生影响。

~~Python 写的东西，还想要什么性能 (╯‵□′)╯︵┻━┻~~

</details>
