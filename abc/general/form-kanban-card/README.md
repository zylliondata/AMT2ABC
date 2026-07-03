简单输入表单 ABC
form-kanban-card · category: form · industry: general

看板请求展示ABC，用于获取看板数据列表

接口契约
Inputs
名称	类型	说明	默认值
token	string	用户身份令牌	""
tenantId	string	租户ID	""
resourceId	string	数据产品ID	""
correlationId string 流程ID ""
Outputs
名称	类型	说明
table_select	string	当前选中行详情
Methods
名称	说明
Events
名称	说明
tableEvent	行点击时触发
脱敏记录
本 ABC 已完成脱敏（amt2abc.sanitized = true），处理项：

检查点	原始值	脱敏后	依据
applicationInfo.name	test1	simple-input-form	5.2 语义化命名
applicationInfo.id	6a3a1884a4c46a7c40616a75	000000000000000000000000	5.2 重新生成，去除内部库关联
applicationInfo.createAt	1749000000000	0	去除时间戳痕迹
applicationInfo.createBy	""	""（已为空）	无敏感信息
其余字段（inputs/outputs/methods/event/global/ui/i18n）经审查均为通用业务内容，无客户、产线、设备、内网地址等敏感信息。


来源
通用组件（已脱敏）。License: Apache-2.0。
