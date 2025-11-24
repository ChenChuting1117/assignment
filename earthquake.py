# 全部 import 放顶部
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as path_effects
import matplotlib.animation as animation

# 震级图例参数（全局）
legend_items = [
	(8.5, 'M≥8.5', '#370702'),
	(8.0, '8.0≤M<8.5', '#861B05'),
	(7.5, '7.5≤M<8.0', '#DC4323'),
	(7.0, '7.0≤M<7.5', '#f57200'),
]
legend_x = 0.98
legend_y = 0.15
legend_width = 0.015
legend_height = 0.18

# 读取地震数据 Excel 文件
df = pd.read_excel('earthquake20122025.xlsx', engine='openpyxl', header=1)
print(df.head())
print('字段名:', df.columns.tolist())
df = df.rename(columns={
	'Origin Time': 'time',
	'Magnitude (M)': 'magnitude',
	'Latitude (°)': 'latitude',
	'Longitude (°)': 'longitude',
	'Depth (km)': 'depth',
	'Reference Location': 'location'
})
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df = df.dropna(subset=['time', 'latitude', 'longitude', 'magnitude'])
df_sorted = df.sort_values('time').reset_index(drop=True)
df_sorted['year'] = df_sorted['time'].dt.year
df_sorted['month'] = df_sorted['time'].dt.month
years = sorted(df_sorted['year'].unique())

# 生成所有帧 (year, month)
fade_frames = 10  # 每个点出现后渐隐10帧（2秒）
frames = [(year, month) for year in years for month in range(1, 13)]

# 初始化主动画窗口
fig = plt.figure(figsize=(14,9))
fig.patch.set_facecolor('#475360')
left = 1 / 14
bottom = 0 / 9
width = 12 / 14
height = 8 / 9
ax = fig.add_axes([left, bottom, width, height], projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor='#f5edcd')
ax.add_feature(cfeature.OCEAN, facecolor='#5b6d80')
font = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=40)
for spine in ax.spines.values():
	spine.set_visible(False)
plt.title('Global Earthquakes of Magnitude 7 or Above, 2012–2025', fontproperties=font, color='#ffffff', pad=20)

# 初始化空的散点图和文本
scatter = ax.scatter([], [], s=[], alpha=0.7, transform=ccrs.PlateCarree(), edgecolors='none', antialiased=True)
year_month_font = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=15)
text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=15, color="#ffcb69", va='top', fontproperties=year_month_font)
text.set_path_effects([
	path_effects.Stroke(linewidth=1, foreground='#5b6d80'),
	path_effects.Normal()
])
# 让震级图例始终显示在动画主窗口
for i, (mag, label, color) in enumerate(legend_items):
	ax.add_patch(Rectangle((legend_x, legend_y + i*legend_height/4), legend_width, legend_height/4, transform=ax.transAxes, color=color, ec='none'))
	ax.text(legend_x-0.01, legend_y + i*legend_height/4 + legend_height/8, label, transform=ax.transAxes, fontsize=12, color=color, va='center', ha='right', fontweight='bold')

# 动画函数
def animate(i):
	if i == len(frames):
		plt.close(fig)
		show_all_points()
		return scatter, text
	elif i > len(frames):
		scatter.set_offsets(np.empty((0, 2)))
		scatter.set_sizes(np.array([0]))
		scatter.set_facecolor([])
		text.set_text("")
		return scatter, text
	year, month = frames[i]
	import calendar
	month_name = calendar.month_name[month]
	lons, lats, sizes, facecolors = [], [], [], []
	for j in range(fade_frames):
		idx = i - j
		if idx < 0:
			continue
		y, m = frames[idx]
		df_fade = df_sorted[(df_sorted['year'] == y) & (df_sorted['month'] == m)]
		scale = 1 + j / (fade_frames - 1) * 4  # 放大到5倍
		for _, row in df_fade.iterrows():
			mag = row['magnitude']
			lons.append(row['longitude'])
			lats.append(row['latitude'])
			sizes.append(mag * 10 * scale)
			if mag >= 8.5:
				color = '#370702'
			elif mag >= 8:
				color = '#861B05'
			elif mag >= 7.5:
				color = '#DC4323'
			elif mag >= 7:
				color = '#f57200'
			else:
				color = '#cccccc'
			import matplotlib.colors as mcolors
			facecolors.append(mcolors.to_rgba(color, 1))
	scatter.set_offsets(list(zip(lons, lats)))
	scatter.set_sizes(sizes if sizes else np.array([0]))
	scatter.set_facecolor(facecolors)
	text.set_text(f"Origin Time: {year}, {month_name}")
	return scatter, text

