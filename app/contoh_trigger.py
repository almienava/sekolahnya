from django.db import models
from django_postgres_extensions.models.fields import JSONField
from django_postgres_extensions.models.trigger import TriggerMixin, Trigger

class Order(TriggerMixin, models.Model):
    order_number = models.CharField(max_length=10)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    class Meta:
        trigger_set = [
            Trigger(
                name='insert_to_log',
                event='insert',
                timing='after',
                func='insert_to_log_trigger',
                language='plpgsql',
                condition='NEW.is_completed = TRUE'
            )
        ]

    @staticmethod
    def insert_to_log_trigger():
        return """
            INSERT INTO order_log (order_id, action)
            VALUES (NEW.id, 'completed');
            RETURN NEW;
        """


# contoh create data
class YourModel(models.Model):
    column1 = models.CharField(max_length=100)
    column2 = models.IntegerField()
    column3 = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_data(cls, column1_value, column2_value):
        data = cls(column1=column1_value, column2=column2_value)
        data.save()
        return data


"""
NEW.id itu adalah dari data yang baru ditambahkan


ini untuk insert pakai where
INSERT INTO your_table_log (column1, column2, column3)
SELECT column1, column2, column3
FROM your_table
WHERE status = 'completed' and id = NEW.id;
"""