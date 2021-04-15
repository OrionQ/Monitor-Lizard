from django.test import TestCase
import models

# Create your tests here.
class ModelsTestCase(TestCase):
    def setUp(self):
        models.objects.create(name="cpu_usage",category="cpu",metric_type="Integer")
        
    def test_models_have_correct_fields(self):
        cpu = models.objects.get(name="cpu_usage")
        self.assertEqual(cpu.name(), "cpu_usage")
        self.assertEqual(cpu.category(), "cpu")
        self.assertEqual(cpu.metric_type(), "Integer")