# 静态分布图函数
def show_all_points():
	fig2 = plt.figure(figsize=(14,9))
	fig2.patch.set_facecolor('#475360')
	ax2 = fig2.add_axes([left, bottom, width, height], projection=ccrs.PlateCarree())
	ax2.add_feature(cfeature.LAND, facecolor='#f5edcd')
	ax2.add_feature(cfeature.OCEAN, facecolor='#5b6d80')
	font2 = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=40)
	for spine in ax2.spines.values():
		spine.set_visible(False)
	plt.title('Global Earthquakes of Magnitude 7 or Above, 2012–2025', fontproperties=font2, color='#ffffff', pad=20)
	lons = df_sorted['longitude'].values
	lats = df_sorted['latitude'].values
	mags = df_sorted['magnitude'].values
	sizes = mags * 10
	facecolors = []
	for mag in mags:
		if mag >= 8.5:
			color = '#370702'
		elif mag >= 8:
			color = '#861B05'
		elif mag >= 7.5:
			color = '#DC4323'
		elif mag >= 7:
			color = '#f57200'
		else:
			color = '#cccccc'
		import matplotlib.colors as mcolors
		facecolors.append(mcolors.to_rgba(color, 1))
	ax2.scatter(lons, lats, s=sizes, alpha=0.7, transform=ccrs.PlateCarree(), edgecolors='none', facecolor=facecolors, antialiased=True)
	# 添加震级图例
	for i, (mag, label, color) in enumerate(legend_items):
		ax2.add_patch(Rectangle((legend_x, legend_y + i*legend_height/4), legend_width, legend_height/4, transform=ax2.transAxes, color=color, ec='none'))
		ax2.text(legend_x-0.01, legend_y + i*legend_height/4 + legend_height/8, label, transform=ax2.transAxes, fontsize=12, color=color, va='center', ha='right', fontweight='bold')
	plt.show()

# 运行动画
ani = animation.FuncAnimation(fig, animate, frames=len(frames) + fade_frames + 1, interval=200, blit=False, repeat=False)
plt.show()
# 添加震级示意图例变量（全局）
from matplotlib.patches import Rectangle
legend_items = [
	(8.5, 'M≥8.5', '#370702'),
	(8.0, '8.0≤M<8.5', '#861B05'),
	(7.5, '7.5≤M<8.0', '#DC4323'),
	(7.0, '7.0≤M<7.5', '#f57200'),
]
legend_x = 0.98
legend_y = 0.15
legend_width = 0.015
legend_height = 0.18
# 动画播放完后，绘制所有地震点静态分布图并永久显示（提前定义）
def show_all_points():
	fig2 = plt.figure(figsize=(14,9))
	fig2.patch.set_facecolor('#475360')
	ax2 = fig2.add_axes([left, bottom, width, height], projection=ccrs.PlateCarree())
	ax2.add_feature(cfeature.LAND, facecolor='#f5edcd')
	ax2.add_feature(cfeature.OCEAN, facecolor='#5b6d80')
	font2 = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=40)
	for spine in ax2.spines.values():
		spine.set_visible(False)
	plt.title('Global Earthquakes of Magnitude 7 or Above, 2012–2025', fontproperties=font2, color='#ffffff', pad=20)
	lons = df_sorted['longitude'].values
	lats = df_sorted['latitude'].values
	mags = df_sorted['magnitude'].values
	sizes = mags * 10
	facecolors = []
	for mag in mags:
		if mag >= 8.5:
			color = '#370702'
		elif mag >= 8:
			color = '#861B05'
		elif mag >= 7.5:
			color = '#DC4323'
		elif mag >= 7:
			color = '#f57200'
		else:
			color = '#cccccc'
		import matplotlib.colors as mcolors
		facecolors.append(mcolors.to_rgba(color, 1))
	ax2.scatter(lons, lats, s=sizes, alpha=0.7, transform=ccrs.PlateCarree(), edgecolors='none', facecolor=facecolors, antialiased=True)
	# 添加震级图例
for i, (mag, label, color) in enumerate(legend_items):
	ax.add_patch(Rectangle((legend_x, legend_y + i*legend_height/4), legend_width, legend_height/4, transform=ax.transAxes, color=color, ec='none'))
	ax.text(legend_x-0.01, legend_y + i*legend_height/4 + legend_height/8, label, transform=ax.transAxes, fontsize=12, color=color, va='center', ha='right', fontweight='bold')

