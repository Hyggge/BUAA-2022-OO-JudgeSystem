## 文件说明

* clean.sh：用于清理 logWA 和 logTLE
* colorfulPrint.py：用于提供彩色输出
* datainput_student_linux_x86_64：官方投喂包
* generate.py：数据生成器
* judger.py：测评主程序
* outputChecker.py：输出检查程序

## 参数说明

generate.py 中的参数 `dst_mode, run_mode` 用于控制请求的空间聚集性，详见注释；`TIME_GAP_MODE` 用于控制请求的时间密集型，详见注释

judger.py 中的参数 `playerName` 用于存放测试程序名称；`playerNum` 表示参加测试程序数，如果小于 `len(playerName)` 则取前几个；`userMaker` 表示是否使用数据生成器，如果不使用需要将待测数据写入 stdin.txt；`testNum` 表示测试次数，需要在 `userMaker = True` 时生效；`displayDetail` 为真时将显示正在执行的命令；测试时默认最大允许时间为 150s，如果超时将强制结束，并且输出 `Program can't end normaly!`，但是测评机不能给出到底是谁超时了

## 运行方法

先将所有待测程序打包好放入该目录，然后设置 judger.py 中的参数 `playerName, playerNum` 等，然后创建文件夹 logWA 和 logTLE（或者直接运行 clean.sh），最后运行 judger.py 即可