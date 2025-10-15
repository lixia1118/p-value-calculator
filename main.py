#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门处理sample_data.xlsx文件的脚本
自动读取Excel文件，计算p值，并输出结果
"""

from p_value_calculator import (
    load_data_from_excel, 
    batch_calculate_p_values, 
    print_batch_results,
    save_results_to_csv,
    save_results_to_excel
)

def process_sample_data():
    """
    处理sample_data.xlsx文件
    """
    print("=" * 60)
    print("处理sample_data.xlsx文件")
    print("=" * 60)
    
    try:
        # 从Excel文件加载数据
        print("正在读取sample_data.xlsx...")
        data_list = load_data_from_excel('sample_data.xlsx')
        print(f"成功读取数据，共 {len(data_list)} 条记录")
        
        print(f"成功加载 {len(data_list)} 条数据")
        
        # 检查数据格式
        if data_list:
            sample_data = data_list[0]
            print("\n数据字段检查:")
            print(f"- coefficient: {sample_data.get('coefficient', 'N/A')}")
            print(f"- std_error: {sample_data.get('std_error', 'N/A')}")
            print(f"- sample_size: {sample_data.get('sample_size', 'N/A')}")
            print(f"- significant_level: {sample_data.get('significant_level', 'N/A')}")
            
            # 检查是否有significant_level字段
            has_significant_level = any('significant_level' in data for data in data_list)
            if has_significant_level:
                print("✓ 检测到significant_level字段，将使用每行数据的显著性水平")
            else:
                print("⚠ 未检测到significant_level字段，将使用默认显著性水平0.05")
        
        # 批量计算p值
        print("\n正在计算p值...")
        results = batch_calculate_p_values(data_list, "simple", 0.05)
        
        # 显示结果
        print_batch_results(results)
        
        # 保存结果
        print("\n正在保存结果...")
        save_results_to_csv(results, 'sample_data_results.csv')
        save_results_to_excel(results, 'sample_data_results.xlsx')
        
        print("\n处理完成！")
        print("输出文件:")
        print("- sample_data_results.csv")
        print("- sample_data_results.xlsx")
        
        return results
        
    except FileNotFoundError:
        print("错误: 找不到sample_data.xlsx文件")
        print("请确保文件存在于当前目录中")
        return None
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        return None

def show_data_summary(results):
    """
    显示数据摘要
    """
    if not results:
        return
    
    print("\n" + "=" * 60)
    print("数据摘要")
    print("=" * 60)
    
    total_count = len(results)
    error_count = sum(1 for r in results if 'error' in r)
    success_count = total_count - error_count
    significant_count = sum(1 for r in results if r.get('is_significant', False))
    
    print(f"总数据条数: {total_count}")
    print(f"成功计算: {success_count}")
    print(f"计算错误: {error_count}")
    print(f"显著结果: {significant_count}")
    
    if success_count > 0:
        # 统计p值分布
        p_values = [r.get('p_value', 0) for r in results if 'p_value' in r and 'error' not in r]
        if p_values:
            import statistics
            print(f"\nP值统计:")
            print(f"最小p值: {min(p_values):.6f}")
            print(f"最大p值: {max(p_values):.6f}")
            print(f"平均p值: {statistics.mean(p_values):.6f}")
            print(f"中位数p值: {statistics.median(p_values):.6f}")
            
            # 显著性水平分布
            alpha_levels = [r.get('used_alpha', r.get('alpha', 0)) for r in results if 'used_alpha' in r or 'alpha' in r]
            if alpha_levels:
                unique_alphas = list(set(alpha_levels))
                print(f"\n使用的显著性水平: {unique_alphas}")

if __name__ == "__main__":
    # 处理sample_data.xlsx文件
    results = process_sample_data()
    
    if results:
        # 显示数据摘要
        show_data_summary(results)
        
        print("\n" + "=" * 60)
        print("处理完成！")
        print("=" * 60)
    else:
        print("处理失败，请检查文件是否存在且格式正确")
