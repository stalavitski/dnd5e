# Generated by Django 3.0.3 on 2020-03-03 14:47

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_drop_ability_and_update_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='backgrounds', to='core.Source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('experience', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(355000)])),
                ('name', models.CharField(blank=True, max_length=50)),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='characters.Background')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('proficiency_bonus', models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(6)])),
                ('required_experience', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(355000)])),
                ('value', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=15, unique=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='core.Source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('proficiency', models.CharField(choices=[('none', 'None'), ('proficiency', 'Proficiency'), ('expertise', 'Expertise')], default='none', max_length=11)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_skills', to='characters.Character')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_skills', to='core.Skill')),
            ],
            options={
                'unique_together': {('character', 'skill')},
            },
        ),
        migrations.CreateModel(
            name='CharacterDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('alignment', models.CharField(blank=True, choices=[('lg', 'Lawful Good'), ('ng', 'Neutral Good'), ('cg', 'Chaotic Good'), ('ln', 'Lawful Neutral'), ('n', 'True Neutral'), ('cn', 'Chaotic Neutral'), ('le', 'Lawful Evil'), ('ne', 'True Evil'), ('ce', 'Chaotic Evil')], max_length=2)),
                ('appearance', models.TextField(blank=True)),
                ('portrait', models.ImageField(null=True, upload_to='')),
                ('eyes', models.CharField(blank=True, max_length=60)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('hair', models.CharField(blank=True, max_length=60)),
                ('height', models.IntegerField(blank=True, help_text='In inches', null=True)),
                ('history', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('organizations', models.TextField(blank=True, help_text='Allies and Organizations')),
                ('skin', models.CharField(blank=True, max_length=60)),
                ('weight', models.IntegerField(blank=True, help_text='In pounds', null=True)),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='characters.Character')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='character',
            name='skills',
            field=models.ManyToManyField(related_name='characters', through='characters.CharacterSkill', to='core.Skill'),
        ),
        migrations.CreateModel(
            name='CharacterSavingThrow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('ability', models.CharField(choices=[('str', 'Strength'), ('dex', 'Dexterity'), ('con', 'Constitution'), ('int', 'Intelligence'), ('wis', 'Wisdom'), ('cha', 'Charisma')], max_length=3)),
                ('is_proficient', models.BooleanField(default=False)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_saving_throws', to='characters.Character')),
            ],
            options={
                'unique_together': {('ability', 'character')},
            },
        ),
        migrations.CreateModel(
            name='CharacterAbility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('ability', models.CharField(choices=[('str', 'Strength'), ('dex', 'Dexterity'), ('con', 'Constitution'), ('int', 'Intelligence'), ('wis', 'Wisdom'), ('cha', 'Charisma')], max_length=3)),
                ('value', models.IntegerField(default=8, validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(20)])),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_abilities', to='characters.Character')),
            ],
            options={
                'unique_together': {('ability', 'character')},
            },
        ),
    ]
