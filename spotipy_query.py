#Create class object to pass to the search

class spotipy_query():
    def __init__(self,row):
        self.song = row['Name'].lower()
        self.artist = row['Artist'].lower()
        self.album = row['Album'].lower()
        self.year = row['Year']
    
    def querify_strict(self):
        q = 'track:'+self.song+' album:'+self.album+' artist:'+self.artist
        # ' album:'+self.album+' artist'+self.artist
        # +'year'+str(self.year)
        return(q)
    def querify_less(self):
        #TODO if the first query fails, try again with less strict criteria, just need to figure out what that is
        q = 'track:'+self.song+' artist:'+self.artist
        return(q)
    def failed_to_db(self,sql_statement,db_conn,strict_less):
        params_dict = (self.song,self.artist,self.album,self.year,strict_less)
        #create this above when the db gets spun up.
        cur = db_conn.cursor()
        cur.execute(sql_statement,params_dict)
        # TODO do I need a commit after each execute, or can I move this to the end of processing?
        db_conn.commit()
    def write_to_playlist(playlist_id):
        pass

def search_loop(query_row,playlist='',client,out_list,insert_statement,db):
    active_obj = spotipy_query(query_row)
    obj_query = active_obj.querify_less()
    results=client.search(q=obj_query,limit=1)
    if results['tracks']['items']:
        # TODO this can take a list of items, so not sure if it makes more sense to do it here or at the end
        if playlist == '':
            out_list.append(results['tracks']['items'][0][id])
        else:
            # TODO flesh this out after I've created the track
            sp.user_playlist_add_tracks(user,playlist,track)
    else:
        active_obj.failed_to_db(failed_to_find,missing_db,'more_strict')