fig.patch.set_facecolor('#475360')
from matplotlib.font_manager import FontProperties


# 设置地图区域为14x7英寸和位置
import cartopy.crs as ccrs
import cartopy.feature as cfeature

left = 1 / 14           # 距离左侧1英寸
bottom = 0/ 9          # 距离底部1英寸
width = 12 / 14         # 地图宽度12英寸
height = 8 / 9          # 地图高度8英寸
ax = fig.add_axes([left, bottom, width, height], projection=ccrs.PlateCarree())

import pandas as pd #地图数据

# 读取地震数据 Excel 文件
df = pd.read_excel('earthquake20122025.xlsx', engine='openpyxl', header=1)

# 显示前几行数据，预览字段和内容
print(df.head())

# 显示所有字段名
print('字段名:', df.columns.tolist())
# 数据清洗与字段重命名
df = df.rename(columns={
	'Origin Time': 'time',
	'Magnitude (M)': 'magnitude',
	'Latitude (°)': 'latitude',
	'Longitude (°)': 'longitude',
	'Depth (km)': 'depth',
	'Reference Location': 'location'
})

# 时间字段转换为 datetime 类型
df['time'] = pd.to_datetime(df['time'], errors='coerce')

# 去除缺失值
df = df.dropna(subset=['time', 'latitude', 'longitude', 'magnitude'])


# 按时间顺序动画显示地震点
import matplotlib.animation as animation


#背景颜色
ax.add_feature(cfeature.LAND, facecolor='#f5edcd')
ax.add_feature(cfeature.OCEAN, facecolor='#5b6d80')

#标题文本和字体
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=40)
for spine in ax.spines.values():
	spine.set_visible(False)
plt.title('Global Earthquakes of Magnitude 7 or Above, 2012–2025', fontproperties=font, color='#ffffff', pad=20)



# 按时间排序
# 按年份分组，每年所有地震点一起闪烁
# 按年份和月份分组动画，每年停留3秒，地震点按月份依次闪烁
df_sorted = df.sort_values('time').reset_index(drop=True)
df_sorted['year'] = df_sorted['time'].dt.year
df_sorted['month'] = df_sorted['time'].dt.month
years = sorted(df_sorted['year'].unique())


# 渐隐参数
fade_frames = 10  # 每个点出现后渐隐10帧（2秒）
frames = []
for year in years:
	for month in range(1, 13):
		frames.append((year, month))

# 必须在顶部补充动画模块
import numpy as np
import matplotlib.patheffects as path_effects
import matplotlib.animation as animation



# 初始化空的散点图和文本
scatter = ax.scatter([], [], s=[], alpha=0.7, transform=ccrs.PlateCarree(), edgecolors='none', antialiased=True)
year_month_font = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=15)
text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=15, color="#ffcb69", va='top', fontproperties=year_month_font)
text.set_path_effects([
	path_effects.Stroke(linewidth=1, foreground='#5b6d80'), 
	path_effects.Normal()
])
# 让震级图例始终显示在动画主窗口
for i, (mag, label, color) in enumerate(legend_items):
	ax.add_patch(Rectangle((legend_x, legend_y + i*legend_height/4), legend_width, legend_height/4, transform=ax.transAxes, color=color, ec='none'))
	ax.text(legend_x-0.01, legend_y + i*legend_height/4 + legend_height/8, label, transform=ax.transAxes, fontsize=12, color=color, va='center', ha='right', fontweight='bold')


def animate(i):
	year, month = frames[i]
	import calendar
	month_name = calendar.month_name[month]
	# 收集当前帧及fade_frames之前的所有地震点
	lons, lats, sizes, facecolors = [], [], [], []
	for j in range(fade_frames):
		idx = i - j
		if idx < 0:
			continue
		y, m = frames[idx]
		df_fade = df_sorted[(df_sorted['year'] == y) & (df_sorted['month'] == m)]
		# 逐渐放大，透明度保持最大
		scale = 1 + j / (fade_frames - 1) * 7  # 放大到7倍
		for _, row in df_fade.iterrows():
			mag = row['magnitude']
			lons.append(row['longitude'])
			lats.append(row['latitude'])
			sizes.append(mag * 2 * scale)

