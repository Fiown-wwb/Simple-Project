from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, HeatMap
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

def plot_rating_counts(df):
    """绘制评分次数最多的10部电影"""
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(df['title'].tolist())
        .add_yaxis("评分次数", df['rating_count'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分次数最多的10部电影"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45),
                name="电影名称"
            ),
            yaxis_opts=opts.AxisOpts(name="评分次数"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.render_embed()

def plot_gender_ratings(df):
    """绘制性别评分最高的电影"""
    # 数据处理：按性别分组
    male_data = df[df['gender'] == 'M']['avg_rating'].tolist()
    female_data = df[df['gender'] == 'F']['avg_rating'].tolist()
    titles = df['title'].unique().tolist()

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(titles)
        .add_yaxis("男性评分", male_data)
        .add_yaxis("女性评分", female_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="性别评分最高的10部电影"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45),
                name="电影名称"
            ),
            yaxis_opts=opts.AxisOpts(name="平均评分"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.render_embed()

def plot_age_ratings(df):
    """绘制年龄段评分分析"""
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(df['age_group'].tolist())
        .add_yaxis(
            "平均评分",
            df['avg_rating'].tolist(),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="编号为1314各年龄段平均评分"),
            xaxis_opts=opts.AxisOpts(name="年龄段"),
            yaxis_opts=opts.AxisOpts(name="平均评分"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.render_embed()

def plot_top_rated(df):
    """绘制评分最高的电影"""
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(df['title'].tolist())
        .add_yaxis(
            "平均评分",
            df['avg_rating'].tolist(),
            label_opts=opts.LabelOpts(position="right")
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分最高的10部电影"),
            xaxis_opts=opts.AxisOpts(name="平均评分"),
            yaxis_opts=opts.AxisOpts(name="电影名称"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.render_embed()

def plot_best_year(df):
    """绘制最佳年份电影"""
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(df['title'].tolist())
        .add_yaxis(
            "平均评分",
            df['avg_rating'].tolist(),
            label_opts=opts.LabelOpts(position="right")
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="最佳年份Top10电影"),
            xaxis_opts=opts.AxisOpts(name="平均评分"),
            yaxis_opts=opts.AxisOpts(name="电影名称"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.render_embed()

def plot_top_comedy(df):
    """绘制最佳喜剧电影"""
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(df['title'].tolist())
        .add_yaxis(
            "平均评分",
            df['avg_rating'].tolist(),
            label_opts=opts.LabelOpts(position="right")
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="最佳喜剧电影Top10"),
            xaxis_opts=opts.AxisOpts(name="平均评分"),
            yaxis_opts=opts.AxisOpts(name="电影名称"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.render_embed()

def plot_genre_ratings(df):
    """绘制各类型最佳电影热力图"""
    # 数据处理
    genres = df['genre'].unique().tolist()
    data = []
    for i, genre in enumerate(genres):
        genre_data = df[df['genre'] == genre]
        for j, (_, row) in enumerate(genre_data.iterrows()):
            data.append([i, j, row['avg_rating']])

    c = (
        HeatMap(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([str(i+1) for i in range(5)])  # 5个排名
        .add_yaxis(
            "评分",
            genres,
            data,
            label_opts=opts.LabelOpts(formatter=JsCode("function(params){return params.data[2].toFixed(2);}")),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各类型电影评分热力图"),
            visualmap_opts=opts.VisualMapOpts(),
            xaxis_opts=opts.AxisOpts(name="排名"),
            yaxis_opts=opts.AxisOpts(name="电影类型"),
        )
    )
    return c.render_embed()


def plot_movie_charts(data_dict):

        # 绘制每个图表
    plot_functions = {
        "rating_counts": plot_rating_counts,
        "gender_ratings": plot_gender_ratings,
        "age_ratings": plot_age_ratings,
        "top_rated": plot_top_rated,
        "best_year": plot_best_year,
        "top_comedy": plot_top_comedy,
        "top_by_genre": plot_genre_ratings
    }

    charts_html = {}

    # 依次绘制每个图表
    for data_name, plot_func in plot_functions.items():
        charts_html[data_name] = plot_func(data_dict[data_name])

    return charts_html