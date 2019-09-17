import flask
import db
import dateutil.parser
import plotly.graph_objects as pgo

profile = flask.Blueprint('profile', __name__)

@profile.route('/history/')
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

	datetime_strs, downloads, uploads, share_links = zip(*rows)
	datetimes = [dateutil.parser.parse(s) for s in datetime_strs]

	fig = pgo.Figure()

	fig.add_trace(
		pgo.Scattergl(
			x=datetimes,
			y=downloads,
			name='Download',
			line_color='deepskyblue',
			opacity=0.8))

	fig.add_trace(
		pgo.Scattergl(
			x=datetimes,
			y=uploads,
			name='Upload',
			line_color='dimgray',
			opacity=0.8))


	return flask.Response(fig.to_html())