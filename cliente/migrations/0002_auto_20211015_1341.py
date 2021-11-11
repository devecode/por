# Generated by Django 2.2 on 2021-10-15 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='abono',
        ),
        migrations.CreateModel(
            name='Abono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abono', models.FloatField(default=0)),
                ('fa', models.DateTimeField(auto_now_add=True)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente')),
                ('num_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.VentaGeneral')),
            ],
        ),
    ]
