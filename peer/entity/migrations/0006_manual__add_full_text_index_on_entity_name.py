from south import db
from south.v2 import SchemaMigration
from django.conf import settings


class Migration(SchemaMigration):

    def forwards(self, orm):
        if db.engine == 'south.db.postgresql_psycopg2':
            lang = getattr(settings, 'PG_FT_INDEX_LANGUAGE', 'english')
            db.db.execute("CREATE INDEX entity_entity_name_idx"
                       " ON entity_entity"
                       " USING gin(to_tsvector('%s', name));" % lang)
            print "Just created a fulltext index on entity_entity.name..."


    def backwards(self, orm):
        pass
