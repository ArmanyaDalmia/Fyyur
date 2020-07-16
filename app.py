#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config. and Models.
#----------------------------------------------------------------------------#

from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  locations = Venue.query.distinct(Venue.city, Venue.state).all()

  for location in locations:
    venue = []
    for venue_location in Venue.query.filter_by(city=location.city, state=location.state).all():
      upcoming_shows = 0
      shows = Show.query.filter_by(venue_id=venue_location.id).all()

      for show in shows:
        if show.start_time > datetime.now():
            upcoming_shows += 1

      venue.append({
        'id': venue_location.id,
        'name': venue_location.name,
        'num_upcoming_shows': upcoming_shows
      })
    data.append({
      'city': location.city,
      'state': location.state,
      'venues': venue
    })
  return render_template('pages/venues.html', areas=data)



@app.route('/venues/search', methods=['POST'])
def search_venues():
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  filtered_results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in filtered_results:
      upcoming_shows = 0
      shows = Show.query.filter_by(venue_id=result.id).all()

      for show in shows:
        if show.start_time > datetime.now():
            upcoming_shows += 1
      data.append({
        "id": result.id,
        "name": result.name,
        "num_upcoming_shows": upcoming_shows
      })

  response={
    "count": len(filtered_results),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id

  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()

  data = {
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0
  }

  for show in shows:
    show_info = {
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    }
    if show.start_time < datetime.now():
      data['past_shows'].append(show_info)
    else:
      data['upcoming_shows'].append(show_info)

  data['past_show_count'] = len(data['past_shows'])
  data['upcoming_show_count'] = len(data['upcoming_shows'])

  return render_template('pages/show_venue.html', venue=data)



#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)



@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error = False

  try:
    form = VenueForm()
    new_venue = Venue(
      name=form.name.data,
      genres=form.genres.data,
      address=form.address.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data,
      image_link=form.image_link.data
    )
    db.session.add(new_venue)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())

  finally:
      db.session.close()

  if error:
    flash('Venue ' + request.form['name'] + ' couldn\'t be listed!')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')



@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  error = False
  try:
    venue = Venue.query.get(venue_id) 
    db.session.delete(venue)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('Venue ' + ' couldn\'t be deleted!')
  else:
    flash('Venue ' + ' was successfully deleted!')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))



#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():

  data = []
  performers = Artist.query.all()

  for performer in performers:
    data.append({
      'id': performer.id,
      'name': performer.name
    })

  return render_template('pages/artists.html', artists=data)



@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term=request.form.get('search_term', '')
  filtered_results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in filtered_results:
      upcoming_shows = 0
      shows = Show.query.filter_by(venue_id=result.id).all()

      for show in shows:
        if show.start_time > datetime.now():
            upcoming_shows += 1
      data.append({
        "id": result.id,
        "name": result.name,
        "num_upcoming_shows": upcoming_shows
      })

  response={
    "count": len(filtered_results),
    "data": data
  }


  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id

  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id).all()

  data = {
    "id": artist_id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0
  }

  for show in shows:
    show_info = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": format_datetime(str(show.start_time))
    }
    if show.start_time < datetime.now():
      data['past_shows'].append(show_info)
    else:
      data['upcoming_shows'].append(show_info)

  data['past_show_count'] = len(data['past_shows'])
  data['upcoming_show_count'] = len(data['upcoming_shows'])

  return render_template('pages/show_artist.html', artist=data)



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  performer = Artist.query.get(artist_id=artist_id)
  artist={
    "id": performer.id,
    "name": performer.name,
    "genres": performer.genres,
    "city": performer.city,
    "state": performer.state,
    "phone": performer.phone,
    "website": performer.website,
    "facebook_link": performer.facebook_link,
    "seeking_venue": performer.seeking_venue,
    "seeking_description":performer.seeking_description,
    "image_link": performer.image_link,
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist)



@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # artist record with ID <artist_id> using the new attributes

  error = False

  try:
    form = ArtistForm()
    artist = Artist.query.get(artist_id=artist_id)

    artist.name=form.name.data,
    artist.genres=form.genres.data,
    artist.city=form.city.data,
    artist.state=form.state.data,
    artist.phone=form.phone.data,
    artist.website=form.website.data,
    artist.facebook_link=form.facebook_link.data,
    artist.seeking_venue=form.seeking_venue.data,
    artist.seeking_description=form.seeking_description.data,
    artist.image_link=form.image_link.data

    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())

  finally:
      db.session.close()

  if error:
    flash('Artist ' + request.form['name'] + ' couldn\'t be updated!')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()
  venue = Venue.query.get(venue_id=venue_id)
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,    
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
  }
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)



@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  error = False

  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id=venue_id)

    venue.name=form.name.data,
    venue.genres=form.genres.data,
    venue.address=form.address.data,    
    venue.city=form.city.data,
    venue.state=form.state.data,
    venue.phone=form.phone.data,
    venue.website=form.website.data,
    venue.facebook_link=form.facebook_link.data,
    venue.seeking_talent=form.seeking_talent.data,
    venue.seeking_description=form.seeking_description.data,
    venue.image_link=form.image_link.data

    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())

  finally:
      db.session.close()

  if error:
    flash('Venue ' + request.form['name'] + ' couldn\'t be updated!')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # on successful db insert, flash success
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

  error = False

  try:
    form = ArtistForm()
    new_artist = Artist(
      name=form.name.data,
      genres=form.genres.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
      image_link=form.image_link.data
    )
    db.session.add(new_artist)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())

  finally:
      db.session.close()

  if error:
    flash('Artist ' + request.form['name'] + ' couldn\'t be listed!')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
  # displays list of shows at /shows
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  shows = Show.query.all()
  data = []

  for show in shows:
    data.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(str(show.start_time))
    })

  return render_template('pages/shows.html', shows=data)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)



@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # on successful db insert, flash success
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  error = False

  try:
    form = ShowForm()
    new_show = Show(
      venue_id=form.venue_id.data,
      artist_id=form.artist_id.data,
      start_time=form.start_time.data
    )
    db.session.add(new_show)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())

  finally:
      db.session.close()

  if error:
    flash('Show couldn\'t be listed!')
  else:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404



@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500



if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
