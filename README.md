
## 回归系数 P 值计算器

本项目提供了一个便捷工具 `p_value_calculator.py`，用于根据给定的回归统计量（如系数、标准误等）反推计算 **$p$ 值 (P-value)**。

### 使用步骤

#### 1. 数据准备
请编辑项目目录下的 **`sample_data.xlsx`** 文件。请确保包含以下关键字段：

| 字段名 (Column) | 含义说明 | 备注 |
| :--- | :--- | :--- |
| **coefficient** | 回归系数 | 想要计算 $p$ 值的对应系数 ($\beta$) |
| **std_error** | 标准误 | 该系数的标准误差 (Standard Error) |
| **sample_size** | 样本数量 | 观测值总数 ($N$) |
| **significant_level** | 显著性水平 | 例如 0.05, 0.01 等 |
| **regression_type** | 回归类型 | 标识是否为多变量回归 |
| **num_preditor** | 自变量总数 | 回归方程中预测变量(Predictors)的数量 |

> **注意**：字段名请保持与上方列表严格一致（例如 `num_preditor`），以免程序读取出错。

#### 2. 运行计算
数据录入完成后，在终端或 IDE 中运行以下脚本：

```bash
python p_value_calculator.py
```

#### 3. 获取结果
程序运行完成后，计算结果将自动导出并覆盖以下两个文件，您可以任选其一查看：

*   **`sample_data_result.csv`**
*   **`sample_data_result.xlsx`**