# 全局唯一 animate 函数
def animate(i):
	if i == len(frames):
		# 动画结束后，弹出静态分布图并关闭动画窗口
		plt.close(fig)
		show_all_points()
		return scatter, text
	elif i > len(frames):
		scatter.set_offsets(np.empty((0, 2)))
		scatter.set_sizes(np.array([0]))
		scatter.set_facecolor([])
		text.set_text("")
		return scatter, text
	year, month = frames[i]
	import calendar
	month_name = calendar.month_name[month]
	# 收集当前帧及fade_frames之前的所有地震点
	lons, lats, sizes, facecolors = [], [], [], []
	for j in range(fade_frames):
		idx = i - j
		if idx < 0:
			continue
		y, m = frames[idx]
		df_fade = df_sorted[(df_sorted['year'] == y) & (df_sorted['month'] == m)]
		# 逐渐放大，透明度保持最大
		scale = 1 + j / (fade_frames - 1) * 4  # 放大到5倍
		for _, row in df_fade.iterrows():
			mag = row['magnitude']
			lons.append(row['longitude'])
			lats.append(row['latitude'])
			sizes.append(mag * 10 * scale)
			if mag >= 8.5:
				color = '#370702'
			elif mag >= 8:
				color = '#861B05'
			elif mag >= 7.5:
				color = '#DC4323'
			elif mag >= 7:
				color = '#f57200'
			else:
				color = '#cccccc'
			import matplotlib.colors as mcolors
			facecolors.append(mcolors.to_rgba(color, 1))  # 透明度始终为1
	scatter.set_offsets(list(zip(lons, lats)))
	scatter.set_sizes(sizes if sizes else np.array([0]))
	scatter.set_facecolor(facecolors)
	text.set_text(f"Origin Time: {year}, {month_name}")
	return scatter, text

# 运行动画


ani = animation.FuncAnimation(fig, animate, frames=len(frames) + fade_frames + 1, interval=200, blit=False, repeat=False)
plt.show()

# 动画播放完后，绘制所有地震点静态分布图并永久显示
def show_all_points():
	fig2 = plt.figure(figsize=(14,9))
	fig2.patch.set_facecolor('#475360')
	ax2 = fig2.add_axes([left, bottom, width, height], projection=ccrs.PlateCarree())
	ax2.add_feature(cfeature.LAND, facecolor='#f5edcd')
	ax2.add_feature(cfeature.OCEAN, facecolor='#5b6d80')
	font2 = FontProperties(fname='fonts/Roboto_Condensed-Bold.ttf', size=40)
	for spine in ax2.spines.values():
		spine.set_visible(False)
	plt.title('Global Earthquakes of Magnitude 7 or Above, 2012–2025', fontproperties=font2, color='#ffffff', pad=20)
	lons = df_sorted['longitude'].values
	lats = df_sorted['latitude'].values
	mags = df_sorted['magnitude'].values
	sizes = mags * 10
	facecolors = []
	for mag in mags:
		if mag >= 8.5:
			color = '#370702'
		elif mag >= 8:
			color = '#861B05'
		elif mag >= 7.5:
			color = '#DC4323'
		elif mag >= 7:
			color = '#f57200'
		else:
			color = '#cccccc'
		import matplotlib.colors as mcolors
		facecolors.append(mcolors.to_rgba(color, 1))
	ax2.scatter(lons, lats, s=sizes, alpha=0.7, transform=ccrs.PlateCarree(), edgecolors='none', facecolor=facecolors, antialiased=True)
	# 添加震级图例
	for i, (mag, label, color) in enumerate(legend_items):
		ax2.add_patch(Rectangle((legend_x, legend_y + i*legend_height/4), legend_width, legend_height/4, transform=ax2.transAxes, color=color, ec='none'))
		ax2.text(legend_x-0.01, legend_y + i*legend_height/4 + legend_height/8, label, transform=ax2.transAxes, fontsize=12, color=color, va='center', ha='right', fontweight='bold')
	plt.show()

# 不再直接调用 show_all_points，交由动画最后一帧触发

# 添加震级示意图例
from matplotlib.patches import Rectangle
legend_items = [
    (8.5, 'M≥8.5', '#370702'),
    (8.0, '8.0≤M<8.5', '#861B05'),
    (7.5, '7.5≤M<8.0', '#DC4323'),
    (7.0, '7.0≤M<7.5', '#f57200'),
]
legend_x = 0.98
legend_y = 0.15
legend_width = 0.015
legend_height = 0.18
for i, (mag, label, color) in enumerate(legend_items):
    ax.add_patch(Rectangle((legend_x, legend_y + i*legend_height/4), legend_width, legend_height/4, transform=ax.transAxes, color=color, ec='none'))
    ax.text(legend_x-0.01, legend_y + i*legend_height/4 + legend_height/8, label, transform=ax.transAxes, fontsize=12, color=color, va='center', ha='right', fontweight='bold')
