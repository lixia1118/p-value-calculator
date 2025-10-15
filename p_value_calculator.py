#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P值计算器
根据回归系数、标准差和样本数计算p值
"""

import numpy as np
from scipy import stats
import math
import pandas as pd
import csv
import json
from typing import List, Dict, Union

def calculate_p_value(coefficient, std_error, sample_size, alpha=0.05):
    """
    计算回归系数的p值
    
    参数:
    coefficient: 回归系数
    std_error: 标准差/标准误
    sample_size: 样本数
    alpha: 显著性水平，默认为0.05
    
    返回:
    dict: 包含t统计量、p值、自由度等信息的字典
    """
    # 计算自由度 (样本数 - 参数个数，这里假设是简单回归，自由度为n-2)
    # 对于多元回归，自由度 = n - k - 1，其中k是解释变量个数
    df = sample_size - 2  # 简单线性回归的自由度
    
    # 计算t统计量
    t_statistic = coefficient / std_error
    
    # 计算p值 (双侧检验)
    p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df))
    
    # 判断是否显著
    is_significant = p_value < alpha
    
    # 计算置信区间 (95%)
    t_critical = stats.t.ppf(1 - alpha/2, df)
    margin_error = t_critical * std_error
    ci_lower = coefficient - margin_error
    ci_upper = coefficient + margin_error
    
    return {
        'coefficient': coefficient,
        'std_error': std_error,
        'sample_size': sample_size,
        'degrees_of_freedom': df,
        't_statistic': t_statistic,
        'p_value': p_value,
        'is_significant': is_significant,
        'alpha': alpha,
        'confidence_interval': (ci_lower, ci_upper),
        'margin_of_error': margin_error
    }

def calculate_p_value_multiple_regression(coefficient, std_error, sample_size, num_predictors, alpha=0.05):
    """
    计算多元回归中回归系数的p值
    
    参数:
    coefficient: 回归系数
    std_error: 标准差/标准误
    sample_size: 样本数
    num_predictors: 预测变量个数
    alpha: 显著性水平，默认为0.05
    
    返回:
    dict: 包含t统计量、p值、自由度等信息的字典
    """
    # 计算自由度 (样本数 - 预测变量个数 - 1)
    df = sample_size - num_predictors - 1
    
    # 计算t统计量
    t_statistic = coefficient / std_error
    
    # 计算p值 (双侧检验)
    p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df))
    
    # 判断是否显著
    is_significant = p_value < alpha
    
    # 计算置信区间 (95%)
    t_critical = stats.t.ppf(1 - alpha/2, df)
    margin_error = t_critical * std_error
    ci_lower = coefficient - margin_error
    ci_upper = coefficient + margin_error
    
    return {
        'coefficient': coefficient,
        'std_error': std_error,
        'sample_size': sample_size,
        'num_predictors': num_predictors,
        'degrees_of_freedom': df,
        't_statistic': t_statistic,
        'p_value': p_value,
        'is_significant': is_significant,
        'alpha': alpha,
        'confidence_interval': (ci_lower, ci_upper),
        'margin_of_error': margin_error
    }

def print_results(results):
    """
    格式化打印结果
    """
    print("=" * 60)
    print("P值计算结果")
    print("=" * 60)
    print(f"回归系数: {results['coefficient']:.6f}")
    print(f"标准误: {results['std_error']:.6f}")
    print(f"样本数: {results['sample_size']}")
    print(f"自由度: {results['degrees_of_freedom']}")
    print(f"t统计量: {results['t_statistic']:.6f}")
    print(f"p值: {results['p_value']:.6f}")
    print(f"显著性水平: {results['alpha']}")
    print(f"是否显著: {'是' if results['is_significant'] else '否'}")
    print(f"95%置信区间: [{results['confidence_interval'][0]:.6f}, {results['confidence_interval'][1]:.6f}]")
    print(f"误差幅度: {results['margin_of_error']:.6f}")
    print("=" * 60)

def batch_calculate_p_values(data_list: List[Dict], regression_type: str = "simple", alpha: float = 0.05) -> List[Dict]:
    """
    批量计算p值，支持每行数据使用不同的回归类型
    
    参数:
    data_list: 包含回归数据的字典列表，每个字典应包含:
        - coefficient: 回归系数
        - std_error: 标准误
        - sample_size: 样本数
        - num_predictors: 预测变量数 (仅多元回归需要)
        - significant_level: 显著性水平 (可选，如果提供则使用该值)
        - regression_type: 回归类型 (可选，如果提供则使用该值)
    regression_type: 默认回归类型 ("simple" 或 "multiple")
    alpha: 默认显著性水平
    
    返回:
    List[Dict]: 包含所有计算结果的列表
    """
    results = []
    
    for i, data in enumerate(data_list):
        try:
            # 使用数据中的显著性水平，如果没有则使用默认值
            current_alpha = data.get('significant_level', alpha)
            
            # 使用数据中的回归类型，如果没有则使用默认值
            current_regression_type = data.get('regression_type', regression_type)
            
            if current_regression_type == "simple":
                result = calculate_p_value(
                    coefficient=data['coefficient'],
                    std_error=data['std_error'],
                    sample_size=data['sample_size'],
                    alpha=current_alpha
                )
            elif current_regression_type == "multiple":
                if 'num_predictors' not in data:
                    raise ValueError(f"第{i+1}条数据缺少num_predictors字段")
                result = calculate_p_value_multiple_regression(
                    coefficient=data['coefficient'],
                    std_error=data['std_error'],
                    sample_size=data['sample_size'],
                    num_predictors=data['num_predictors'],
                    alpha=current_alpha
                )
            else:
                raise ValueError(f"第{i+1}条数据的regression_type必须是'simple'或'multiple'，当前值: {current_regression_type}")
            
            result['row_id'] = i + 1
            result['used_alpha'] = current_alpha  # 记录实际使用的显著性水平
            result['used_regression_type'] = current_regression_type  # 记录实际使用的回归类型
            results.append(result)
            
        except Exception as e:
            error_result = {
                'row_id': i + 1,
                'error': str(e),
                'coefficient': data.get('coefficient', 'N/A'),
                'std_error': data.get('std_error', 'N/A'),
                'sample_size': data.get('sample_size', 'N/A'),
                'significant_level': data.get('significant_level', 'N/A'),
                'regression_type': data.get('regression_type', 'N/A')
            }
            results.append(error_result)
    
    return results

def load_data_from_excel(file_path: str, sheet_name: str = None) -> List[Dict]:
    """
    从Excel文件加载数据
    
    参数:
    file_path: Excel文件路径
    sheet_name: 工作表名称，默认为第一个工作表
    
    返回:
    List[Dict]: 数据字典列表
    """
    try:
        # 读取Excel文件
        if sheet_name is None:
            # 如果没有指定工作表，读取第一个工作表
            df = pd.read_excel(file_path, sheet_name=0)
        else:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 确保df是DataFrame而不是字典
        if isinstance(df, dict):
            # 如果返回的是字典，取第一个值
            df = list(df.values())[0]
        
        data_list = []
        
        for _, row in df.iterrows():
            data = {
                'coefficient': float(row['coefficient']),
                'std_error': float(row['std_error']),
                'sample_size': int(row['sample_size'])
            }
            
            # 支持significant_level字段
            if 'significant_level' in df.columns:
                data['significant_level'] = float(row['significant_level'])
            
            # 支持num_predictors字段
            if 'num_predictors' in df.columns:
                data['num_predictors'] = int(row['num_predictors'])
            
            # 支持regression_type字段
            if 'regression_type' in df.columns:
                data['regression_type'] = str(row['regression_type']).strip().lower()
            
            data_list.append(data)
            
        return data_list
        
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    except KeyError as e:
        raise KeyError(f"Excel文件缺少必要的列: {e}")
    except Exception as e:
        raise Exception(f"读取Excel文件时出错: {e}")

def save_results_to_csv(results: List[Dict], output_path: str):
    """
    将结果保存到CSV文件，第二行添加中文说明
    
    参数:
    results: 计算结果列表
    output_path: 输出文件路径
    """
    if not results:
        print("没有结果可保存")
        return
    
    # 移除row_id字段
    cleaned_results = []
    for result in results:
        cleaned_result = {k: v for k, v in result.items() if k != 'row_id'}
        cleaned_results.append(cleaned_result)
    
    # 获取所有可能的字段
    all_fields = set()
    for result in cleaned_results:
        all_fields.update(result.keys())
    
    # 排序字段，将重要字段放在前面
    priority_fields = ['coefficient', 'std_error', 'sample_size', 't_statistic', 'p_value', 'is_significant']
    other_fields = sorted([f for f in all_fields if f not in priority_fields])
    fieldnames = [f for f in priority_fields if f in all_fields] + other_fields
    
    # 字段中文说明映射
    field_descriptions = {
        'row_id': '行号',
        'coefficient': '回归系数',
        'std_error': '标准误',
        'sample_size': '样本数',
        't_statistic': 't统计量',
        'p_value': 'p值',
        'is_significant': '是否显著',
        'alpha': '显著性水平',
        'used_alpha': '使用的显著性水平',
        'confidence_interval': '置信区间',
        'degrees_of_freedom': '自由度',
        'margin_of_error': '误差幅度',
        'num_predictors': '预测变量数',
        'regression_type': '回归类型',
        'used_regression_type': '使用的回归类型'
    }
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 写入英文列名
        writer.writeheader()
        
        # 写入中文说明行
        chinese_row = {}
        for field in fieldnames:
            chinese_row[field] = field_descriptions.get(field, field)
        writer.writerow(chinese_row)
        
        # 写入数据
        writer.writerows(cleaned_results)
    
    print(f"结果已保存到: {output_path}")

def save_results_to_excel(results: List[Dict], output_path: str, sheet_name: str = "P值计算结果"):
    """
    将结果保存到Excel文件，第二行添加中文说明
    
    参数:
    results: 计算结果列表
    output_path: 输出文件路径
    sheet_name: 工作表名称
    """
    if not results:
        print("没有结果可保存")
        return
    
    try:
        # 移除row_id字段
        cleaned_results = []
        for result in results:
            cleaned_result = {k: v for k, v in result.items() if k != 'row_id'}
            cleaned_results.append(cleaned_result)
        
        # 字段中文说明映射
        field_descriptions = {
            'coefficient': '回归系数',
            'std_error': '标准误',
            'sample_size': '样本数',
            't_statistic': 't统计量',
            'p_value': 'p值',
            'is_significant': '是否显著',
            'alpha': '显著性水平',
            'used_alpha': '使用的显著性水平',
            'confidence_interval': '置信区间',
            'degrees_of_freedom': '自由度',
            'margin_of_error': '误差幅度',
            'num_predictors': '预测变量数',
            'regression_type': '回归类型',
            'used_regression_type': '使用的回归类型'
        }
        
        # 创建DataFrame
        df = pd.DataFrame(cleaned_results)
        
        # 创建中文说明行
        chinese_row = {}
        for col in df.columns:
            chinese_row[col] = field_descriptions.get(col, col)
        
        # 将中文说明行插入到第二行
        # 首先创建一个新的DataFrame，包含中文说明行
        chinese_df = pd.DataFrame([chinese_row])
        
        # 合并中文说明行和原始数据
        result_df = pd.concat([chinese_df, df], ignore_index=True)
        
        # 保存到Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"结果已保存到: {output_path}")
    except Exception as e:
        print(f"保存Excel文件时出错: {e}")

def save_results_to_json(results: List[Dict], output_path: str):
    """
    将结果保存到JSON文件
    
    参数:
    results: 计算结果列表
    output_path: 输出文件路径
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {output_path}")
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

