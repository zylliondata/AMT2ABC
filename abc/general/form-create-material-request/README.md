创建物料请求 ABC
form-create-material-request · category: form · industry: general

用于应用缺货时填写货物信息以及补货数量，创建补货请求

接口契约
Inputs
名称	类型	说明	默认值
material_definition_id string 物料ID ""
material_description string 物料介绍 ""
qty integer 物料数量 0
status string 当前货物状态 ""
due_date timestampz 过期时间 ""
kanban_id string 看板ID ""
tenant_id string 租户ID ""
token string 用户身份令牌 ""
resource_id string 数据产品ID ""
image_url string 物料图片链接 ""
Outputs
名称	类型	说明
Methods
名称	说明
Events
名称	说明
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
