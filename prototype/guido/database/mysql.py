import re, sys, os, time
import ConfigParser
import MySQLdb
import _mysql_exceptions

class DB(object):
    def __init__( self ):
        #print "__init__"
        self._is_closed = False

    def get_connection( self ):
        conf = ConfigParser.ConfigParser()
        location = os.path.dirname(__file__)
        fn = os.path.join(location, "config.ini")
        conf.read(fn) 
        try:
            #
            # This makes a single MysQLdb.connect object which is shared by
            # every instance of the db.DB class
            #
            thehost = conf.get('database', 'host')
            theuser = conf.get('database', 'user')
            thepasswd = conf.get('database', 'passwd')
            thedb = conf.get('database', 'db')
            DB.cnx = MySQLdb.connect(host=thehost,user=theuser,passwd=thepasswd,db=thedb)
            #print "Got here"
            self._is_closed = False
        except _mysql_exceptions.OperationalError:
            sys.exit('Failed to form a MySQLdb cnx')
        return DB.cnx


    def do_query(self, sql, substitutions=None):
        self.cnx = self.get_connection()
        new_results = [];
        try:
            # Execute the SQL command
            self.cursor = self.cnx.cursor(MySQLdb.cursors.DictCursor)
            if substitutions:
                self.cursor.execute(sql.encode('UTF-8'), substitutions)
            else:
                self.cursor.execute(sql.encode('UTF-8'))
            #print "OK, I got something"
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            #print results
            for row in results:
                new_row = {}
                for k in row.keys():
                    new_row[k] = row[k]
                new_results.append(new_row)
        except Exception, e:
            return str(e)

        return new_results

    def fetchone(self, sql, substitutions=None):
        self.cnx = self.get_connection()
        try:
            self.cursor = self.cnx.cursor(MySQLdb.cursors.DictCursor)
            if substitutions:
                self.cursor.execute(sql.encode('UTF-8'), substitutions)
            else:
                self.cursor.execute(sql.encode('UTF-8'))
            out = {}
            result = self.cursor.fetchone()
            for k in result.keys():
                out[k] = result[k]
        except:
            return None
        return out

    def do_commit( self, sql, param ):
        """Execute some SQL and return the lastrowid, the key of the row that
        was most recently added. """
        self.cnx = self.get_connection()
        try:
            # Execute the SQL command
            self.cursor = self.cnx.cursor()
            self.cursor.execute(sql.encode('UTF-8'), param)
            #print "OK, I committed"
            return self.cursor.lastrowid
        except:
            self.cnx.rollback()    
            print "Error: I rolled back your commit %s, %s" % (sql, param)
            return None

    def close(self):
        if not self._is_closed:
            try:
                self.cnx.cursor().close()
                self.cnx.commit()
                self.cnx.close()
            except MySQLdb.ProgrammingError:
                pass # this error would mean it's already closed.  So, ignore
            self._is_closed = True