def print_batch_results(results: List[Dict]):
    """
    格式化打印批量结果
    """
    print("=" * 80)
    print("批量P值计算结果")
    print("=" * 80)
    
    # 统计信息
    total_count = len(results)
    error_count = sum(1 for r in results if 'error' in r)
    success_count = total_count - error_count
    significant_count = sum(1 for r in results if r.get('is_significant', False))
    
    print(f"总计算数: {total_count}")
    print(f"成功计算: {success_count}")
    print(f"计算错误: {error_count}")
    print(f"显著结果: {significant_count}")
    print("-" * 80)
    
    # 详细结果
    print(f"{'系数':<10} {'标准误':<10} {'样本数':<8} {'t统计量':<10} {'p值':<12} {'显著':<6} {'α水平':<8} {'回归类型':<8}")
    print("-" * 92)
    
    for result in results:
        if 'error' in result:
            print(f"{'ERROR':<10} {'ERROR':<10} {'ERROR':<8} {'ERROR':<10} {'ERROR':<12} {'ERROR':<6} {'ERROR':<8} {'ERROR':<8}")
        else:
            coefficient = f"{result.get('coefficient', 0):.4f}"
            std_error = f"{result.get('std_error', 0):.4f}"
            sample_size = result.get('sample_size', 'N/A')
            t_stat = f"{result.get('t_statistic', 0):.4f}"
            p_value = f"{result.get('p_value', 0):.6f}"
            significant = "是" if result.get('is_significant', False) else "否"
            alpha_level = f"{result.get('used_alpha', result.get('alpha', 0)):.3f}"
            regression_type = result.get('used_regression_type', 'N/A')
            
            print(f"{coefficient:<10} {std_error:<10} {sample_size:<8} {t_stat:<10} {p_value:<12} {significant:<6} {alpha_level:<8} {regression_type:<8}")

if __name__ == "__main__":
    # 示例用法
    print("示例1: 简单线性回归")
    results1 = calculate_p_value(coefficient=2.5, std_error=0.8, sample_size=100)
    print_results(results1)
    
    print("\n示例2: 多元回归")
    results2 = calculate_p_value_multiple_regression(
        coefficient=1.8, std_error=0.6, sample_size=150, num_predictors=3
    )
    print_results(results2)