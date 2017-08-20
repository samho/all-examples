from sqlalchemy import MetaData, create_engine, Table, select

metadata = MetaData()
engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')

artist = Table('Artist', metadata, autoload=True, autoload_with=engine)

print artist.columns.keys()
s = select([artist]).limit(10)
print engine.execute(s).fetchall()

album = Table('Album', metadata, autoload=True, autoload_with=engine)
print metadata.tables.items()[0]
# print album.foreign_keys()

metadata.reflect(bind=engine)
print metadata.tables.keys()
playlist = metadata.tables['Playlist']
s1 = select([playlist]).limit(10)
print engine.execute(s1).fetchall()



