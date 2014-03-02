# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('core', '0005_auto__add_license'),
    )

    def forwards(self, orm):
        # Adding field 'Ingredient.license'
        db.add_column(u'nutrition_ingredient', 'license',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.License']),
                      keep_default=False)

        # Adding field 'Ingredient.license_author'
        db.add_column(u'nutrition_ingredient', 'license_author',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Ingredient.license'
        db.delete_column(u'nutrition_ingredient', 'license_id')

        # Deleting field 'Ingredient.license_author'
        db.delete_column(u'nutrition_ingredient', 'license_author')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.language': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'Language'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'core.license': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'License'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'nutrition.ingredient': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ingredient'},
            'carbohydrates': ('wger.utils.fields.Html5DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'carbohydrates_sugar': ('wger.utils.fields.Html5DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'energy': ('wger.utils.fields.Html5IntegerField', [], {}),
            'fat': ('wger.utils.fields.Html5DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'fat_saturated': ('wger.utils.fields.Html5DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'fibres': ('wger.utils.fields.Html5DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['core.License']"}),
            'license_author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'protein': ('wger.utils.fields.Html5DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'sodium': ('wger.utils.fields.Html5DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '2'}),
            'update_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'nutrition.ingredientweightunit': {
            'Meta': {'object_name': 'IngredientWeightUnit'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'}),
            'gramm': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nutrition.Ingredient']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nutrition.WeightUnit']"})
        },
        u'nutrition.meal': {
            'Meta': {'ordering': "['time']", 'object_name': 'Meal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nutrition.NutritionPlan']"}),
            'time': ('wger.utils.fields.Html5TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'nutrition.mealitem': {
            'Meta': {'object_name': 'MealItem'},
            'amount': ('wger.utils.fields.Html5DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nutrition.Ingredient']"}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nutrition.Meal']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'blank': 'True'}),
            'weight_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nutrition.IngredientWeightUnit']", 'null': 'True', 'blank': 'True'})
        },
        u'nutrition.nutritionplan': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'NutritionPlan'},
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'has_goal_calories': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'nutrition.weightunit': {
            'Meta': {'ordering': "['name']", 'object_name': 'WeightUnit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['nutrition']
