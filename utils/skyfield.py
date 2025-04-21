from skyfield.api import load, Topos, Star


def is_star_visible(ra, dec, lat, lon):
    ts = load.timescale()
    t = ts.now()
    eph = load('de421.bsp')
    observer = eph['earth'] + \
        Topos(latitude_degrees=lat, longitude_degrees=lon)
    star = Star(ra_hours=ra / 15.0, dec_degrees=dec)
    alt, _, _ = observer.at(t).observe(star).apparent().altaz()
    return alt.degrees > 0
