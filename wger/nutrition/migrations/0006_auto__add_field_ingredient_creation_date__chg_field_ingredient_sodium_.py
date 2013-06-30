# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Ingredient.creation_date'
        db.add_column('nutrition_ingredient', 'creation_date',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.date.today, blank=True),
                      keep_default=False)

        # Adding field 'Ingredient.update_date'
        db.add_column('nutrition_ingredient', 'update_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today),
                      keep_default=False)


        # Changing field 'Ingredient.sodium'
        db.alter_column('nutrition_ingredient', 'sodium', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Ingredient.fat'
        db.alter_column('nutrition_ingredient', 'fat', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=3))

        # Changing field 'Ingredient.carbohydrates_sugar'
        db.alter_column('nutrition_ingredient', 'carbohydrates_sugar', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Ingredient.fat_saturated'
        db.alter_column('nutrition_ingredient', 'fat_saturated', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Ingredient.fibres'
        db.alter_column('nutrition_ingredient', 'fibres', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Ingredient.protein'
        db.alter_column('nutrition_ingredient', 'protein', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=3))

        # Changing field 'Ingredient.carbohydrates'
        db.alter_column('nutrition_ingredient', 'carbohydrates', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=3))

    def backwards(self, orm):
        # Deleting field 'Ingredient.creation_date'
        db.delete_column('nutrition_ingredient', 'creation_date')

        # Deleting field 'Ingredient.update_date'
        db.delete_column('nutrition_ingredient', 'update_date')


        # Changing field 'Ingredient.sodium'
        db.alter_column('nutrition_ingredient', 'sodium', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Changing field 'Ingredient.fat'
        db.alter_column('nutrition_ingredient', 'fat', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

        # Changing field 'Ingredient.carbohydrates_sugar'
        db.alter_column('nutrition_ingredient', 'carbohydrates_sugar', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Changing field 'Ingredient.fat_saturated'
        db.alter_column('nutrition_ingredient', 'fat_saturated', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Changing field 'Ingredient.fibres'
        db.alter_column('nutrition_ingredient', 'fibres', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Changing field 'Ingredient.protein'
        db.alter_column('nutrition_ingredient', 'protein', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

        # Changing field 'Ingredient.carbohydrates'
        db.alter_column('nutrition_ingredient', 'carbohydrates', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exercises.language': {
            'Meta': {'object_name': 'Language'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'nutrition.ingredient': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ingredient'},
            'carbohydrates': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'carbohydrates_sugar': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'energy': ('django.db.models.fields.IntegerField', [], {}),
            'fat': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'fat_saturated': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'fibres': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'protein': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'sodium': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        'nutrition.ingredientweightunit': {
            'Meta': {'object_name': 'IngredientWeightUnit'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2'}),
            'gramm': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Ingredient']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.WeightUnit']"})
        },
        'nutrition.meal': {
            'Meta': {'ordering': "['time']", 'object_name': 'Meal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.NutritionPlan']"}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'nutrition.mealitem': {
            'Meta': {'object_name': 'MealItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Ingredient']"}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Meal']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'blank': 'True'}),
            'weight_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.IngredientWeightUnit']", 'null': 'True', 'blank': 'True'})
        },
        'nutrition.nutritionplan': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'NutritionPlan'},
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Language']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'nutrition.weightunit': {
            'Meta': {'ordering': "['name']", 'object_name': 'WeightUnit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exercises.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['nutrition']