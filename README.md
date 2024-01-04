> 查询某个类别的所属干员, 支持别名

已支持的查询**类别**:

- 职业
- 分支 (子职业)
- 种族
- 势力
- 队伍
- 阵营
- 画师 <font color=Green>*new</font>

## 使用   

- 直接查询 
    - `兔兔近卫`
    - `兔兔中坚术师`
    - `兔兔黎博利`
    - `兔兔罗德岛`
    - `兔兔Skade` <font color=Green>*new</font>
    <br>...<br>

- 按干员查询 <font color=Green>*new</font>
    - `兔兔锏的职业`
    - `兔兔小羊的分支` 
    - `兔兔白咕咕的种族`
    - `兔兔迷迭香的阵营`
    - `兔兔归溟幽灵鲨的画师`
    <br>...<br>
    <font color=Orange>注意: 此方法必须包含关键词 `的[类别]`</font>
    <br>

- **与其他关键词冲突时, 使用 `兔兔[类别][名称]` 来提高优先级**
    - `兔兔种族菲林`  <font color=Grey>(与 林 冲突)</font>
    - `兔兔种族阿戈尔` <font color=Grey>(与 阿 冲突)</font>
    - `兔兔势力阿戈尔` <font color=Grey>(与 种族阿戈尔 冲突)</font>
    - `兔兔画师幻象黑兔`  <font color=Green>*new</font> <font color=Grey>(与 黑 冲突)</font>


## 其他说明

- 支持别名, 需要自行设置, 如: `兔兔领主别名远卫`
- 建议配合 [查询快速响应](https://console.amiyabot.com/#/shop) 食用

## 开发计划 (可能咕)
- 伤害类型
- buff, debuff类型
- 基建技能组合

## 配置

> 前往 [插件管理-干员查询扩展-插件配置](https://console.amiyabot.com/#/plugin) 修改 <br>
> 配置实时更新，无需重启bot

- 默认优先级


---
   问题反馈：在 [Amiya的测试工坊—插件开发&使用交流](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=1XqeeRDjEVa&from=246610&biz=ka#/pc) 中@.Tdp

   感谢 [幻月皮肤资源包](https://console.amiyabot.com/#/plugin) 提供的部分图标

      
| 版本  | 变更                                 
|-------|---------------------------------
| 2.5.2 | 可选隐藏未知类别
| 2.5   | 支持按干员查询; 修复职业查询报错
| 2.4   | 大幅优化响应速度; 向下获取最新头像;<br> 防止空白头像; 支持查询画师
| 2.3.8 | 临时修复无立绘报错
| 2.3.7 | 统一log标题; 画饼(
| 2.3   | 调整模板; 使用皮肤头像
| 2.2   | 适配新版gamedata
| 2.1   | 修复优先级
| 2.0.4 | 优化模板
| 2.0   | 添加通用模板, 支持查询快速响应;<br>优化同名优先级; 默认优先级可调; 
| 1.1   | 支持查询种族/势力/队伍/阵营
| 1.0   | 添加职业/分支查询功能               




