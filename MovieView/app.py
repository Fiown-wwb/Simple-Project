from flask import Flask, render_template
from charts import plot_movie_charts
from db_utils import get_movie_data
import sys

# 存储图表HTML代码的全局变量
global_charts = None

def initialize_charts():
    print("开始生成图表...")

    try:
        # 获取数据
        data = get_movie_data()
            # 生成图表
        global global_charts
        global_charts = plot_movie_charts(data)

        # 验证所有必需的图表都已生成
        required_charts = [
            "rating_counts", "gender_ratings", "age_ratings",
            "top_rated", "best_year", "top_comedy", "top_by_genre"
        ]

        missing_charts = [chart for chart in required_charts if chart not in global_charts]

        if missing_charts:
            print(f"错误: 以下图表未能生成: {', '.join(missing_charts)}")
            return False

        print("所有图表生成成功!")
        return True

    except Exception as e:
        print(f"生成图表时发生错误: {str(e)}")
        return False

    # 创建 Flask 应用


app = Flask(__name__)


@app.route('/')
def index():
    if global_charts is None:
        return "错误: 图表未初始化", 500
    return render_template('index.html', charts=global_charts)


def main():
    """主函数"""
    # 首先生成图表
    if not initialize_charts():
        print("图表初始化失败，程序退出")
        sys.exit(1)

        # 图表生成成功后启动 Flask
    print("\n所有图表已准备就绪!")
    print("启动 Flask 服务器...")
    print("请访问 http://localhost:5000 查看数据可视化仪表板")

    # 启动 Flask 应用
    app.run(debug=False, port=5000)


if __name__ == '__main__':
    main()