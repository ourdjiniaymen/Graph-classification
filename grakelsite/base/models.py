from django.db import models

# Create your models here.


class Dataset(models.Model):
    name = models.CharField(max_length=200, unique=True)
    number_graphs = models.IntegerField()
    number_classes = models.IntegerField()
    classes_imbalance = models.CharField(max_length=200)
    average_nodes = models.FloatField()
    average_edges = models.FloatField()
    labels_number = models.CharField(max_length=200)
    attribute_dimension = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Kernel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    use_node_labels = models.BooleanField()
    use_node_attributes = models.BooleanField()

    def __str__(self) -> str:
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=200)
    kernel = models.ForeignKey(Kernel, on_delete=models.CASCADE)
    values = models.JSONField()

    def kernel_name(self):
        return self.kernel.name

    def __str__(self) -> str:
        return self.name


class Evaluation(models.Model):
    kernel = models.CharField(max_length=200)
    dataset = models.CharField(max_length=200)
    rbf = models.BooleanField()
    sigma = models.JSONField()
    normalize = models.BooleanField()
    c = models.JSONField()
    cv = models.IntegerField()
    experiments = models.IntegerField()
    with_labels = models.BooleanField()
    with_attributes = models.BooleanField()
    parameters = models.JSONField()


class Result(models.Model):
    kernel = models.CharField(max_length=200)
    dataset = models.CharField(max_length=200)
    accuracy = models.FloatField()
    standard_deviation = models.FloatField()
    running_time = models.FloatField()
    rbf = models.BooleanField()
    sigma = models.FloatField()
    normalize = models.BooleanField()
    c = models.IntegerField()
    cv = models.IntegerField()
    experiments = models.IntegerField()
    with_labels = models.BooleanField()
    with_attributes = models.BooleanField()
    parameters = models.JSONField()
    
    def __str__(self) -> str:
        return self.kernel+' - '+self.dataset