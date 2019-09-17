import flask
import db
# import plotly.graph_objects as pgo

profile = flask.Blueprint('profile', __name__)

@profile.route('/history.svg')
def history():
	args = flask.request.args
	start_datetime = args.get('start_datetime', 'now')
	start_offset = args.get('start_offset', '-7 days')
	end_datetime = args.get('end_datetime', 'now')
	end_offset = args.get('end_offset', '0 days')
	rows = db.fetchall('''
		select `timestamp`, download, upload, share
		from speedtest
		where datetime(`timestamp`) >= datetime(?, ?)
		and datetime(`timestamp`) <= datetime(?, ?)
	''', (start_datetime, start_offset, end_datetime, end_offset))

	datetimes, downloads, uploads, share_links = zip(*rows)

	# fig = pgo.Figure()

	# timestamps = []
	# downloads = []
	# uploads = []
	# shares = []

	# fig.add_trace(pgo.Scatter(
	#                 x=df.Date,
	#                 y=df['AAPL.High'],
	#                 name="AAPL High",
	#                 line_color='deepskyblue',
	#                 opacity=0.8))

	# fig.add_trace(go.Scatter(
	#                 x=df.Date,
	#                 y=df['AAPL.Low'],
	#                 name="AAPL Low",
	#                 line_color='dimgray',
	#                 opacity=0.8))

	# # Use date string to set xaxis range
	# fig.update_layout(xaxis_range=['2016-07-01','2016-12-31'],
	#                   title_text="Manually Set Date Range")
	# fig.show()
	return ''