from django.db import models

import logging
logger = logging.getLogger('data')


from django.db import models


class MonthlyWeatherByCity(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    new_york_temp = models.DecimalField(max_digits=5, decimal_places=1)
    san_francisco_temp = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        db_table = 'monthly_weather_by_city'

